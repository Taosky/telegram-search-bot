from telegram.ext import CommandHandler
from database import Chat, DBSession


def insert_chat_or_enable(chat_id, title):
    session = DBSession()
    target_chat = session.query(Chat).get(chat_id)
    if not target_chat:
        new_chat = Chat(id=chat_id, title=title, enable=True)
        session.add(new_chat)
        session.commit()
        msg_text = '成功启用'
    else:
        if target_chat.enable:
            msg_text = '前期已启用,停用需使用/stop命令'
        else:
            target_chat.enable = True
            session.commit()
            msg_text = '成功恢复使用'
    session.close()
    return msg_text


def start(update, context):
    msg_text = ''
    chat_id = update.effective_chat.id
    chat_title = update.message.chat.title
    from_user_id = update.message.from_user.id
    chat_member= context.bot.get_chat_member(chat_id=chat_id, user_id=from_user_id)
    if chat_member.status != 'creator' and chat_member.status != 'administrator':
        return
    if not update.message.chat.type == 'supergroup':
        msg_text = '仅在超级群组中可用'
    else:

        msg_text = insert_chat_or_enable(chat_id, chat_title)

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)


handler = CommandHandler('start', start)