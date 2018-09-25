from telegram.ext import CommandHandler
from config import BOT_ID

from utils import auto_delete, delete_prev_message


@auto_delete
def get_help(bot, update):
    delete_prev_message(bot, update)
    help_text = '*搜索消息:* 输入 `@%s {keyword} {page}`. (例如: @%s china 2)' % (BOT_ID, BOT_ID)
    sent_message = bot.send_message(update.message.chat_id, text=help_text, disable_notification=True,
                                    parse_mode='markdown')
    return sent_message


handler = CommandHandler('help', get_help)
