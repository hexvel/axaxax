from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.IntField()
    balance = fields.IntField(default=0)
    token = fields.TextField(null=True)
    vkme_token = fields.TextField(null=True)
    username = fields.TextField(default="Unknown")
    profile_photo = fields.TextField(null=True)
    prefix_commands = fields.TextField(default=".д")
    prefix_scripts = fields.TextField(default=".скр")
