# coding: utf-8
import logging
import math
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from config import SEARCH_PAGE_SIZE, GROUP_ID
from database import search_db
import re


def inline_caps(bot, update):
    from_user_id = update.inline_query.from_user.id
    try:
        bot.get_chat_member(chat_id=GROUP_ID, user_id=from_user_id)
    except:
        return

    query = update.inline_query.query
    if not query:
        return
    re_match = re.match('(.*) (\d+)', query)
    if re_match:
        keyword, page = re_match.group(1), int(re_match.group(2))
    else:
        keyword, page = query, 1
    messages, count = search_db(keyword, page)
    results = [InlineQueryResultArticle(
        id='info',
        title='Total:{}. Page {} of {}'.format(count, page, math.ceil(count / SEARCH_PAGE_SIZE)),
        input_message_content=InputTextMessageContent(
            'Enter `@{bot name} {keyword} {page}` to *choose page*.',
            parse_mode='markdown')
    )]
    for message in messages:
        results.append(
            InlineQueryResultArticle(
                id=message['id'],
                title='{}'.format(message['text'][:100]),
                description=message['time'].strftime("%Y-%m-%d").ljust(40) + message['user'],
                input_message_content=InputTextMessageContent('/locate {}'.format(message['id']))
            )
        )
        bot.answer_inline_query(update.inline_query.id, results)


handler = InlineQueryHandler(inline_caps)
