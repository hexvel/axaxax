import re

from vkbottle import API, AiohttpClient
from vkbottle.user import Message


class Vars:
    USERS = {}


async def send_message(
    message: Message,
    text: None | str = None,
    attachments: None | list = None,
    reply_to: None | int = None,
):
    """Отправка сообщения"""
    try:
        await message.ctx_api.messages.send(
            peer_id=message.peer_id,
            message=text,
            attachment=attachments,
            reply_to=reply_to,
            random_id=0,
        )
    except Exception:
        await message.ctx_api.messages.delete(
            peer_id=message.peer_id, message_ids=message.id, delete_for_all=1
        )


async def edit_message(
    message: Message,
    text: None | str = None,
    attachments: None | list = None,
    reply_to: None | int = None,
):
    """Редактирование сообщения"""
    try:
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            keep_forward_messages=True,
            message=text,
            attachment=attachments,
        )
    except Exception:
        await message.ctx_api.messages.delete(
            peer_id=message.peer_id, message_ids=message.id, delete_for_all=1
        )
        await send_message(message, attachments, reply_to)


async def search_user_id(event: Message) -> int:
    """Поиск идентификатора пользователя"""
    if event.reply_message:
        user_id = event.reply_message.from_id
    elif len(event.text.split(maxsplit=2)) < 3:
        user_id = event.from_id
    else:
        user_id = int(re.findall(r"\d+", event.text)[0])

    return user_id


async def search_group_id(event: Message):
    """Поиск идентификатора группы"""
    match = re.match(r"\[(club|public)(\d+)\|(.*)]", event.text)
    if match:
        group_id = int(match.group(2))
    else:
        group_id = None

    return group_id


async def check_token(token: str) -> bool:
    try:
        api = API(token=token, http_client=AiohttpClient())
        apps = await api.apps.get()
        return True if apps.items[0].id in [6121396] else False
    except Exception:
        return False
    finally:
        await api.http_client.close()


async def get_user_name(api: API, user_id: int) -> str:
    user = await api.users.get(user_ids=[user_id], name_case="gen")
    return user[0].first_name + " " + user[0].last_name if user else "Unknown"
