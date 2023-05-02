import struct
import logging
import socket
import asyncio
import asyncio_dgram

from enum import IntEnum

UDP_PORT = 1337

_LOGGER = logging.getLogger(__name__)

class TSmartMode(IntEnum):
    MANUAL   = 0x00
    ECO      = 0x01
    SMART    = 0x02
    TIMER    = 0x03
    TRAVEL   = 0x04
    BOOST    = 0x05
    LIMITED  = 0x21
    CRITICAL = 0x22

class TSmart:

    def __init__(self, device_id, ip, name):
        self.device_id = device_id
        self.ip = ip
        self.name = name
        self.power = None
        self.temperature = None
        self.mode = None
        self.setpoint = None

    async def async_discover():

        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 1337))

        _LOGGER.info("Performing discovery")

        stream = await asyncio_dgram.from_socket(sock)
        response_struct = struct.Struct("=BBBHL32sBB")

        devices = dict()

        data = None
        for i in range(2):
            message = struct.pack("=BBBB", 0x01, 0, 0, 0x01 ^ 0x55)

            await stream.send(message, ("255.255.255.255", UDP_PORT))

            _LOGGER.info("Discovery message sent")

            while True:
                try:
                    data, remote_addr = await asyncio.wait_for(stream.recv(), 2)
                    if len(data) == len(message):
                        # Got our own broadcast
                        continue

                    if len(data) != response_struct.size:
                        _LOGGER.warn("Unexpected packet length (got: %d, expected: %d)" % (len(data), response_struct.size))
                        continue

                    if data[0] == 0:
                        _LOGGER.warn("Got error response (code %d)" % (data[0]))
                        continue

                    if data[0] != message[0] or data[1] != data[1] or data[2] != data[2]:
                        _LOGGER.warn("Unexpected response type (%02X %02X %02X)" % (data[0], data[1], data[2]))
                        continue

                    t = 0
                    for b in data[:-1]:
                        t = t ^ b
                    if t ^ 0x55 != data[-1]:
                        _LOGGER.warn("Received packet checksum failed")
                        continue

                    _LOGGER.info("Got response from %s" % remote_addr[0])

                    if remote_addr[0] not in devices:
                        (cmd, sub, sub2, device_type, device_id, name, tz, checksum) = response_struct.unpack(data)
                        name = name.decode('utf-8').split('0x00')[0]
                        device_id_str = "%4X" % device_id
                        _LOGGER.info("Discovered %s %s" % (device_id_str, name))
                        devices[remote_addr[0]] = TSmart(device_id_str, remote_addr[0], name)

                except asyncio.exceptions.TimeoutError:
                    break


        stream.close()
        _LOGGER.info("Discovery done")

        #devices[1234] = TSmart('1234', '192.168.0.161', 'Device 2')
        return devices.values()


    async def _async_request(self, request, response_struct):
        t = 0
        request = bytearray(request)
        for b in request[:-1]:
            t = t ^ b
        request[-1] = t ^ 0x55

        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 1337))
        sock.connect((self.ip, UDP_PORT))

        stream = await asyncio_dgram.from_socket(sock)

        data = None
        for i in range(2):

            await stream.send(request)

            _LOGGER.info("Message sent to %s" % self.ip)

            try:
                data, remote_addr = await asyncio.wait_for(stream.recv(), 2)
                if len(data) != response_struct.size:
                    _LOGGER.warn("Unexpected packet length (got: %d, expected: %d)" % (len(data), response_struct.size))
                    continue

                if data[0] == 0:
                    _LOGGER.warn("Got error response (code %d)" % (data[0]))
                    continue

                if data[0] != request[0] or data[1] != data[1] or data[2] != data[2]:
                    _LOGGER.warn("Unexpected response type (%02X %02X %02X)" % (data[0], data[1], data[2]))
                    continue

                t = 0
                for b in data[:-1]:
                    t = t ^ b
                if t ^ 0x55 != data[-1]:
                    _LOGGER.warn("Received packet checksum failed")

            except asyncio.exceptions.TimeoutError:
                continue

            break

        stream.close()

        if data is None:
            _LOGGER.warn("Timed-out fetching status from %s" % self.ip)
            return None
        return data

    async def _async_get_status(self):

        request = struct.pack("=BBBB", 0xF1, 0, 0, 0)

        response_struct = struct.Struct("=BBBBHBHBBH16sB")
        response = await self._async_request(request, response_struct)

        if response is None:
            return

        (cmd, sub, sub2, power, setpoint, mode, t_high, relay, smart_state, t_low, error, checksum) = response_struct.unpack(response)

        self.temperature = (t_high + t_low) / 20
        self.setpoint = setpoint / 10
        self.power = bool(power)
        self.mode = TSmartMode(mode)
        self.relay = bool(relay)

        _LOGGER.info("Received status from %s" % self.ip)

    async def _async_control_set(self, power, mode, setpoint):
        _LOGGER.info("Async control set %d %d %0.2f" % (power, mode, setpoint))

        if mode < 0 or mode > 5:
            raise ValueError("Invalid mode")

        request = struct.pack("=BBBBHBB", 0xF2, 0, 0, int(power), int(setpoint*10), mode, 0)

        response_struct = struct.Struct("=BBBB")
        response = await self._async_request(request, response_struct)