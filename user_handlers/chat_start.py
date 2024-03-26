from telegram.ext import CommandHandler
import telegram.error

from database import Chat, DBSession
from utils import check_control_permission, is_userbot_mode, read_userbot_admin_id


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
    from_user_id = update.message.from_user.id

    # userbot模式下通过命令加群聊ID的形式设置
    if is_userbot_mode():
        admin_id = read_userbot_admin_id()
        if from_user_id == admin_id and len(context.args) == 1:
            command_text = context.args[0]
            if command_text.isdigit() or command_text.lstrip('-').isdigit():
                msg_text = insert_chat_or_enable(int(command_text), '')
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)
        return
    # 正常模式直接在对应群聊中使用命令
    chat_id = update.effective_chat.id
    chat_title = update.message.chat.title
    
    # 对成员过多的群组非管理员可能无法读取成员信息
    try:
        chat_member = context.bot.get_chat_member(
            chat_id=chat_id, user_id=from_user_id)
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=update.effective_chat.id, 
            text='读取群成员信息出错 (Telegram对大群的限制), 授予管理员后再试')
        return
    
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
    if not update.message.chat.type == 'supergroup':
        msg_text = '仅在超级群组中可用'
    else:
        msg_text = insert_chat_or_enable(chat_id, chat_title)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)


handler = CommandHandler('start', start)
