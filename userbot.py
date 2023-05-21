from telethon import TelegramClient, events
from user_handlers import msg_store
from utils import write_chat_members, load_chat_members

import os
import json

listen_chat_ids = [int(cid)
                   for cid in os.getenv("USER_BOT_CHAT_IDS").split(',') if cid != '']
api_id = int(os.getenv("USER_BOT_API_ID"))
api_hash = os.getenv("USER_BOT_API_HASH")

client = TelegramClient('/app/config/anon', api_id, api_hash)

if not os.path.exists('.chat_members'):
    with open('.chat_members', 'w') as f:
        json.dump({}, f)


@client.on(events.NewMessage(chats=listen_chat_ids))
async def handler(event):
    current_chat = await event.get_chat()
    chat_id = current_chat.id
    if chat_id > 0:
        fixed_id = int('-100' + str(chat_id))
        if fixed_id in listen_chat_ids:
            chat_id = fixed_id
    chat_title = current_chat.title

    # 更新群组成员列表作为查询白名单
    chat_members = load_chat_members()
    members = await client.get_participants(current_chat)
    member_ids = [member.id for member in members]
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
        msg_photo = msg_video = msg_audio = msg_text = msg_voice = ''
        msg_text = event.message.message
        msg_type = 'text'
        msg_date = event.date
        print(msg_date)
        print(msg_link)
        print(chat_id)
        print('\n')
        # 存储消息
        msg_store.insert_message(msg_id, msg_link, msg_text, msg_video, msg_photo, msg_audio, msg_voice, msg_type, from_id, chat_id,
                                 msg_date)
        # 更新用户信息
        msg_store.insert_or_update_user(
            user_id, sender_fullname, sender_username)


client.start()
client.run_until_disconnected()
