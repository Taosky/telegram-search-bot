# coding: utf-8
from sqlalchemy import Column, INTEGER, TEXT, DATETIME, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

engine = create_engine('sqlite:///bot.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool,
                       echo=False)
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