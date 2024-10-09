from loguru import logger

from database.models.user import User


class UserManager:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.user = None

        """Модели пользователя"""
        self.balance = None
        self.token = None
        self.vkme_token = None
        self.username = None
        self.profile_photo = None
        self.prefix_commands = None
        self.prefix_scripts = None

    async def initialize(self):
        self.user = await User.get(user_id=self.user_id)
        self.balance = self.user.balance
        self.token = self.user.token
        self.vkme_token = self.user.vkme_token
        self.username = self.user.username
        self.profile_photo = self.user.profile_photo
        self.prefix_commands = self.user.prefix_commands
        self.prefix_scripts = self.user.prefix_scripts

        logger.success(
            "Manager for user {} successfully initialized", self.user.user_id
        )

    def get_prefix_commands(self):
        return self.prefix_commands
