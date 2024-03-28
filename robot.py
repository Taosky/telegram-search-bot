from telegram.ext import Updater
from threading import Thread
import asyncio
import logging
import os
from user_handlers import bot_help, chat_start, chat_stop, chat_delete, chatid_get, msg_search, msg_store
from user_jobs.commands_set import set_bot_commands
from userbot import run_telethon
from utils import is_userbot_mode, get_text_func

logging.basicConfig(format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

_ = get_text_func()

bot_token = os.getenv('BOT_TOKEN')

updater = Updater(token=bot_token)

dispatcher = updater.dispatcher

# Set bot command
job = updater.job_queue
job.run_once(set_bot_commands, 30)

# Handle user action
dispatcher.add_handler(msg_search.handler)
dispatcher.add_handler(chat_start.handler)
dispatcher.add_handler(chat_stop.handler)
dispatcher.add_handler(chat_delete.handler)
dispatcher.add_handler(bot_help.handler)
dispatcher.add_handler(chatid_get.handler)
# Do not save message when using userbot mode
if not is_userbot_mode():
    dispatcher.add_handler(msg_store.handler)


# Telethon thread func
def run_telethon_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_telethon())

if __name__ == '__main__':
    
    # Run userbot
    if is_userbot_mode():
        telethon_thread = Thread(target=run_telethon_thread, name='Thread-userbot')
        telethon_thread.start()
        logging.info(_('userbot start...'))
    
    # Webhook / Pollling
    mode_env = os.getenv("BOT_MODE")
    if mode_env == "webhook":
        url_path = os.getenv("URL_PATH")
        hook_url = os.getenv("HOOK_URL")
        updater.start_webhook(listen='0.0.0.0',
                              port=9968,
                              url_path=url_path,
                              webhook_url=hook_url)
    else:
        updater.start_polling()
    logging.info(_('robot start...'))
    updater.idle()

