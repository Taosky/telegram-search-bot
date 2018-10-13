import time
from telegram import Sticker

import config

TIME_STICKERS = {
    11: 'CAADBQAD_gADDxXNGWuj_Z6psGN4Ag',
    1: 'CAADBQAD9AADDxXNGcJK3qzks8qLAg',
    8: 'CAADBQAD-wADDxXNGe8aqxEu9OCLAg',
}


def time_monitor(bot, job):
    now = time.localtime()
    if now.tm_min == 0 and now.tm_hour in TIME_STICKERS:
        bot.send_sticker(chat_id=config.GROUP_ID,
                         sticker=Sticker(file_id=TIME_STICKERS[now.tm_hour], width=376, height=376))


job_info = {'callback': time_monitor, 'interval': 30, 'first': None}
