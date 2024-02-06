import socket
import time

from config.secret import port, ip_address
from loguru import logger


class SocketSend:
    """send - отпрвка данных в сокет
       close - закрываем socket
       single_send - метод для отладки, если необходимо протестировать отправку пакета"""

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__socket = self.__bind()

    @staticmethod
    def __bind():
        try:
            __socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            __socket.bind(('', int(port)))
            __socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except OSError as er:
            logger.exception(f'Ошибка сокета {er}')
            __socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            __socket.close()
            __socket.bind(('', int(port)))
            __socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return __socket

    def send(self, shared_buffer: dict):
        logger.info('Идет процесс отправки пакетов')
        while True:
            for packet in shared_buffer.values():
                try:
                    self.__socket.sendto(packet, (ip_address, port))
                    logger.debug(f'Отправка пакета {packet} в сеть {ip_address, port}')
                    time.sleep(0.2)
                except Exception as er:
                    logger.exception(f'Ошибка отправки пакета: {er}')

    def close(self):
        self.__socket.close()
        logger.warning(f'Сокет закрылся')

    def single_send(self, packet: bytearray) -> None:
        try:
            with self.__socket as sock:
                sock.sendto(packet, (ip_address, port))
                logger.debug(f'Отправка пакета {packet} в сеть {ip_address, port}')
        except Exception as er:
            logger.exception(f'Ошибка отправки пакета: {er}')
