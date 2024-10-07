from loguru import logger
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message()
async def test_command(message: Message):
    logger.debug(message.text)
