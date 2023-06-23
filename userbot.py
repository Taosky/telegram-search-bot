from telethon import TelegramClient, events

from utils import write_chat_members, load_chat_members, update_userbot_admin_id
from database import DBSession, Message, User, Chat

import os
import time
import logging


SESSION_FILE = './config/anon.session'


def get_enabled_chat_ids():
    session = DBSession()
    chat_ids = [chat.id for chat in session.query(Chat) if chat.enable]
    session.close()
    return chat_ids


def insert_message(msg_id, msg_link, msg_text, from_id, from_chat, date):
    new_msg = Message(id=msg_id, link=msg_link, text=msg_text, video='', photo='', audio='',
                      voice='', type='text', category='', from_id=from_id, from_chat=from_chat, date=date)
    session = DBSession()
    session.add(new_msg)
    session.commit()
    session.close()

def update_message(from_chat, msg_id, msg_text):
    session = DBSession()
    session.query(Message) \
        .filter(Message.from_chat.is_(from_chat)) \
        .filter(Message.id.is_(msg_id)) \
        .update({"text": msg_text})
    session.commit()
    session.close()


def insert_or_update_user(user_id, fullname, username):
    session = DBSession()
    target_user = session.query(User).get(user_id)
    if not target_user:
        new_user = User(id=user_id, fullname=fullname, username=username)
        session.add(new_user)
        session.commit()
    elif target_user.fullname != fullname or target_user.username != username:
        target_user.fullname = fullname
        target_user.username = username
        session.commit()
    session.close()


async def handle_new_message(event, client):
    current_chat = await event.get_chat()
    # 跳过非群组消息
    if not hasattr(current_chat, 'title'):
        return
    chat_id = current_chat.id
    listen_chat_ids = get_enabled_chat_ids()
    if chat_id > 0:
        fixed_id = int('-100' + str(chat_id))
        if fixed_id in listen_chat_ids:
            chat_id = fixed_id
    # 跳过无关群组消息
    if chat_id not in listen_chat_ids:
        return
    chat_title = current_chat.title

    # 更新群组成员列表作为查询白名单
    chat_members = load_chat_members()
    members = await client.get_participants(current_chat)
    member_ids = [member.id for member in members if not member.deleted]
    chat_id_str = str(chat_id)
    chat_members[chat_id_str] = {}
    chat_members[chat_id_str]['title'] = chat_title
    chat_members[chat_id_str]['members'] = member_ids
    write_chat_members(chat_members)

    sender = await event.get_sender()
    # 排除bot和inline消息
    if not sender.bot and not event.via_bot_id:
        sender_username = sender.username
        sender_fullname = ''
        if sender.first_name:
            sender_fullname += sender.first_name + ' '
        if sender.last_name:
            sender_fullname += sender.last_name
        if sender_fullname == '':
            sender_fullname = sender_username
        user_id = from_id = event.from_id.user_id
        msg_id = event.id
        msg_link = 'https://t.me/c/{}/{}'.format(str(chat_id)[4:], event.id)
        msg_text = event.message.message
        msg_date = event.date
        logging.info('{} {}'.format(chat_id, msg_link))
        # 存储消息
        insert_message(msg_id, msg_link, msg_text, from_id, chat_id,  msg_date)
        # 更新用户信息
        insert_or_update_user(user_id, sender_fullname, sender_username)

async def handle_edit_message(event):
    current_chat = await event.get_chat()
    # 跳过非群组消息
    if not hasattr(current_chat, 'title'):
        return
    chat_id = current_chat.id
    listen_chat_ids = get_enabled_chat_ids()
    if chat_id > 0:
        fixed_id = int('-100' + str(chat_id))
        if fixed_id in listen_chat_ids:
            chat_id = fixed_id
    # 跳过无关群组消息
    if chat_id not in listen_chat_ids:
        return
    # 修改后的消息
    edited_message = event.message
    if (edited_message.edit_date - edited_message.date).seconds > 120:
        return
    msg_id = edited_message.id
    msg_text = edited_message.message

    update_message(chat_id, msg_id, msg_text)

async def run_telethon():
    while not os.path.exists(SESSION_FILE):
       logging.info('尚未登陆，等待10秒重试...')
       time.sleep(10)
    api_id = int(os.getenv("USER_BOT_API_ID"))
    api_hash = os.getenv("USER_BOT_API_HASH")
    client = TelegramClient(SESSION_FILE, api_id, api_hash)
    # 监听处理新消息
    client.add_event_handler(lambda event: handle_new_message(
        event, client), events.NewMessage)
    # 监听处理消息修改
    client.add_event_handler(handle_edit_message, events.MessageEdited)
    # 启动客户端
    await client.start()
    # 保存登陆用户到本地，作为管理用户（仅userbot模式下）
    me = await client.get_me()
    admin_id = me.id
    update_userbot_admin_id(admin_id)

    await client.run_until_disconnected()


def run_once():
    if os.path.exists(SESSION_FILE):
        print('session已存在，如需重新登陆，删除配置文件夹下的anon.session文件')
    else:
        api_id = int(os.getenv("USER_BOT_API_ID"))
        api_hash = os.getenv("USER_BOT_API_HASH")
        client = TelegramClient(SESSION_FILE, api_id, api_hash)
        # 启动客户端
        client.start()


if __name__ == '__main__':
    run_once()
