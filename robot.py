# coding: utf-8
from telegram.ext import Updater
import config
import logging
from user_handlers import custom_handlers
from user_jobs import custom_jobs
from user_handlers.__error_handle import error_callback

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token=config.TOKEN)
dispatcher = updater.dispatcher
job = updater.job_queue

# handle error
dispatcher.add_error_handler(error_callback)

# handle user_handlers
for handler in custom_handlers:
    dispatcher.add_handler(handler)

# jobs
for job_info in custom_jobs:
    job.run_repeating(**job_info)

if __name__ == '__main__':
    # polling mode
    updater.start_polling()

    # Webhook mode
    # updater.start_webhook(listen='127.0.0.1', port=12306, url_path='TOKEN')
    # updater.bot.set_webhook(url='https://telegram.xxx.xx/TOKEN')
    # updater.idle()
