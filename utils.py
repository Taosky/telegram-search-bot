import re
from threading import Thread
import functools
import time
import json
import os


def delay_delete(bot, chat_id, message_id):
    time.sleep(30)
    bot.delete_message(chat_id=chat_id, message_id=message_id)


def auto_delete(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        bot = args[1].bot
        sent_message = fn(*args, **kw)
        if sent_message:
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


# calculate num of non-ascii characters
def len_non_ascii(data):
    temp = re.findall('[^a-zA-Z0-9.]+', data)
    count = 0
    for i in temp:
        count += len(i)
    return count


def get_bot_user_name(bot):
    return bot.get_me().username


def get_bot_id(bot):
    return bot.get_me().id


def read_config():
    if not os.path.exists('./config/.config.json'):
        return None
    f = open('./config/.config.json')
    config_dict = json.load(f)
    f.close()
    return config_dict


def check_control_permission(from_user_id):
    try:
        config = read_config()
        if config['enable']:
            if from_user_id in config['group_admins']:
                return True
            else:
                return False
        else:
            return None
    except:
        return None
