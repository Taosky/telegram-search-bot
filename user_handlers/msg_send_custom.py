# coding: utf-8
from telegram.ext import CommandHandler
from utils import delete_prev_message

granted_user_ids = [527716928, ]


# @auto_delete
def send_custom_message(bot, update, args):
    delete_prev_message(bot, update)
    if not args or update.message.from_user.id not in granted_user_ids:
        return

    text = ' '.join(args)

    sent_message = bot.send_message(chat_id=update.message.chat_id, text=text, disable_notification=True)
    return sent_message


handler = CommandHandler('message', send_custom_message, pass_args=True)
