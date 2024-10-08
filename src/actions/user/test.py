from vkbottle.user import UserLabeler, Message

labeler = UserLabeler()


@labeler.message(text="тест")
async def test_handler(message: Message):
    message.ctx_api.data.stop_user_session()
