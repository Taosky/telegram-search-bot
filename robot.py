from telegram.ext import Updater
from threading import Thread
import asyncio
import logging
import os
from user_handlers import bot_help, chat_start, chat_stop, chat_delete, chatid_get, msg_search, msg_store
from user_jobs.commands_set import set_bot_commands
from userbot import run_telethon
from utils import is_userbot_mode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

bot_token = os.getenv('BOT_TOKEN')

updater = Updater(token=bot_token)

dispatcher = updater.dispatcher

# 设置bot命令
job = updater.job_queue
job.run_once(set_bot_commands, 30)

# 处理用户操作
dispatcher.add_handler(msg_search.handler)
dispatcher.add_handler(chat_start.handler)
dispatcher.add_handler(chat_stop.handler)
dispatcher.add_handler(chat_delete.handler)
dispatcher.add_handler(bot_help.handler)
dispatcher.add_handler(chatid_get.handler)
# 只在非userbot模式下存储记录
if not is_userbot_mode():
    dispatcher.add_handler(msg_store.handler)


# 在新的线程中执行 Telethon 的异步操作
def run_telethon_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_telethon())

if __name__ == '__main__':
    # 创建一个线程来运行userbot
    telethon_thread = Thread(target=run_telethon_thread)
    telethon_thread.start()
    logging.info('userbot启动...')
    
    # webhook / pollling
    if os.getenv("BOT_MODE") == "webhook":
        url_path = os.getenv("URL_PATH")
        hook_url = os.getenv("HOOK_URL")
        updater.start_webhook(listen='0.0.0.0',
                              port=9968,
                              url_path=url_path,
                              webhook_url=hook_url)
    else:
        updater.start_polling()
    logging.info('robot启动...')
    updater.idle()

