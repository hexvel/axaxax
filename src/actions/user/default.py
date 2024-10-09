import time
import timeit

from vkbottle.user import Message, UserLabeler

from actions.rules import Commands
from core import Emoji, utils

labeler = UserLabeler()


@labeler.message(Commands(commands=["ping", "пинг"]))
async def ping(message: Message):
    ping_time = time.time() - message.date
    code_ping = timeit.timeit("ping_time", number=1000, globals=locals())
    global_ping = timeit.timeit("import math", number=1000, globals=globals())

    await utils.edit_message(
        message=message,
        text=f"{Emoji.EARTH} Ping: {ping_time:.2f}s | "
        f"{Emoji.SETTINGS} Code ping: {code_ping:.2f}s | "
        f"{Emoji.FLAG} Global ping: {global_ping:.2f}s.",
    )


@labeler.message(Commands(commands=["+др"]))
async def add_friend(message: Message):
    user_id = await utils.search_user_id(message)
    add_friend = await message.ctx_api.friends.add(user_id=user_id)

    if add_friend == 1:
        text = f"{Emoji.OK} [id{user_id}|Пользователю] отправлен запрос на дружбу."
    elif add_friend == 2:
        text = f"{Emoji.OK} Заявка [id{user_id}|пользователя] одобрена."
    elif add_friend == 4:
        text = f"{Emoji.OK} [id{user_id}|Пользователю] отправлен повторный запрос на дружбу."
    else:
        text = (
            f"{Emoji.WARNING} Не удалось добавить [id{user_id}|пользователя] в друзья."
        )

    await utils.edit_message(message=message, text=text)


@labeler.message(Commands(commands=["-др"]))
async def delete_friend(message: Message):
    user_id = await utils.search_user_id(message)

    delete_friend = await message.ctx_api.friends.delete(user_id=user_id)

    if bool(delete_friend.success):
        text = f"{Emoji.OK} [id{user_id}|Пользователю] удален из друзей."
    elif bool(delete_friend.out_request_deleted):
        text = f"{Emoji.OK} Отменяю исходящюю заявку [id{user_id}|пользователю]."
    elif bool(delete_friend.in_request_deleted):
        text = f"{Emoji.OK} Отменяю входящую заявку [id{user_id}|пользователю]."
    else:
        text = (
            f"{Emoji.WARNING} Не удалось удалить [id{user_id}|пользователя] из друзей."
        )

    await utils.edit_message(message=message, text=text)


@labeler.message(Commands(commands=["+чс"]))
async def add_blacklist(message: Message):
    user_id = await utils.search_user_id(message)
    blacklist = await message.ctx_api.account.ban(owner_id=user_id)

    if bool(blacklist):
        text = f"{Emoji.OK} [id{user_id}|Пользователь] заблокирован."
    else:
        text = f"{Emoji.WARNING} Не удалось заблокировать [id{user_id}|пользователя]."

    await utils.edit_message(message=message, text=text)


@labeler.message(Commands(commands=["-чс"]))
async def delete_blacklist(message: Message):
    user_id = await utils.search_user_id(message)
    unblacklist = await message.ctx_api.account.unban(owner_id=user_id)

    if bool(unblacklist):
        text = f"{Emoji.OK} [id{user_id}|Пользователь] разблокирован."
    else:
        text = f"{Emoji.WARNING} Не удалось разблокировать [id{user_id}|пользователя]."

    await utils.edit_message(message=message, text=text)
