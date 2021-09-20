# coding: utf-8
import math
import re
from utils import read_config

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from database import User, Message, DBSession
from sqlalchemy import and_

SEARCH_PAGE_SIZE = 25


def pure_str(s):
    reg='</?.+?/?>'
    return re.sub(reg, '', s, count=0)


def search_messages(keywords, page):
    messages = []
    start = (page - 1) * SEARCH_PAGE_SIZE
    stop = page * SEARCH_PAGE_SIZE
    session = DBSession()
    if keywords:
        rule = and_(*[Message.text.like('%' + keyword+ '%') for keyword in keywords])
        count = session.query(Message).filter(rule).count()
        query = session.query(Message).filter(rule).order_by(
            Message.date.desc()).slice(start, stop)
    else:
        count = session.query(Message).count()
        query = session.query(Message).filter().order_by(Message.date.desc()).slice(start, stop)
    for message in query.all():
        user = session.query(User).filter_by(id=message.from_id).one()
        user_fullname = user.fullname
        if message.type != 'text':
            msg_text = '[{}]'.format(message.type)
        else:
            msg_text = message.text
        messages.append(
            {'id': message.id, 'link': message.link, 'text': msg_text, 'date': message.date, 'user': user_fullname,
             'type': message.type})

    session.close()
    return messages, count


def inline_caps(update, context):
    from_user_id = update.inline_query.from_user.id
    # Check user permission
    try:
        config = read_config()
        context.bot.get_chat_member(chat_id=config['group_id'], user_id=from_user_id)
    except:
        return

    query = update.inline_query.query
    # Get recent messages
    if not query:
        keywords, page = None, 1

    elif re.match(' *\* +(\d+)', query):
        keywords, page = None, int(re.match('\* +(\d+)', query).group(1))
    # Search messages
    else:
        keywords = [word for word in query.split(" ")]
        if keywords[-1].isdigit():
            page = int(keywords[-1])
            keywords.pop()
        else:
            page = 1
    messages, count = search_messages(keywords, page)
    results = [InlineQueryResultArticle(
        id='info',
        title='Total:{}. Page {} of {}'.format(count, page, math.ceil(count / SEARCH_PAGE_SIZE)),
        input_message_content=InputTextMessageContent('/help')
    )]
    for message in messages:
        results.append(
            InlineQueryResultArticle(
                id=message['id'],
                title='{}'.format(message['text'][:100]),
                description=message['date'].strftime("%Y-%m-%d").ljust(40) + message['user'],
                input_message_content=InputTextMessageContent(
                    '{}<a href="{}">「From {}」</a>'.format(pure_str(message['text']), message['link'], message['user']),parse_mode='html'
                    ) if
                message['link'] != '' and message['type'] == 'text' or message['id'] < 0 else InputTextMessageContent(
                    '/locate {}'.format(message['id']))
            )
        )
    context.bot.answer_inline_query(update.inline_query.id, results)


handler = InlineQueryHandler(inline_caps)
