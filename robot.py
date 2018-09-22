# coding: utf-8
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackQueryHandler
import config
import logging
from database import insert_db, search_db, get_document
from utils import auto_delete, build_menu

updater = Updater(token=config.TOKEN)
dispatcher = updater.dispatcher
job = updater.job_queue

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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


@auto_delete
def show_deleted_message(bot, update):
    text = 'Message has been deleted!'
    sent_message = bot.send_message(chat_id=update.message.chat_id, text=text, disable_notification=True)
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

    # polling
    # updater.start_polling()

    # Webhook
    updater.start_webhook(listen='127.0.0.1', port=8321, url_path='TOKEN')
    updater.bot.set_webhook(url='https://telegram.xxx.xx/TOKEN')
    updater.idle()
