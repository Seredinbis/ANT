from typing import Optional
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
            self.buffer = self.global_manager.dict()
            self.__pass = False

    def get_buffer(self) -> bytearray:
        logger.debug(f'Запрос всех данных из буффера')
        return self.buffer

    def append(self, packet) -> None:
        self.buffer.update({(self.universe, self.subnet, self.net): packet})
        logger.debug(f'Добавление данных в буфер {packet}, с u/s/n {self.universe, self.subnet, self.net}')

    def get_packet(self) -> Optional[bytearray]:
        if (self.universe, self.subnet, self.net) in self.buffer:
            _packet = self.buffer.get((self.universe, self.subnet, self.net))
            logger.debug(f'Возврат пакета данных из буфера {_packet}, с u/s/n {self.universe, self.subnet, self.net}')
            return _packet
        logger.debug('Пакета с такими u/s/n нет в буфере')
