# coding: utf-8
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import search_db, get_document
from utils import auto_delete, build_menu
from telegram.ext import CommandHandler
import config


@auto_delete
def search_message(bot, update=None, args=None):
    if not args:
        args = ['search', '1']
    elif len(args) == 1:
        args.append('1')
    # page changing has no update
    chat_id = update.message.chat_id if update else args[2]
    # hide mode disable group call
    if config.HIDE_MODE and config.GROUP_ID == chat_id:
        return
    keyword = args[0]
    page = int(args[1])

    messages, count = search_db(keyword, page)
    if count == 0:
        sent_message = bot.send_message(chat_id=chat_id,
                                        text='No search result.', disable_notification=True)
        return sent_message
    elif count == -1:
        sent_message = bot.send_message(chat_id=chat_id,
                                        text='Search Error.', disable_notification=True)
        return sent_message

    # result button list
    button_list = [
        InlineKeyboardButton(
            '{} | {} | {}'.format(message['text'][:12] + '...' if len(message['text']) > 12 else message['text'],
                                  message['user'], message['time'].strftime("%Y-%m-%d")),
            callback_data='/locate {}'.format(message['id'])) for message in messages
    ]
    prev_button = InlineKeyboardButton('Prev Page',
                                       callback_data='/search {} {} {}'.format(keyword, page - 1,
                                                                               chat_id)) if page > 1 else None
    next_button = InlineKeyboardButton('Next Page', callback_data='/search {} {} {}'
                                       .format(keyword, page + 1,
                                               chat_id)) if page * config.SEARCH_PAGE_SIZE < count else None
    pager = []
    if prev_button:
        pager.append(prev_button)
    if next_button:
        pager.append(next_button)
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1, footer_buttons=pager))

    # send search result
    sent_message = bot.send_message(chat_id=chat_id,
                                    text='Page {} of {} \t Total {} messages.'.format(page, math.ceil(
                                        count / config.SEARCH_PAGE_SIZE), count),
                                    reply_markup=reply_markup)
    return sent_message


handler = CommandHandler('search', search_message, pass_args=True)
