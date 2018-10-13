# coding: utf-8
from telegram.ext import CommandHandler
from database import get_document
from utils import auto_delete, delete_prev_message


@auto_delete
def locate_message(bot, update, args):
    delete_prev_message(bot, update)
    if args and args[0].isdigit():
        msg_id = int(args[0])
    else:
        return

    message = get_document(msg_id)

    sent_message = bot.send_message(chat_id=update.message.chat_id, text=message['text'], disable_notification=True,
                                    reply_to_message_id=msg_id)
    return sent_message


handler = CommandHandler('locate', locate_message, pass_args=True)
