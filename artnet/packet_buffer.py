from typing import Optional, Tuple, Dict
from loguru import logger
from multiprocessing import Manager


class Buffer:
    """Проверка данных в буфере, если пакет с такими же uni, subne, net есть в буфере - пересобираем пакет"""

    __instance = None
    __pass = True

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, universe: int = 0, subnet: int = 0, net: int = 0):
        self.universe = universe
        self.subnet = subnet
        self.net = net
        if self.__pass:
            self.global_manager = Manager()
            self.buffer: Dict[Tuple, bytearray] = self.global_manager.dict()
            self.__pass = False

    def append(self, packet) -> None:
        self.buffer.update({(self.universe, self.subnet, self.net): packet})
        logger.debug(f'Добавление данных в буфер {packet}, с u/s/n {self.universe, self.subnet, self.net}')

    def get_packet(self) -> Optional[bytearray]:
        if (self.universe, self.subnet, self.net) in self.buffer:
            _packet = self.buffer.get((self.universe, self.subnet, self.net))
            logger.debug(f'Возврат пакета данных из буфера {_packet}, с u/s/n {self.universe, self.subnet, self.net}')
            return _packet
        logger.debug('Пакета с такими u/s/n нет в буфере')


class GetData(Buffer):
    """Класс для получения данных из буффера, для пользовательского интерфейса"""

    def get_value(self, universe: int, address: int, net: int = 0, subnet: int = 0) -> int:
        logger.debug(f'Запрос на данные из буфера: {net, subnet, universe, address}')
        packet = self.buffer.get((net, subnet, universe))
        return self.translate(packet, address)

    @staticmethod
    def translate(packet: bytearray, address: int) -> int:
        start_data_index = 18
        index = start_data_index + address - 1
        return int(packet[index])
