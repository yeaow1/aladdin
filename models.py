from tortoise.models import Model
from tortoise import fields


class GuildSettings(Model):
    guild_id = fields.BigIntField(pk=True, unique=True)
    guild_name = fields.TextField()
    guild_prefix = fields.TextField(default=">")
    welcome_enabled = fields.BooleanField(
        default=False, description="Set true/false to enable the welcome message"
    )
    leave_enabled = fields.BooleanField(
        default=False, description="Set true/false to enable the leave message"
    )


class WelcomeSettings(Model):
    guild_id = fields.BigIntField(pk=True, unique=True)
    channel_id = fields.BigIntField(unique=True)
    welcome_message = fields.TextField()


class LeaveSettings(Model):
    guild_id = fields.BigIntField(pk=True, unique=True)
    channel_id = fields.BigIntField(unique=True)
    leave_message = fields.TextField()

class Levels(Model):
    user_id = fields.BigIntField()
    guild_id = fields.BigIntField()
    level = fields.IntField()
    xp = fields.BigIntField()
