from telegram.ext import CommandHandler
import config
from utils import auto_delete, delete_prev_message
import datetime
from database import DBSession, DBFile


@auto_delete
def get_database_file(bot, update):
    if update.message.chat_id != config.GROUP_ID:
        return
    delete_prev_message(bot, update)

    now = datetime.datetime.now()

    session = DBSession()
    count = session.query(DBFile).filter().count()
    if count:
        last_db_file = session.query(DBFile).filter().order_by(DBFile.date.desc()).first()
    else:
        last_db_file = None

    if last_db_file and last_db_file.date + datetime.timedelta(minutes=10) > now:
        file = last_db_file.file_id
        filename = 'bot.{}.db'.format(last_db_file.date.strftime("%Y-%m-%d_%H.%M"))
        new_record = False
    else:
        file = open('bot.db', 'rb')
        filename = 'bot.{}.db'.format(now.strftime("%Y-%m-%d_%H.%M"))
        new_record = True

    sent_message = bot.send_document(chat_id=update.message.chat_id, document=file, filename=filename,
                                     disable_notification=True)

    # 保存新的获取数据库记录
    if new_record:
        file_id = sent_message.document.file_id
        new_db_file = DBFile(file_id=file_id, date=now)
        session.add(new_db_file)
        session.commit()

    session.close()

    return sent_message


handler = CommandHandler('database', get_database_file)
