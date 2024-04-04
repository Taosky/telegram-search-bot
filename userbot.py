from telethon import TelegramClient, events
from utils import write_chat_members, load_chat_members, update_userbot_admin_id
from database import DBSession, Message, User, Chat
from utils import get_text_func, group_history_is_fetched, write_history_groups

import os
import time
import logging
import pathlib
import asyncio
import threading


SESSION_FILE = './config/anon.session'
SESSION_LOCK_FILE = './config/anon.session.lock'

user_client = None

file_lock = threading.Lock()


_ = get_text_func()


def get_sender_fullname(sender):
    sender_username = sender.username
    sender_fullname = ''
    if sender.first_name:
        sender_fullname += sender.first_name + ' '
    if sender.last_name:
        sender_fullname += sender.last_name
    if sender_fullname == '':
        sender_fullname = sender_username
    return sender_fullname


def get_enabled_chat_ids():
    session = DBSession()
    chat_ids = [chat.id for chat in session.query(Chat) if chat.enable]
    session.close()
    return chat_ids

def update_whitelist_or_do_nothing(chat_id, member_ids, chat_title):
    chat_id_str = str(chat_id)
    chat_members = load_chat_members()
    if chat_id_str in chat_members:
        current_chat_members = chat_members[chat_id_str]['members']
        if len(current_chat_members) != member_ids:
            chat_members[chat_id_str] = {}
            chat_members[chat_id_str]['title'] = chat_title
            chat_members[chat_id_str]['members'] = member_ids
            with file_lock:
                write_chat_members(chat_members)
        else:    
            for member_id in member_ids:
                if member_id not in current_chat_members:
                    chat_members[chat_id_str] = {}
                    chat_members[chat_id_str]['title'] = chat_title
                    chat_members[chat_id_str]['members'] = member_ids
                    with file_lock:
                        write_chat_members(chat_members)
                    break
    else:
        chat_members[chat_id_str] = {}
        chat_members[chat_id_str]['title'] = chat_title
        chat_members[chat_id_str]['members'] = member_ids
        with file_lock:
            write_chat_members(chat_members)


def insert_message(msg_id, msg_link, msg_text, from_id, from_chat, date):
    new_msg = Message(id=msg_id, link=msg_link, text=msg_text, video='', photo='', audio='',
                      voice='', type='text', category='', from_id=from_id, from_chat=from_chat, date=date)
    session = DBSession()
    target_msg = session.query(Message).filter_by(id=msg_id).first()
    if not target_msg:
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
    # do nothing if user exists and new from history
    elif fullname == 'temp name':
        pass
    elif target_user.fullname != fullname or target_user.username != username:
        target_user.fullname = fullname
        target_user.username = username
        session.commit()
    session.close()


async def fetch_msg_history(chat_id):
    if not user_client:
        return
    count = 0
    messages = await user_client.get_messages(chat_id, limit=100)
    while messages:
        await asyncio.sleep(5)
        # stop fetching when group disabled
        listen_chat_ids = get_enabled_chat_ids()
        if chat_id not in listen_chat_ids:
            break
        for message in messages:
            if not message.text:
                continue
            count += 1
            # Save message
            link_chat_id = str(chat_id)[4:] if str(chat_id).startswith('-100') else str(chat_id)
            msg_link = 'https://t.me/c/{}/{}'.format(link_chat_id, message.id)
            insert_message(message.id, msg_link, message.text, message.from_id.user_id, chat_id, message.date)
            # Update user info
            # sender = await user_client.get_entity(message.from_id)
            # sender_fullname = get_sender_fullname(sender)
            insert_or_update_user(message.from_id.user_id, 'temp name', 'temp_username')
        
        messages = await user_client.get_messages(chat_id, limit=100, offset_id=messages[-1].id-1)

    logging.info(_('{} messages fetched!').format(count))
    return

async def handle_new_message(event, client):
    current_chat = await event.get_chat()
    # Skip non-group
    if not hasattr(current_chat, 'title'):
        return
    # Fix chat id
    chat_id = current_chat.id
    listen_chat_ids = get_enabled_chat_ids()
    if chat_id > 0:
        fixed_id = int('-100' + str(chat_id))
        if fixed_id in listen_chat_ids:
            chat_id = fixed_id
    # Skip other groups
    if chat_id not in listen_chat_ids:
        return

    # Update group member list as whitelist
    new_chat_title = current_chat.title    
    members = await client.get_participants(current_chat)
    new_member_ids = [member.id for member in members if not member.deleted]
    update_whitelist_or_do_nothing(chat_id, new_member_ids, new_chat_title)
    
    # Fetch history if not fetched before
    if not group_history_is_fetched(chat_id):
        logging.info(_('fetching history...'))
        with file_lock:
            write_history_groups(chat_id)
        asyncio.create_task(fetch_msg_history(chat_id))
        return  # Skip current message

    sender = await event.get_sender()
    # Skip bot message and inline message
    if not sender.bot and not event.via_bot_id:
        sender_fullname = get_sender_fullname(sender)
        user_id = from_id = event.from_id.user_id
        msg_id = event.id
        link_chat_id = str(chat_id)[4:] if str(chat_id).startswith('-100') else str(chat_id)
        msg_link = 'https://t.me/c/{}/{}'.format(link_chat_id, event.id)
        msg_text = event.message.message
        msg_date = event.date
        logging.debug('new_message: chat{} user{} "{}"'.format(
            chat_id, from_id, msg_text))

        # Save message
        insert_message(msg_id, msg_link, msg_text, from_id, chat_id, msg_date)
        # Update user info
        insert_or_update_user(user_id, sender_fullname, sender.username)


async def handle_edit_message(event):
    current_chat = await event.get_chat()
    # Skip other groups
    if not hasattr(current_chat, 'title'):
        return
    chat_id = current_chat.id
    listen_chat_ids = get_enabled_chat_ids()
    if chat_id > 0:
        fixed_id = int('-100' + str(chat_id))
        if fixed_id in listen_chat_ids:
            chat_id = fixed_id
    # Skip other groups
    if chat_id not in listen_chat_ids:
        return
    # Read edited message
    edited_message = event.message
    if (edited_message.edit_date - edited_message.date).seconds > 120:
        return
    msg_id = edited_message.id
    from_id = event.from_id.user_id
    msg_text = edited_message.message

    logging.debug('edit_message: chat{} user{} "{}"'.format(
        chat_id, from_id, msg_text))

    update_message(chat_id, msg_id, msg_text)


async def run_telethon():
    global user_client

    while not os.path.exists(SESSION_FILE) or os.path.exists(SESSION_LOCK_FILE):
        logging.info(_('not logged in, waiting 10s to retry...'))
        time.sleep(10)
    api_id = int(os.getenv("USER_BOT_API_ID"))
    api_hash = os.getenv("USER_BOT_API_HASH")
    user_client = TelegramClient(SESSION_FILE, api_id, api_hash)
    # Listen and handle new message
    user_client.add_event_handler(lambda event: handle_new_message(
        event, user_client), events.NewMessage)
    # Listen and handle edited message
    user_client.add_event_handler(handle_edit_message, events.MessageEdited)
    # Start client
    await user_client.start()
    # Save the user logged in as admin (only work in userbot mode)
    me = await user_client.get_me()
    admin_id = me.id
    update_userbot_admin_id(admin_id)

    await user_client.run_until_disconnected()


def run_once():
    if os.path.exists(SESSION_FILE):
        print(_('session exists, delete `anon.session` to login again'))
    else:
        pathlib.Path(SESSION_LOCK_FILE).touch()
        api_id = int(os.getenv("USER_BOT_API_ID"))
        api_hash = os.getenv("USER_BOT_API_HASH")
        client = TelegramClient(SESSION_FILE, api_id, api_hash)
        # Start client
        client.start()

        time.sleep(5)
        os.remove(SESSION_LOCK_FILE)


if __name__ == '__main__':
    run_once()
