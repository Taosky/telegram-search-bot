# coding: utf-8
from telegram.ext import CommandHandler
import config
from database import get_document
from utils import auto_delete


@auto_delete
def locate_message(bot, update, args):
    if config.ADMIN:
        prev_msg_id = update.message.message_id
        prev_msg_chat_id = update.message.chat_id
        bot.delete_message(chat_id=prev_msg_chat_id, message_id=prev_msg_id)

    if args and args[0].isdigit():
        msg_id = int(args[0])
    else:
        return

    message = get_document(msg_id)

    sent_message = bot.send_message(chat_id=update.message.chat_id, text=message['text'], disable_notification=True,
                                    reply_to_message_id=msg_id)
    return sent_message


handler = CommandHandler('locate', locate_message, pass_args=True)
