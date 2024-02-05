from typing import Dict, Tuple
from artnet.packet_buffer import Buffer


class PacketBuild:
    """Составление Art-Net пакета
        0 - id (7 x bytes + Null)
        8 - opcode (2 x 8 low byte first)
        10 - protocol version (2 x 8 high byte first)\
        12 - sequence (int 8)
        13 - physical port
        14 - universe
            Bit 3 - 0 = Universe (1-16)
            Bit 7 - 4 = Subnet (1-16)
        15 - net
            Bit 14 - 8 = Net (1-128)
        15 = 0
        16 - packet size (2 x 8 high byte first)
        next - data

        use example
        a = PacketBuild({1: 5}, 1, 2, 3).build()
        """

    def __init__(self, values: Dict[int, int], universe: int = 0, subnet: int = 0, net: int = 0):
        """Инициализация с заданными параметрами"""

        self.values = values
        self.universe = universe
        self.subnet = subnet
        self.net = net
        self.header = bytearray(b'Art-Net\x00\x00P\x00\x0e\x00\x00')
        self.data = bytearray(512)
        self.buffer = Buffer(self.universe, self.subnet, self.net)

    def build(self) -> None:
        """Построение пакета"""

        subnet_universe = (self.subnet << 8) | self.universe
        self.header += subnet_universe.to_bytes(2, byteorder='big')
        self.header.append(self.net & 0xFF)

        self.header.append(0x02 & 0x00)

        if not self.values:
            packet = self.header + self.data
        else:
            for address in self.values:
                self.data[address - 1] = self.values.get(address)

            packet = self.header + self.data
        # добавляем пакет в буффер
        self.buffer.append(packet)


class PackerRebuild:
    """Изменения data Art-Net пакета в зависимости от пришедших данные, 18 индекса начинается data
     use example b = PackerRebuild(a, {1:255}).rebuild()"""

    def __init__(self, packet: bytearray, values: Dict[int, int], net_settings: Tuple[int, int, int]):
        self.packet = packet
        self.values = values
        self.start_data_index = 18
        self.net_settings = net_settings
        self.buffer = Buffer(*self.net_settings)

    def rebuild(self) -> None:
        for address in self.values:
            index = self.start_data_index + address - 1
            self.packet[index] = self.values.get(address)
        # добавляем данные в буфер
        self.buffer.append(self.packet)
