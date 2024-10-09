from typing import Optional

from pydantic import BaseModel

from manager.user import UserManager


class UserModel(BaseModel):
    manager: Optional[UserManager] = None

    class Config:
        arbitrary_types_allowed = True
