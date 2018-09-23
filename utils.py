import imp
import os

from telegram.error import BadRequest
from threading import Thread
import functools
import config
import time


def package_contents(path_name):
    return set([os.path.splitext(module)[0] for module in os.listdir(path_name) if module.endswith('.py')])


def delay_delete(bot, chat_id, message_id):
    time.sleep(config.SENT_DELETE_DELAY)
    bot.delete_message(chat_id=chat_id, message_id=message_id)


def auto_delete(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        bot = args[0]
        sent_message = fn(*args, **kw)
        if sent_message:
            if not config.HIDE_MODE or fn.__name__ == 'locate_message':
                Thread(target=delay_delete, args=[bot, sent_message.chat_id, sent_message.message_id]).start()
        return sent_message

    return wrapper


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


@auto_delete
def send_error_message(bot, update, text):
    sent_message = bot.send_message(chat_id=update.message.chat_id, text=text, disable_notification=True)
    return sent_message


def error_callback(bot, update, error):
    try:
        raise error
    except BadRequest:
        send_error_message(bot, update)
