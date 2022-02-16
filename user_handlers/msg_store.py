# coding: utf-8
from telegram.ext import MessageHandler, Filters
from database import DBSession, Message, User, Chat


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


def update_chat(chat_id, title):
    session = DBSession()
    target_chat = session.query(Chat).get(chat_id)
    if target_chat.title != title :
        target_chat.title = title
        session.commit()
    session.close()


def insert_message(msg_id, msg_link, msg_text, msg_video, msg_photo, msg_audio, msg_voice, msg_type, from_id, from_chat, date):
    new_msg = Message(id=msg_id, link=msg_link, text=msg_text, video=msg_video, photo=msg_photo, audio=msg_audio,
                      voice=msg_voice, type=msg_type, category='', from_id=from_id, from_chat=from_chat, date=date)
    session = DBSession()
    session.add(new_msg)
    session.commit()
    session.close()


def store_message(update, context):
    session = DBSession()
    chat_ids = [chat.id for chat in session.query(Chat) if chat.enable]
    if update.effective_chat.id not in chat_ids \
            or update.message.from_user.is_bot \
                or update.message.via_bot:
        return
    msg_id = update.message.message_id
    msg_link = update.message.link
    from_id = update.message.from_user.id
    chat_id = update.message.chat.id
    chat_title = update.message.chat.title
    msg_text = update.message.text if update.message.text else ''
    msg_video = update.message.video.file_id if update.message.video else ''
    if update.message.photo:
        photo_sizes = [photo_size_info.file_size for photo_size_info in update.message.photo]
        msg_photo = update.message.photo[photo_sizes.index(max(photo_sizes))].file_id
    else:
        msg_photo = ''

    msg_audio = update.message.audio.file_id if update.message.audio else ''
    msg_voice = update.message.voice.file_id if update.message.voice else ''

    if msg_text:
        msg_type = 'text'
    elif msg_video:
        msg_type = 'video'
    elif msg_photo:
        msg_type = 'photo'
    elif msg_audio:
        msg_type = 'audio'
    elif msg_voice:
        msg_type = 'voice'
    else:
        msg_type = 'unknown'

    insert_message(msg_id, msg_link, msg_text, msg_video, msg_photo, msg_audio, msg_voice, msg_type, from_id, chat_id,
                   update.message.date)

    user_id = from_id
    user_fullname = update.message.from_user.full_name if update.message.from_user.full_name else ''
    user_username = update.message.from_user.username if update.message.from_user.username else ''

    insert_or_update_user(user_id, user_fullname, user_username)
    update_chat(chat_id, chat_title)

handler = MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.audio | Filters.voice, store_message)
