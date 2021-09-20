from telegram.ext import CommandHandler
from utils import read_config
import datetime
from database import DBSession, DBFile


def get_database_file(update, context):
    config = read_config()
    if not config or update.effective_chat.id != config['group_id']:
        return

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

    sent_message = context.bot.send_document(chat_id=update.effective_chat.id, document=file, filename=filename,
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
