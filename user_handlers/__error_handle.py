from telegram.error import BadRequest
from database import get_document, get_prev_document_id
from utils import auto_delete
from config import GROUP_ID


@auto_delete
def send_error_message(bot, text, parse_mode=None):
    sent_message = bot.send_message(chat_id=GROUP_ID, text=text, parse_mode=parse_mode, disable_notification=True)
    return sent_message


def error_callback(bot, update, error):
    try:
        raise error
    except BadRequest as e:
        # locate message error
        if e.message == 'Reply message not found' and update.message.text.startswith('/locate'):
            msg_id = int(update.message.text.split(' ')[-1])
            msg = get_document(msg_id)
            prev_msg_id = get_prev_document_id(msg_id)
            if msg:
                send_error_message(bot, text='*消息已删除*\n{}：{}\n(/locate {} 定位上一条消息)'.format(msg['user'], msg['text'],
                                                                                            prev_msg_id),
                                   parse_mode='markdown')
            else:
                send_error_message(bot, text='消息不存在')
        # permission denied
        elif e.message == "Message can't be deleted":
            pass
        else:
            send_error_message(bot, text='未知错误')
