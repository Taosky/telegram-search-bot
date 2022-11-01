import math
import re
import html
import telegram
import os
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedSticker, InlineQueryResultCachedPhoto
from telegram.ext import InlineQueryHandler
from database import User, Message, Chat, DBSession
from sqlalchemy import and_

SEARCH_PAGE_SIZE = 25
CACHE_TIME = int(os.getenv('CACHE_TIME'))


def search_messages(keywords, page, filter_chats):
    messages = []
    start = (page - 1) * SEARCH_PAGE_SIZE
    stop = page * SEARCH_PAGE_SIZE
    session = DBSession()
    chat_ids = [chat[0] for chat in filter_chats]
    chat_titles = [chat[1] for chat in filter_chats]

    if keywords:
        rule = and_(*[Message.text.like('%' + keyword + '%') for keyword in keywords])
        count = session.query(Message).filter(rule).filter(Message.from_chat.in_(chat_ids)).count()
        query = session.query(Message).filter(rule).filter(Message.from_chat.in_(chat_ids))
    else:
        count = session.query(Message).filter(Message.from_chat.in_(chat_ids)).count()
        query = session.query(Message).filter(Message.from_chat.in_(chat_ids))

    for message in query.order_by(Message.date.desc()).slice(start, stop).all():
        user = session.query(User).filter_by(id=message.from_id).one()
        user_fullname = user.fullname
        index = chat_ids.index(message.from_chat)
        chat_title = chat_titles[index]

        if message.type != 'text':
            msg_text = f'[{message.type}] {message.text if message.text else ""}'
        else:
            msg_text = message.text

        if msg_text == '':
            continue

        messages.append(
            {
                'id': message.id,
                'link': message.link,
                'text': msg_text,
                'date': message.date,
                'user': user_fullname,
                'chat': chat_title,
                'type': message.type
            }
        )

    session.close()
    return messages, count


def inline_caps(update, context):
    from_user_id = update.inline_query.from_user.id
    session = DBSession()
    chats = session.query(Chat)
    if not chats:
        return

    filter_chats = []
    for chat in chats:
        if not chat.enable:
            continue
        try:
            chat_member = context.bot.get_chat_member(chat_id=chat.id, user_id=from_user_id)
        except telegram.error.BadRequest:
            continue
        except telegram.error.Unauthorized:
            continue

        if chat_member.status != 'left' and chat_member.status != 'kicked':
            filter_chats.append((chat.id, chat.title))

    query = update.inline_query.query

    if not query:
        keywords, page = None, 1
    elif re.match(' *\* +(\d+)', query):
        keywords, page = None, int(re.match('\* +(\d+)', query).group(1))
    else:
        keywords = [word for word in query.split(" ")]
        if keywords[-1].isdigit():
            page = int(keywords[-1])
            keywords.pop()
        else:
            page = 1

    messages, count = search_messages(keywords, page, filter_chats)

    if count == 0:
        results = [
            InlineQueryResultArticle(
                id='empty',
                title='好像没有查询到任何结果呢？',
                description='Attention! 不要点击任何按钮，否则会发送空消息。',
                input_message_content=InputTextMessageContent('.')
            )]
    else:
        results = [InlineQueryResultArticle(
            id='info',
            title='Total:{}. Page {} of {}'.format(count, page, math.ceil(count / SEARCH_PAGE_SIZE)),
            description='Attention! 这只是一条提示消息，不要点击它，否则会发送 /help 消息',
            input_message_content=InputTextMessageContent(f'/help@{context.bot.get_me().username}')
        )]

    for message in messages:
        results.append(
            InlineQueryResultArticle(
                id=message['id'],
                title='{}'.format(message['text'][:100]),
                description=message['date'].strftime("%Y-%m-%d").ljust(40) + str(message['user']) + '@' + message[
                    'chat'],
                input_message_content=InputTextMessageContent(
                    '「{}」<a href="{}">Via {}</a>'.format(html.escape(message['text']),
                                                         message['link'],
                                                         message['user']), parse_mode='html'
                )
            )
        )
    context.bot.answer_inline_query(update.inline_query.id, results, cache_time=CACHE_TIME)


handler = InlineQueryHandler(inline_caps)
