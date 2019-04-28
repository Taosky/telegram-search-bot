import re
from threading import Thread
import functools
import config
import time


def delay_delete(bot, chat_id, message_id):
    time.sleep(config.SENT_DELETE_DELAY)
    bot.delete_message(chat_id=chat_id, message_id=message_id)


def auto_delete(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        bot = args[0]
        sent_message = fn(*args, **kw)
        if sent_message:
            if config.AUTO_DELETE:
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


def delete_prev_message(bot, update):
    if config.ADMIN:
        bot_id = get_bot_id(bot)
        # 检查权限
        if not bot.get_chat_member(config.GROUP_ID, bot_id).can_delete_messages:
            bot.send_message(
                chat_id=config.GROUP_ID,
                text='缺少撤回群员消息权限，如不提供请关闭此选项。',
                disable_notification=True
            )
            return
        if not update.message:
            prev_msg_id = update.callback_query.message.message_id
            prev_msg_chat_id = update.callback_query.message.chat.id
        else:
            prev_msg_id = update.message.message_id
            prev_msg_chat_id = update.message.chat_id

        bot.delete_message(chat_id=prev_msg_chat_id, message_id=prev_msg_id)


def get_bot_user_name(bot):
    return bot.get_me().username


def get_bot_id(bot):
    return bot.get_me().id
