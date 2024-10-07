from vkbottle.user import UserLabeler, Message

labeler = UserLabeler()


@labeler.message(text="тест")
async def test_handler(message: Message):
    await message.answer("хуй")
