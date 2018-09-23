from telegram.error import BadRequest
from utils import auto_delete
from config import GROUP_ID


@auto_delete
def send_error_message(bot, update, text):
    sent_message = bot.send_message(chat_id=GROUP_ID, text=text, disable_notification=True)
    return sent_message


def error_callback(bot, update, error):
    try:
        raise error
    except BadRequest as e:
        if e.message == 'Reply message not found':
            send_error_message(bot, update, text='Message not exists.')
        else:
            send_error_message(bot, update, text='Unknown error.')
