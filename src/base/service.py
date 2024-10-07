from abc import ABC, abstractmethod
from loguru import logger

from database.models.user import User


class UserServiceBase(ABC):
    def __init__(self, user: User) -> None:
        self.user = user
        self.user_id = user.user_id

        self.polling = None
        self.session = None
        self.manager = None
        self.script_manager = None

    def __getattr__(self, name):
        # Делегирование методов для доступа к API
        return getattr(self.service, name)

    @abstractmethod
    async def initialize_api(self) -> None:
        """Инициализация API для работы с пользователем."""
        pass

    @abstractmethod
    async def initialize_managers(self) -> None:
        """Инициализация менеджеров для работы с пользователем."""
        pass

    # @abstractmethod
    # async def initialize_background_tasks(self) -> None:
    #     """Инициализация фоновых задач."""
    #     pass

    @abstractmethod
    async def start_user_session(self) -> None:
        """Запуск сессии пользователя"""
        pass

    @abstractmethod
    async def restart_user_session(self) -> None:
        """Перезапуск сессий пользователей"""
        pass

    @abstractmethod
    async def stop_user_session(self) -> None:
        """Остановка сессии пользователей"""
        pass

    async def initialize(self) -> None:
        logger.debug("Initializing service for user {}", self.user_id)

        # Инициализация API
        await self.initialize_api()

        # Инициализация менеджеров
        await self.initialize_managers()

        # Инициализация фоновых задач
        # await self.initialize_background_tasks()

        logger.success("User service successfully initialized")
