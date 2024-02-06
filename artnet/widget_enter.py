from typing import Dict, Optional
from artnet.packet_buffer import Buffer
from artnet.packet_build import PackerRebuild, PacketBuild
from loguru import logger
from multiprocessing import Process
from artnet.socet_send.send import SocketSend
from config.secret import logs_path


logger = logger.bind(module_name=__name__)
logger.add(f'{logs_path}{__name__}.log', format='{time} {level} {message}', level='INFO', mode='w', enqueue=True)
print(__name__)

class DataValidator:
    """Класс для валидации данных"""

    @staticmethod
    def validate_address(address: int) -> None:
        if not (1 <= address <= 512):
            raise ValueError('Допустимый диапазон значений для адреса: 1-512')

    @staticmethod
    def validate_value(value: int) -> None:
        if not (0 <= value <= 255):
            raise ValueError('Допустимый диапазон значений: 0-255')

    @staticmethod
    def validate(values: Dict[int, int]) -> None:
        for key, val in values.items():
            DataValidator.validate_address(key)
            DataValidator.validate_value(val)


class CheckData(DataValidator):
    """Класс для обработки данных из виджета и отправки данных, от формы виджета требуется
    только создать экземпляр класса и использовать метод send"""

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
            self.buffer = Buffer(self.universe, self.subnet, self.net)
            self.socket = SocketSend()
            self.p = Process(target=self.socket.send, args=(self.buffer.buffer,))
            self.__pass = False

    def send(self, values: Dict[int, int]) -> Optional[str]:
        try:
            logger.info(f'Отправка данных с виджета {values}, u/s/n: {self.universe, self.subnet, self.net}')
            self.validate(values)
            packet = self.buffer.get_packet()
            if packet:
                PackerRebuild(packet, values, (self.universe, self.subnet, self.net)).rebuild()
            else:
                PacketBuild(values, self.universe, self.subnet, self.net).build()
            if not self.p.is_alive():
                self.p.start()
        except ValueError as er:
            logger.exception(f'Ошибка валидации данных: {er}')
            return 'Ошибка: Некорректные значения'
