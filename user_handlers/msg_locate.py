# coding: utf-8
from telegram.ext import CommandHandler
from database import Message, DBSession
from utils import auto_delete, delete_prev_message
import sqlalchemy


@auto_delete
def locate_message(bot, update, args):
    delete_prev_message(bot, update)
    if args and args[0].isdigit():
        msg_id = int(args[0])
    else:
        return
    session = DBSession()
    try:
        message = session.query(Message).filter_by(id=msg_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        message = None

    if message and message.type in ['text', 'video', 'photo', 'audio', 'voice']:
        if message.type == 'text':
            msg_method = 'message'
        else:
            msg_method = message.type
        content = {message.type: getattr(message, message.type)}
        send_msg_fun = getattr(bot, 'send_' + msg_method)
        sent_message = send_msg_fun(chat_id=update.message.chat_id, disable_notification=True,
                                    reply_to_message_id=msg_id, **content)
    else:
        sent_message = bot.send_message(chat_id=update.message.chat_id, disable_notification=True,
                                        reply_to_message_id=msg_id, text='！数据库未收录')

    session.close()

    return sent_message


handler = CommandHandler('locate', locate_message, pass_args=True)
