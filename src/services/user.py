import asyncio

from loguru import logger
from manager.user import UserManager
from actions.user import user_labeler
from base.service import UserServiceBase
from vkbottle import API, AiohttpClient
from vkbottle.user import User as Session
from vkbottle.tools import LoopWrapper

from database.models.user import User


class UserService(UserServiceBase):
    def __init__(self, user: User) -> None:
        super().__init__(user)
        self.loop_wrapper = LoopWrapper(loop=asyncio.get_event_loop())

    async def initialize_api(self) -> None:
        api = API(self.user.token, http_client=AiohttpClient())
        self.session = Session(
            api=api, labeler=user_labeler, loop_wrapper=self.loop_wrapper
        )
        self.polling = UserPolling(self.session, self.loop_wrapper)
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
        self.polling.start_user_session()

    async def restart_user_session(self) -> None:
        if not self.polling:
            logger.error(f"Polling is not initialized for user: {self.user_id}")
            return

        self.polling.stop_user_session()
        await self.initialize()
        self.polling.start_user_session()

    def stop_user_session(self) -> None:
        if not self.polling:
            logger.error(f"Polling is not initialized for user: {self.user_id}")
            return

        self.polling.stop_user_session()
        logger.warning("Session of user {} will be stopped", self.user_id)


class UserPolling:
    def __init__(self, session: Session, loop_wrapper: LoopWrapper) -> None:
        self.session = session
        self.loop_wrapper = loop_wrapper

    def start_user_session(self) -> None:
        self.loop_wrapper.add_task(self.session.run_polling())

    def stop_user_session(self) -> None:
        self.session.polling.stop = True
