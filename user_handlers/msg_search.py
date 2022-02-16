# coding: utf-8
import math
import re
import html
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from database import User, Message, Chat, DBSession
from sqlalchemy import and_

SEARCH_PAGE_SIZE = 25


def search_messages(keywords, page, chat_ids):
    messages = []
    start = (page - 1) * SEARCH_PAGE_SIZE
    stop = page * SEARCH_PAGE_SIZE
    session = DBSession()
    if keywords:
        rule = and_(*[Message.text.like('%' + keyword+ '%') for keyword in keywords])
        count = session.query(Message).filter(rule).count()
        query = session.query(Message).filter(rule)
    else:
        count = session.query(Message).count()
        query = session.query(Message).filter()
    for message in query.order_by(Message.date.desc()).slice(start, stop).all():
        if message.from_chat not in chat_ids:
            count -= 1
            continue
        user = session.query(User).filter_by(id=message.from_id).one()
        chat = session.query(Chat).filter_by(id=message.from_chat).one()
        if not chat.enable:
            count -= 1
            continue
        user_fullname = user.fullname
        chat_title = chat.title
        if message.type != 'text':
            msg_text = '[{}]'.format(message.type)
        else:
            msg_text = message.text
        
        if msg_text == '':
            continue
        messages.append(
            {'id': message.id, 'link': message.link, 'text': msg_text, 'date': message.date, 'user': user_fullname, 'chat':chat_title,
             'type': message.type})

    session.close()
    return messages, count


def inline_caps(update, context):
    from_user_id = update.inline_query.from_user.id
    # Check user permission
    session = DBSession()
    chats = session.query(Chat)
    if not chats:
        return
    chat_ids = []
    for chat in chats:
        chat_member= context.bot.get_chat_member(chat_id=chat.id, user_id=from_user_id)
        if chat_member.status != 'left' and chat_member.status != 'kicked':
            chat_ids.append(chat.id)

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
    messages, count = search_messages(keywords, page, chat_ids)
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
                description=message['date'].strftime("%Y-%m-%d").ljust(40) + message['user'] + '@' +message['chat'],
                input_message_content=InputTextMessageContent(
                    '{}<a href="{}">「From {}」</a>'.format(html.escape(message['text']), message['link'], message['user']),parse_mode='html'
                    ) if
                message['link'] != '' and message['type'] == 'text' or message['id'] < 0 else InputTextMessageContent(
                    '/locate {}'.format(message['id']))
            )
        )
    context.bot.answer_inline_query(update.inline_query.id, results)


handler = InlineQueryHandler(inline_caps)
