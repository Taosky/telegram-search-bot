# coding: utf-8
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackQueryHandler
import config
import logging
from tieba import get_update_post
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


def get_chat_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="This chat id: {}".format(update.message.chat_id))


def store_message(bot, update):
    if update.message.chat_id == config.GROUP_ID:
        insert_db(update.message.message_id, update.message.from_user.full_name, update.message.text,
                  update.message.date.strftime("%Y-%m-%d %H:%M:%S"))


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
    bot.send_message(chat_id=config.GROUP_ID,
                     text='Page {} of {} \t Total {} messages.'.format(page, math.ceil(count / config.SEARCH_PAGE_SIZE),
                                                                       count),
                     reply_markup=reply_markup)


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
            text = 'At: {}\nContent: "{}"'.format(target_message['time'], target_message['text'])
        else:
            text = 'Database Error'
        bot.send_message(chat_id=config.GROUP_ID, reply_to_message_id=msg_id,
                         text=text, disable_notification=True)


def tieba_monitor(bot, job):
    for post in get_update_post():
        bot.send_message(chat_id=config.GROUP_ID,
                         text='"{}" 发布帖子: "{}".\n{}'.format(post['author'], post['title'], post['url']))


if __name__ == '__main__':
    # get chat id
    dispatcher.add_handler(CommandHandler('chatid', get_chat_id))
    # store messages in database
    dispatcher.add_handler(MessageHandler(Filters.text, store_message))
    # search message
    dispatcher.add_handler(CommandHandler('search', search_message, pass_args=True))
    # search callback to locate message
    dispatcher.add_handler(CallbackQueryHandler(locate_message))
    # 贴吧更新提醒
    job.run_repeating(tieba_monitor, interval=60, first=0)
    updater.start_polling()

    # updater.start_webhook(listen='127.0.0.1', port=8321, url_path=TOKEN)
    # updater.bot.set_webhook('https://api.mou.science/telegram/' + TOKEN)
