from typing import List, Optional, Union

from vkbottle import ABCRule
from vkbottle.user import Message

from models.user import UserModel


class Commands(ABCRule):
    def __init__(
        self,
        prefix: Optional[str] = ".д",
        commands: Union[str, List[str]] = list(),
    ):
        """
        Initialize the class with the given prefix, commands, and rank.

        Args:
            prefix (Optional[str]): The prefix for the commands.
            commands (Union[str, List[str]]): The command or list of commands.
            rank (Optional[int], optional): The rank of the commands. Defaults to 1.
        """
        self.prefix = prefix
        self.commands = commands

    async def check(self, message: Message):
        """
        Async function to check the message for valid command and permissions.

        Args:
            message (Message): The message object to be checked.

        Returns:
            bool: True if the command is valid and has the required permissions, False otherwise.
        """
        data: UserModel = message.ctx_api.data

        if not bool(message.out):
            return False
        if not message.text:
            return False

        # TODO: Заготовка для алиасов
        # if message.text.split()[0].lower() in list(data.alias.aliases.keys()):
        #     alias_command = data.alias.get_alias(message.text.split()[0].lower())
        #     message.text = message.text.replace(message.text.split()[0], alias_command)

        command = message.text.split("\n")[0].split()
        if len(command) < 2:
            return False

        if self.prefix == ".д":
            self.prefix = [".д", data.manager.get_prefix_commands()]

        return bool(
            command[0].lower() in self.prefix and command[1].lower() in self.commands
        )


class ToMe(ABCRule):
    async def check(self, message: Message):
        return not bool(message.out)
