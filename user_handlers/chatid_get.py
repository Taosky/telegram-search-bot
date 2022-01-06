# coding: utf-8
from telegram.ext import CommandHandler
from utils import auto_delete
import logging


@auto_delete
def get_chat_id(update, context):
    sent_message = context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_chat.id))
    return sent_message


# Command: get chat id
handler = CommandHandler('chat_id', get_chat_id)
