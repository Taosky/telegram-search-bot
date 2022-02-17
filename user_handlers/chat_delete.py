from telegram.ext import CommandHandler
from database import Message, Chat, DBSession


def delete_chat_or_do_nothing(chat_id):
    session = DBSession()
    target_chat = session.query(Chat).get(chat_id)
    if target_chat and not target_chat.enable:
        session.delete(target_chat)
        session.commit()
        related_messages = session.query(Message).filter(Message.from_chat==chat_id)
        for message in related_messages:
            session.delete(message)
            session.commit()
        msg_text = '成功删除相关记录'
    else:
        msg_text = '此前未停用或未启用'
    session.close()
    return msg_text

def delete(update, context):
    chat_id = update.effective_chat.id
    chat_title = update.message.chat.title
    from_user_id = update.message.from_user.id
    chat_member= context.bot.get_chat_member(chat_id=chat_id, user_id=from_user_id)
    if chat_member.status != 'creator' and chat_member.status != 'administrator':
        return
    msg_text = delete_chat_or_do_nothing(chat_id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)


handler = CommandHandler('delete', delete)