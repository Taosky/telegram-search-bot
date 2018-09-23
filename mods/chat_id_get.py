# coding: utf-8
from telegram.ext import CommandHandler
from utils import auto_delete


@auto_delete
def get_chat_id(bot, update):
    sent_message = bot.send_message(chat_id=update.message.chat_id,
                                    text="This chat id: {}".format(update.message.chat_id))
    return sent_message


# command to get chat id
handler = CommandHandler('chatid', get_chat_id)
