# coding: utf-8
from telegram.ext import CommandHandler
from utils import auto_delete, get_bot_user_name
import logging


@auto_delete
def get_help(update, context):
    bot_user_name = get_bot_user_name(context.bot)
    help_text = '*搜索消息(支持多个关键词):*\n  `@%s {keyword} {page}`。\n例如: "@%s 今天 我 2" 搜索包含"今天"、"我"的消息并翻到第二页; \n不输入页码默认第一页；\n AT后不输入显示的是全部记录，此时输入 ' \
                '"\* {page}"进行翻页\n\n' % (
                    bot_user_name, bot_user_name)
    sent_message = context.bot.send_message(update.effective_chat.id, text=help_text, disable_notification=True,
                                    parse_mode='markdown')
    return sent_message


handler = CommandHandler('help', get_help)
