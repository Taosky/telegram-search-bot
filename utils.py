import re
from threading import Thread
import functools
import gettext
import time
import json
import os

CONFIG_FILE = './config/.config.json'

USERBOT_CHAT_MEMBERS_FILE = '.userbot_chat_members'
USERBOT_ADMIN_FILE = '.userbot_admin'

HISTORY_GROUPS_FILE = '.hisory_groups'


def get_text_func():
    # Init i18n func
    gettext.bindtextdomain('bot', 'locale')
    gettext.textdomain('bot')
    _ = gettext.gettext
    return _

def delay_delete(bot, chat_id, message_id):
    time.sleep(60)
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
    if not os.path.exists(CONFIG_FILE):
        return None
    f = open(CONFIG_FILE)
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


def load_chat_members():
    if not os.path.exists(USERBOT_CHAT_MEMBERS_FILE):
        with open(USERBOT_CHAT_MEMBERS_FILE, 'w') as f:
            json.dump({}, f)

    with open(USERBOT_CHAT_MEMBERS_FILE, 'r') as f:
        chat_members = json.load(f)
    return chat_members


def write_chat_members(chat_members):
    with open(USERBOT_CHAT_MEMBERS_FILE, 'w') as f:
        json.dump(chat_members, f)


def get_filter_chats(user_id):
    filter_chats = []
    chat_members = load_chat_members()
    for chat_id in chat_members:
        if user_id in chat_members[chat_id]['members']:
            filter_chats.append((int(chat_id),chat_members[chat_id]['title']))
    return filter_chats


def is_userbot_mode():
    env = os.getenv("USER_BOT")
    if not env:
        return False
    return os.getenv("USER_BOT")=="1"


def update_userbot_admin_id(user_id):
    current_id = -1
    if os.path.exists(USERBOT_ADMIN_FILE):
        with open(USERBOT_ADMIN_FILE) as f:
            current_id = int(f.read().strip())

    if current_id != user_id:
        with open(USERBOT_ADMIN_FILE, 'w') as f:
            f.write(str(user_id))


def read_userbot_admin_id():
    with open(USERBOT_ADMIN_FILE) as f:
        current_id = int(f.read().strip())
    return current_id


def group_history_is_fetched(group_id):
    if not os.path.exists(HISTORY_GROUPS_FILE):
        return False
    with open(HISTORY_GROUPS_FILE) as f:
        group_ids = [line.strip() for line in f.readlines()]
        if str(group_id) in group_ids:
            return True
        return False


def write_history_groups(group_id):
    if not os.path.exists(HISTORY_GROUPS_FILE):
        with open(HISTORY_GROUPS_FILE,'w') as f:
            f.write(str(group_id) + '\n')
        return        
    with open(HISTORY_GROUPS_FILE) as f:
        group_ids = [line.strip() for line in f.readlines()]
        if str(group_id) not in group_ids:
            group_ids.append(str(group_id))
    with open(HISTORY_GROUPS_FILE,'w') as f:
        for groud_id_ in group_ids:
            f.write(groud_id_ + '\n')


def remove_history_group(group_id):
    if not os.path.exists(HISTORY_GROUPS_FILE):
        return        
    with open(HISTORY_GROUPS_FILE) as f:
        group_ids = [line.strip() for line in f.readlines()]
        if str(group_id) not in group_ids:
            return
    group_ids.remove(str(group_id))
    with open(HISTORY_GROUPS_FILE,'w') as f:
        for groud_id_ in group_ids:
            f.write(groud_id_ + '\n')