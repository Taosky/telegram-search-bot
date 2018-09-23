# coding: utf-8
from telegram.ext import MessageHandler, Filters
import config
from database import insert_db


def store_message(bot, update):
    if update.message.chat_id == config.GROUP_ID and not update.message.text.endswith('\n_'):
        insert_db(update.message.message_id, update.message.from_user.full_name, update.message.text,
                  update.message.date.strftime("%Y-%m-%d %H:%M:%S"))


handler = MessageHandler(Filters.text, store_message)
