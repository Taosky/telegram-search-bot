from telegram.ext import Updater
import logging
import sys
import os
from user_handlers import bot_help, bot_start, chatid_get, db_file_get, msg_search, msg_store
from user_jobs.commands_set import set_bot_commands

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)

bot_token = os.getenv('BOT_TOKEN')

updater = Updater(token=bot_token)

dispatcher = updater.dispatcher

# Run jobs
job = updater.job_queue
job.run_once(set_bot_commands, 30)

# Handle user_handlers
dispatcher.add_handler(bot_start.handler)
dispatcher.add_handler(bot_help.handler)
dispatcher.add_handler(chatid_get.handler)
dispatcher.add_handler(db_file_get.handler)
dispatcher.add_handler(msg_search.handler)
dispatcher.add_handler(msg_store.handler)

if __name__ == '__main__':        
    # Polling mode
    updater.start_polling()
    updater.idle()
