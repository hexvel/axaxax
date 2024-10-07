from loguru import logger


class UserManager:
    def __init__(self, user_id) -> None:
        self.user_id = user_id

    async def initialize(self):
        logger.debug("Init user manager...")
