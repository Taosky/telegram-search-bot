from telegram.ext import CommandHandler
from database import Message, Chat, DBSession
from utils import check_control_permission, is_userbot_mode, read_userbot_admin_id


def delete_chat_or_do_nothing(chat_id):
    session = DBSession()
    target_chat = session.query(Chat).get(chat_id)
    if target_chat and not target_chat.enable:
        session.delete(target_chat)
        session.commit()
        related_messages = session.query(
            Message).filter(Message.from_chat == chat_id)
        for message in related_messages:
            session.delete(message)
            session.commit()
        msg_text = '成功删除相关记录'
    else:
        msg_text = '此前未停用或未启用'
    session.close()
    return msg_text


def delete(update, context):
    from_user_id = update.message.from_user.id
    # userbot模式下通过命令加群聊ID的形式设置
    if is_userbot_mode():
        admin_id = read_userbot_admin_id()
        if from_user_id == admin_id and len(context.args) == 1:
            command_text = context.args[0]
            if command_text.isdigit() or command_text.lstrip('-').isdigit():
                msg_text = delete_chat_or_do_nothing(int(command_text))
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)
        return
    # 正常模式直接在对应群聊中使用命令
    chat_id = update.effective_chat.id
    chat_member = context.bot.get_chat_member(
        chat_id=chat_id, user_id=from_user_id)
    # Check control permission
    if check_control_permission(from_user_id) is True:
        pass
    elif check_control_permission(from_user_id) is False:
        return
    elif check_control_permission(from_user_id) is None:
        if chat_member.status != 'creator' and chat_member.status != 'administrator':
            return
    else:
        return
    msg_text = delete_chat_or_do_nothing(chat_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)


handler = CommandHandler('delete', delete)
