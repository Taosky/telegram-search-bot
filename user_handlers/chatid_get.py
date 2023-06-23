from telegram.ext import CommandHandler
from utils import auto_delete

@auto_delete
def get_chat_id(update, context):
    sent_message = context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_chat.id))
    return sent_message


handler = CommandHandler('chat_id', get_chat_id)
