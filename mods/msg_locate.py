# coding: utf-8
from telegram.ext import CallbackQueryHandler

import config
from database import get_document
from mods.msg_search import search_message
from utils import auto_delete


@auto_delete
def locate_message(bot, update):
    query = update.callback_query
    args = query.data.split(' ')[1:]
    # change page
    if query.data.startswith('/search'):
        search_message(bot, args=args)

    # locate message
    elif query.data.startswith('/locate'):
        msg_id = int(args[0])
        target_message = get_document(msg_id)
        if target_message:
            text = 'At: {}\nContent:\n "{}"'.format(target_message['time'], target_message['text'])
        else:
            text = 'Unknown Error!'
        sent_message = bot.send_message(chat_id=config.GROUP_ID, reply_to_message_id=msg_id,
                                        text=text, disable_notification=True)
        return sent_message


handler = CallbackQueryHandler(locate_message)
