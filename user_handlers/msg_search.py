import math
import re
import html
import telegram
import os
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedSticker
from telegram.ext import InlineQueryHandler
from database import User, Message, Chat, DBSession
from sqlalchemy import and_

from utils import get_filter_chats


SEARCH_PAGE_SIZE = 25
CACHE_TIME = int(os.getenv('CACHE_TIME'))

def get_query_matches(query):
    user, keywords, page = None, None, 1
    if not query:
        pass
    elif re.match(' *\* +(\d+)', query):
        user, keywords, page = None, None, int(re.match('\* +(\d+)', query).group(1))
    # 匹配 @用户 * page 形式
    elif re.match(' *@(.+) +\* +(\d+)', query):
        r = re.match(' *@(.+) +\* +(\d+)', query)
        user, keywords, page = r.group(1), None, int(r.group(2))
    else:
        keywords = [word for word in query.split(' ')]            
        if keywords[-1].isdigit():
            page = int(keywords[-1])
            keywords.pop()
        else:
            page = 1
        # 第一个字符为 @ 时作特殊处理
        if len(keywords) >= 1 and keywords[0].startswith('@'):
            user = keywords[0].lstrip('@')
            if len(keywords) >= 2:
                keywords = keywords[1:]
            else:
                keywords = None
    return user, keywords, page


def search_messages(uname, keywords, page, filter_chats):
    messages = []
    start = (page - 1) * SEARCH_PAGE_SIZE
    stop = page * SEARCH_PAGE_SIZE
    session = DBSession()
    chat_ids = [chat[0] for chat in filter_chats]
    chat_titles = [chat[1] for chat in filter_chats]
    user_ids = []

    if uname:        
        user_count = session.query(User).filter(User.fullname.like('%' + uname + '%')).count()
        if user_count >=1:
            for user in session.query(User).filter(User.fullname.like('%' + uname + '%')).all():
                user_ids.append(user.id)

    if keywords:
        rule = and_(*[Message.text.like('%' + keyword + '%') for keyword in keywords])
        if uname:
            count = session.query(Message).filter(rule).filter(Message.from_chat.in_(chat_ids)).filter(Message.from_id.in_(user_ids)).count()
            query = session.query(Message).filter(rule).filter(Message.from_chat.in_(chat_ids)).filter(Message.from_id.in_(user_ids))
        else:
            count = session.query(Message).filter(rule).filter(Message.from_chat.in_(chat_ids)).count()
            query = session.query(Message).filter(rule).filter(Message.from_chat.in_(chat_ids))
    else:
        if uname:
            count = session.query(Message).filter(Message.from_chat.in_(chat_ids)).filter(Message.from_id.in_(user_ids)).count()
            query = session.query(Message).filter(Message.from_chat.in_(chat_ids)).filter(Message.from_id.in_(user_ids))
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

    # userbot模式
    if os.getenv("USER_BOT")=="1":
        filter_chats = get_filter_chats(from_user_id)

    else:
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

    user, keywords, page = get_query_matches(query)

    # 在搜索消息前判断用户是否属于任意启用了 Bot 的群组，如果没有。直接返回一张你不许参加银趴的表情包
    # 循环 20 次是因为在某些设备上单独一张 sticker 可能会被不正确的拉伸，此外，20 张你不准参加银趴更加生草。
    if len(filter_chats) == 0:
        results = []
        num = 0
        for i in range(20):
            results.append(
                InlineQueryResultCachedSticker(
                    id=f'unauthorized_sticker_{str(num)}',
                    sticker_file_id='CAACAgUAAxkDAAEFBIhjffVfXIFyngE4vR2Zg_uDkDS41gACMAsAAoB48FdrYCP5TE3CEh4E'
                )
            )
            num += 1
        context.bot.answer_inline_query(update.inline_query.id, results, cache_time=CACHE_TIME)
        return

    messages, count = search_messages(user, keywords, page, filter_chats)

    if count == 0:
        results = [
            InlineQueryResultArticle(
                id='empty',
                title='好像没有查询到任何结果呢？',
                description='Attention! 不要点击任何按钮，否则会发送空消息。',
                input_message_content=InputTextMessageContent('⁤')
            )]
    else:
        results = [
            InlineQueryResultArticle(
                id='info',
                title='Total:{}. Page {} of {}'.format(count, page, math.ceil(count / SEARCH_PAGE_SIZE)),
                description='Attention! 这只是一条提示消息，不要点击它，否则会发送 /help 消息',
                input_message_content=InputTextMessageContent(f'/help@{context.bot.get_me().username}')
            )
        ]

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
