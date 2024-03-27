import telegram
from utils import get_text_func

_ = get_text_func()

def set_bot_commands(context: telegram.ext.CallbackContext):
    commands = [
        ('help', _('get search help')),
        ('chat_id', _('get current chat id (group or user)')),
        ('start', _('start bot in current group ( userbot mode need `start <group_id>`)')),
        ('stop', _('stop bot in current group (userbot mode need `stop <group_id>`)')),
        ('delete', _('delete saved messages if stopped  (userbot mode need `stop <group_id>`)'))
    ]

    context.bot.set_my_commands(commands)
