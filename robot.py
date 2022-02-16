from telegram.ext import Updater
import logging
import sys
import os
from user_handlers import bot_help, chat_start, chat_stop, chat_delete, chatid_get, msg_search, msg_store
from user_jobs.commands_set import set_bot_commands

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

bot_token = os.getenv('BOT_TOKEN')

updater = Updater(token=bot_token)

dispatcher = updater.dispatcher

# Run jobs
job = updater.job_queue
job.run_once(set_bot_commands, 30)

# Handle user_handlers
dispatcher.add_handler(chat_start.handler)
dispatcher.add_handler(chat_stop.handler)
dispatcher.add_handler(chat_delete.handler)
dispatcher.add_handler(bot_help.handler)
dispatcher.add_handler(chatid_get.handler)
dispatcher.add_handler(msg_search.handler)
dispatcher.add_handler(msg_store.handler)


if __name__ == '__main__':
    # Select mode
    if os.getenv("BOT_MODE") == "webhook":
        url_path = os.getenv("URL_PATH")
        hook_url = os.getenv("HOOK_URL")
        updater.start_webhook(listen='0.0.0.0',
                              port=9968,
                              url_path=url_path,
                              webhook_url=hook_url)
    else:
        updater.start_polling()
    updater.idle()

