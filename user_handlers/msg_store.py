# coding: utf-8
from telegram.ext import MessageHandler, Filters
import config
from database import DBSession, Message, User


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


def insert_message(msg_id, msg_link, msg_text, msg_video, msg_photo, msg_audio, msg_voice, msg_type, from_id, date):
    new_msg = Message(id=msg_id, link=msg_link, text=msg_text, video=msg_video, photo=msg_photo, audio=msg_audio, voice=msg_voice,
                      type=msg_type, category='', from_id=from_id, date=date)
    session = DBSession()
    session.add(new_msg)
    session.commit()
    session.close()


def store_message(bot, update):
    if update.message.chat_id != config.GROUP_ID \
            or update.message.from_user.id in config.EXCEPT_IDS \
            or update.message.from_user.is_bot:
        return
    msg_id = update.message.message_id
    msg_link = update.message.link if update.message.link else ''
    from_id = update.message.from_user.id
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

    insert_message(msg_id, msg_link, msg_text, msg_video, msg_photo, msg_audio, msg_voice, msg_type, from_id,
                   update.message.date)

    user_id = from_id
    user_fullname = update.message.from_user.full_name if update.message.from_user.full_name else ''
    user_username = update.message.from_user.username if update.message.from_user.username else ''

    insert_or_update_user(user_id, user_fullname, user_username)


handler = MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.audio | Filters.voice, store_message)
