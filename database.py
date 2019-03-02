# coding: utf-8
from sqlalchemy import Column, INTEGER, TEXT, DATETIME, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

engine = create_engine('sqlite:///bot.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool,
                       echo=True)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class Message(Base):
    # 表的名字
    __tablename__ = 'message'

    # 表的结构
    id = Column(INTEGER, primary_key=True)
    type = Column(TEXT)  # 文本、图像、视频、音频、语音
    category = Column(TEXT)  # 分类
    text = Column(TEXT)
    video = Column(TEXT)
    photo = Column(TEXT)
    audio = Column(TEXT)
    voice = Column(TEXT)
    date = Column(DATETIME)
    from_id = Column(INTEGER)


class User(Base):
    # 表的名字
    __tablename__ = 'user'

    # 表的结构
    id = Column(INTEGER, primary_key=True)
    fullname = Column(TEXT)
    username = Column(TEXT)
    update_time = Column(DATETIME)


class DBFile(Base):
    # 表的名字
    __tablename__ = 'db_file'

    # 表的结构
    file_id = Column(TEXT, primary_key=True)
    date = Column(DATETIME)


Base.metadata.create_all(engine)

#############

# def init_db():
#     if os.path.exists('.database'):
#         return
#     db = pymysql.connect(**DATABASE)
#     cursor = db.cursor()
#
#     sql = """CREATE TABLE group_message(
#              id BIGINT,
#              user varchar(100),
#              content MEDIUMTEXT,
#              time DATETIME)"""
#     try:
#         cursor.execute(sql)
#         db.commit()
#     except:
#         db.rollback()
#     db.close()
#     open('.database', 'a').close()
#
#
# def insert_db(msg_id, msg_user, msg_text, msg_time):
#     db = pymysql.connect(**DATABASE)
#     cursor = db.cursor()
#     sql = """INSERT INTO group_message(id,user,content,time) VALUE
#      ({},'{}','{}','{}')""".format(msg_id, msg_user, msg_text, msg_time)
#     try:
#         cursor.execute(sql)
#         db.commit()
#     except:
#         db.rollback()
#     db.close()
#
#
# def search_db(text=None, page=1):
#     db = pymysql.connect(**DATABASE)
#     cursor = db.cursor()
#     if text:
#         search_sql = "SELECT * FROM group_message WHERE locate('{}',content) ORDER BY time DESC LIMIT {}, {}".format(
#             text, (page - 1) * SEARCH_PAGE_SIZE, SEARCH_PAGE_SIZE)
#         count_sql = "SELECT count(id) FROM group_message WHERE locate('{}',content)".format(text)
#     else:
#         search_sql = "SELECT * FROM group_message ORDER BY time DESC LIMIT {}, {}".format((page - 1) * SEARCH_PAGE_SIZE,
#                                                                                           SEARCH_PAGE_SIZE)
#         count_sql = "SELECT count(id) FROM group_message"
#
#     try:
#         cursor.execute(count_sql)
#         count = cursor.fetchall()[0][0]
#         if count <= (page - 1) * SEARCH_PAGE_SIZE:
#             result = []
#         else:
#             cursor.execute(search_sql)
#             messages = cursor.fetchall()
#             result = [{'id': row[0], 'user': row[1], 'text': row[2], 'time': row[3]} for row in messages]
#
#     except BaseException as e:
#         logging.log(logging.DEBUG, e)
#         result = []
#         count = -1
#
#     db.close()
#     return result, count
#
#
# def get_document(msg_id):
#     db = pymysql.connect(**DATABASE)
#     cursor = db.cursor()
#     sql = "SELECT content,user, time FROM group_message WHERE id={}".format(msg_id)
#
#     try:
#         cursor.execute(sql)
#         message = cursor.fetchall()[0]
#         result = {'text': message[0], 'user': message[1], 'time': message[2]}
#
#     except:
#         result = None
#
#     db.close()
#     return result
#
#
# def get_prev_document_id(msg_id):
#     db = pymysql.connect(**DATABASE)
#     cursor = db.cursor()
#     sql = "SELECT id FROM group_message WHERE id=(SELECT id FROM group_message WHERE id<{} order by id desc limit 1)".format(
#         msg_id)
#
#     try:
#         cursor.execute(sql)
#         message = cursor.fetchall()[0]
#         result = message[0]
#
#     except:
#         result = None
#
#     db.close()
#     return result
