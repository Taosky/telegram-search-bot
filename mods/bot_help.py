from telegram.ext import CommandHandler
from config import BOT_ID

from utils import auto_delete, delete_prev_message


@auto_delete
def get_help(bot, update):
    delete_prev_message(bot, update)
    help_text = '*Search message:* Enter `@%s {keyword} {page}`. (ex: @whatever_repeat_bot china 2)' % BOT_ID
    sent_message = bot.send_message(update.message.chat_id, text=help_text, disable_notification=True,
                                    parse_mode='markdown')
    return sent_message


handler = CommandHandler('help', get_help)
