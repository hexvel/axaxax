import importlib
from pathlib import Path

from vkbottle.framework.labeler import BaseLabeler
from vkbottle.user import UserLabeler

package_path = Path(__file__).parent
module_files = [
    file.stem for file in package_path.glob("*.py") if file.name != "__init__.py"
]

user_labeler = UserLabeler()
user_labelers: list["BaseLabeler"] = [
    importlib.import_module(f".{module}", __package__).labeler
    for module in module_files
]

for labeler in user_labelers:
    user_labeler.load(labeler)
