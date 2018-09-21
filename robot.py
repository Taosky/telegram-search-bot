# coding: utf-8
import functools
import math
import time
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackQueryHandler
import config
import logging
from database import insert_db, search_db, get_document

updater = Updater(token=config.TOKEN)
dispatcher = updater.dispatcher
job = updater.job_queue

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def delay_delete(bot, chat_id, message_id):
    time.sleep(config.SENT_DELETE_DELAY)
    bot.delete_message(chat_id=chat_id, message_id=message_id)


def auto_delete(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        bot = args[0]
        sent_message = fn(*args, **kw)
        Thread(target=delay_delete, args=[bot, sent_message.chat_id, sent_message.message_id]).start()
        return sent_message

    return wrapper


@auto_delete
def get_chat_id(bot, update):
    sent_message = bot.send_message(chat_id=update.message.chat_id,
                                    text="This chat id: {}".format(update.message.chat_id))
    return sent_message


def store_message(bot, update):
    if update.message.chat_id == config.GROUP_ID:
        insert_db(update.message.message_id, update.message.from_user.full_name, update.message.text,
                  update.message.date.strftime("%Y-%m-%d %H:%M:%S"))


@auto_delete
def search_message(bot, update, args):
    keyword = args[0]
    page = int(args[1]) if len(args) > 1 else 1

    messages, count = search_db(keyword, page)
    if count == 0:
        bot.send_message(chat_id=config.GROUP_ID,
                         text='No search result.', disable_notification=True)
        return
    elif count == -1:
        bot.send_message(chat_id=config.GROUP_ID,
                         text='Search Error.', disable_notification=True)
        return

    # result button list
    button_list = [
        InlineKeyboardButton(
            '{} | {} | {}'.format(message['text'][:12] + '...' if len(message['text']) > 12 else message['text'],
                                  message['user'], message['time'].strftime("%Y-%m-%d")),
            callback_data='/locate {}'.format(message['id'])) for message in messages
    ]
    prev_button = InlineKeyboardButton('Prev Page',
                                       callback_data='/search {} {}'.format(keyword, page - 1)) if page > 1 else None
    next_button = InlineKeyboardButton('Next Page', callback_data='/search {} {}'
                                       .format(keyword, page + 1)) if page * config.SEARCH_PAGE_SIZE < count else None
    pager = []
    if prev_button:
        pager.append(prev_button)
    if next_button:
        pager.append(next_button)
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1, footer_buttons=pager))

    # send search result
    sent_message = bot.send_message(chat_id=config.GROUP_ID,
                                    text='Page {} of {} \t Total {} messages.'.format(page, math.ceil(
                                        count / config.SEARCH_PAGE_SIZE), count),
                                    reply_markup=reply_markup)
    return sent_message


@auto_delete
def locate_message(bot, update):
    query = update.callback_query
    args = query.data.split(' ')[1:]
    # change page
    if query.data.startswith('/search'):
        search_message(bot, query, args=args)

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


@auto_delete
def show_deleted_message(bot, update):
    text = 'Message has been deleted!'
    sent_message = bot.send_message(chat_id=config.GROUP_ID, text=text, disable_notification=True)
    return sent_message


def error_callback(bot, update, error):
    try:
        raise error
    except BadRequest:
        show_deleted_message(bot, update)


if __name__ == '__main__':
    # get chat id
    dispatcher.add_handler(CommandHandler('chatid', get_chat_id))
    # store messages in database
    dispatcher.add_handler(MessageHandler(Filters.text, store_message))
    # search message
    dispatcher.add_handler(CommandHandler('search', search_message, pass_args=True))
    # search callback to locate message
    dispatcher.add_handler(CallbackQueryHandler(locate_message))

    dispatcher.add_error_handler(error_callback)
    updater.start_polling()

    # updater.start_webhook(listen='127.0.0.1', port=8321, url_path=TOKEN)
    # updater.bot.set_webhook('https://telegram.xxx.xx/' + TOKEN)
