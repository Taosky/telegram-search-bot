from telegram.error import BadRequest
from database import DBSession, Message, User
from utils import auto_delete
from config import GROUP_ID


@auto_delete
def send_error_message(bot, msg_id, parse_mode='markdown'):
    # 消息不存在
    if not msg_id:
        sent_message = bot.send_message(chat_id=GROUP_ID, text='！消息不存在', disable_notification=True)
        return sent_message

    session = DBSession()
    msg = session.query(Message).filter_by(id=msg_id).one()
    prev_msg_id = session.query(Message).filter(Message.id < msg_id).order_by(Message.id.desc()).slice(0,
                                                                                                       1).one().id
    delete_tip_text = '*消息已删除*\n(/locate {} 定位上一条消息)'.format(prev_msg_id)
    fullname = session.query(User).filter_by(id=msg.from_id).one().fullname
    session.close()

    if msg.type in ['text', 'video', 'photo', 'audio', 'voice']:
        if msg.type == 'text':
            sent_message = bot.send_message(chat_id=GROUP_ID,
                                            text='{}\n\n{}: {}'.format(delete_tip_text, fullname, msg.text),
                                            parse_mode=parse_mode,
                                            disable_notification=True)
        else:
            msg_method = msg.type
            content = {
                msg.type: getattr(msg, msg.type),
            }
            send_msg_fun = getattr(bot, 'send_' + msg_method)
            sent_message = send_msg_fun(chat_id=GROUP_ID, arse_mode=parse_mode, disable_notification=True,
                                        caption=delete_tip_text, **content)
    else:
        sent_message = None

    return sent_message


def error_callback(bot, update, error):
    try:
        raise error
    except BadRequest as e:
        # locate message error
        if e.message == 'Reply message not found' and update.message.text.startswith('/locate'):
            msg_id = int(update.message.text.split(' ')[-1])
            session = DBSession()
            msg_count = session.query(Message).filter_by(id=msg_id).count()
            session.close()

            # 数据库中有这条消息
            if msg_count:
                send_error_message(bot, msg_id)

            else:
                send_error_message(bot, None)
        # permission denied
        elif e.message == "Message can't be deleted":
            pass
        else:
            send_error_message(bot, text='!未知错误')
