from loguru import logger

from database.models.user import User


class UserManager:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.user = None

    async def initialize(self):
        self.user = await User.get(user_id=self.user_id)
        logger.success(
            "Manager for user {} successfully initialized", self.user.user_id
        )
