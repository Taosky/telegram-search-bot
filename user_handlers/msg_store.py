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
    if target_chat.title != title:
        target_chat.title = title
        session.commit()
    session.close()


def insert_message(msg_id, msg_link, msg_text, msg_video, msg_photo, msg_audio, msg_voice, msg_type, from_id, from_chat,
                   date):
    new_msg = Message(id=msg_id, link=msg_link, text=msg_text, video=msg_video, photo=msg_photo, audio=msg_audio,
                      voice=msg_voice, type=msg_type, category='', from_id=from_id, from_chat=from_chat, date=date)
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


def store_message(update, context):
    session = DBSession()
    chat_ids = [chat.id for chat in session.query(Chat) if chat.enable]
    if update.effective_chat.id not in chat_ids:
        return

    '''
    Determine if it is an edited message. If it is, search for existing messages in the database based on GroupID and Message ID
    and update them.
    
    I personally don't really want to write about updates on media such as images and audio. Even if they are updated, it doesn't
    seem to be of great use at the moment. Images are not like text that cannot be queried without good segmentation,
    It is completely possible to use TG's built-in image search to solve this problem. So I only updated the text messages in this
    section and did not update any other messages.
    
    In addition, the time of the edited message is also determined here. If the difference between the original message release time
    and the edited message time is too large, it will not be updated to avoid the dme database explosion of the userbot.
    '''
    if update.edited_message:
        # Determine the interval between edited messages
        if (update.edited_message.edit_date - update.edited_message.date).seconds > 120:
            return

        if update.edited_message.text:
            msg_text = update.edited_message.text if update.edited_message.text else ''
        elif update.edited_message.caption:
            msg_text = update.edited_message.caption if update.edited_message.caption else ''
        else:
            return

        msg_id = update.edited_message.message_id
        chat_id = update.edited_message.chat.id

        update_message(chat_id, msg_id, msg_text)
        return
    
    if update.message.via_bot:
        if update.message.via_bot.id == context.bot.get_me().id:
            return
    '''
    The if here determines whether the speech is a user, channel, or group.
    It should be noted that, BOT cannot be ruled out here, for backward compatibility, the Anon group entity will come with a from parameter, where bot is true. 
    "from": {
        "id": 1087968824,
        "first_name": "Group",
        "username": "GroupAnonymousBot",
        "is_bot": true
    }
    '''
    if update.message.sender_chat:
        user_id = from_id = update.message.sender_chat.id
        sender_fullname = update.message.sender_chat.title if update.message.sender_chat.title else ''
        sender_username = update.message.sender_chat.username if update.message.sender_chat.username else ''
    elif update.message.from_user:
        # Return if from_user is bot
        if update.message.from_user.is_bot:
            return
        user_id = from_id = update.message.from_user.id
        sender_fullname = update.message.from_user.full_name if update.message.from_user.full_name else ''
        sender_username = update.message.from_user.username if update.message.from_user.username else ''
    else:
        return

    msg_id = update.message.message_id
    msg_link = update.message.link
    chat_id = update.message.chat.id
    chat_title = update.message.chat.title

    msg_photo = msg_video = msg_audio = msg_text = msg_voice = ''
    if update.message.photo:
        photo_sizes = [photo_size_info.file_size for photo_size_info in update.message.photo]
        msg_photo = update.message.photo[photo_sizes.index(max(photo_sizes))].file_id
        msg_text = update.message.caption if update.message.caption else ''
        msg_type = 'photo'
    elif update.message.video:
        msg_video = update.message.video.file_id if update.message.video else ''
        msg_text = update.message.caption if update.message.caption else ''
        msg_type = 'video'
    elif update.message.audio:
        msg_audio = update.message.audio.file_id if update.message.audio else ''
        msg_text = update.message.caption if update.message.caption else ''
        msg_type = 'audio'
    elif update.message.voice:
        msg_voice = update.message.voice.file_id if update.message.voice else ''
        msg_type = 'voice'
    elif update.message.text:
        msg_text = update.message.text if update.message.text else ''
        msg_type = 'text'
    else:
        msg_type = 'unknown'

    # Insert and update
    insert_message(msg_id, msg_link, msg_text, msg_video, msg_photo, msg_audio, msg_voice, msg_type, from_id, chat_id,
                   update.message.date)
    insert_or_update_user(user_id, sender_fullname, sender_username)
    update_chat(chat_id, chat_title)


handler = MessageHandler(
    Filters.text | Filters.video | Filters.photo | Filters.audio | Filters.voice,
    store_message,
)
