import asyncio

from loguru import logger
from manager.user import UserManager
from actions.user import user_labeler
from base.service import UserServiceBase
from vkbottle import API, AiohttpClient
from vkbottle.user import User as Session

from database.models.user import User


class UserService(UserServiceBase):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    async def initialize_api(self) -> None:
        api = API(self.user.token, http_client=AiohttpClient())
        self.session = Session(api=api, labeler=user_labeler)
        self.polling = UserPolling(self.session)
        setattr(self.session.api, "data", self)

    async def initialize_managers(self) -> None:
        self.manager = UserManager(self.user_id)

        await asyncio.gather(
            self.manager.initialize(),
        )

    # async def initialize_background_tasks(self) -> None:
    #     for i, task in enumerate(background_tasks, 1):
    #         logger.debug(
    #             "Initializing background task for user {} with id {}", self.user_id, i
    #         )
    #         asyncio.create_task(task(self.session.api, self.script_manager))

    async def start_user_session(self) -> None:
        if self.polling:
            logger.error(f"Polling already initialized for user: {self.user_id}")
            return

        await self.initialize()
        await self.polling.start_user_session()

    async def restart_user_session(self) -> None:
        if not self.polling:
            logger.error(f"Polling is not initialized for user: {self.user_id}")
            return

        await self.polling.restart_user_session()

    async def stop_user_session(self) -> None:
        if not self.polling:
            logger.error(f"Polling is not initialized for user: {self.user_id}")
            return

        await self.polling.stop_user_session()


class UserPolling:
    def __init__(self, session) -> None:
        self.session = session
        self.loop = asyncio.get_event_loop()

    async def start_user_session(self) -> asyncio.Task:
        self.loop = asyncio.create_task(self.session.run_polling(), name=f"user")

    async def restart_user_session(self) -> asyncio.Task:
        await self.stop_user_session()
        await self.start_user_session()

    async def stop_user_session(self):
        self.loop.cancel()
