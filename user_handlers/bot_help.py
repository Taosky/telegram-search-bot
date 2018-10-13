from telegram.ext import CommandHandler
from config import BOT_ID

from utils import auto_delete, delete_prev_message


@auto_delete
def get_help(bot, update):
    delete_prev_message(bot, update)
    help_text = '*搜索消息:*\n  `@%s {keyword} {page}`。\n例如: "@%s 星星 2" 搜索"星星"并翻到第二页; \n不输入页码默认第一页；\n AT后不输入显示的是全部记录，此时输入 ' \
                '"\* {page}"进行翻页\n\n' % (
                    BOT_ID, BOT_ID)
    sent_message = bot.send_message(update.message.chat_id, text=help_text, disable_notification=True,
                                    parse_mode='markdown')
    return sent_message


handler = CommandHandler('help', get_help)
