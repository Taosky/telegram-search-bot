from sqlalchemy import Column, INTEGER, TEXT, BOOLEAN, DATETIME, create_engine, Index
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import OperationalError

engine = create_engine('sqlite:///./config/bot.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool,
                       echo=False)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()
metadata = MetaData()

class Message(Base):
    # 表的名字
    __tablename__ = 'message'

    # 表的结构
    _id = Column(INTEGER, primary_key=True)
    id = Column(INTEGER)
    link = Column(TEXT)
    type = Column(TEXT)  # 文本、图像、视频、音频、语音
    category = Column(TEXT)  # 分类
    text = Column(TEXT)
    video = Column(TEXT)
    photo = Column(TEXT)
    audio = Column(TEXT)
    voice = Column(TEXT)
    date = Column(DATETIME)
    from_id = Column(INTEGER)
    from_chat = Column(INTEGER)


class User(Base):
    # 表的名字
    __tablename__ = 'user'

    # 表的结构
    id = Column(INTEGER, primary_key=True)
    fullname = Column(TEXT)
    username = Column(TEXT)


class Chat(Base):
    # 表的名字
    __tablename__ = 'chat'

    # 表的结构
    id = Column(INTEGER, primary_key=True)
    title = Column(TEXT)
    enable = Column(BOOLEAN)

Base.metadata.create_all(engine)

# 定义索引
index_msg_id = Index('idx_message_id', Message.id)
index_msg_text = Index('idx_message_text', Message.text)
index_msg_from_id = Index('idx_message_from_id', Message.from_id)
index_msg_from_chat = Index('idx_message_from_chat', Message.from_chat)
index_user_fullname = Index('idx_user_fullname', User.fullname)

try:
    index_msg_text.create(bind=engine)
    index_msg_from_id.create(bind=engine)
    index_msg_from_chat.create(bind=engine)
    index_user_fullname.create(bind=engine)
except OperationalError:
    pass
