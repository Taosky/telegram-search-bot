from telegram.ext import CommandHandler
from database import Chat, DBSession


def disbale_chat_or_do_nothing(chat_id):
    session = DBSession()
    target_chat = session.query(Chat).get(chat_id)
    if target_chat and target_chat.enable:
        target_chat.enable = False
        session.add(target_chat)
        session.commit()
        msg_text = '成功停用,记录暂时保留,删除需使用/delete命令'
    else:
        msg_text = '此前已停用/未启用,启用需使用/start命令'
    session.close()
    return msg_text

def stop(update, context):
    chat_id = update.effective_chat.id
    chat_title = update.message.chat.title
    from_user_id = update.message.from_user.id
    chat_member= context.bot.get_chat_member(chat_id=chat_id, user_id=from_user_id)
    if chat_member.status != 'creator' and chat_member.status != 'administrator':
        return
    msg_text = disbale_chat_or_do_nothing(chat_id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)


handler = CommandHandler('stop', stop)