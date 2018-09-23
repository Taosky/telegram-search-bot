# coding: utf-8
import pymysql
from config import DATABASE, SEARCH_PAGE_SIZE

def init_db():
    db = pymysql.connect(**DATABASE)
    cursor = db.cursor()

    sql = """CREATE TABLE group_message(
             id BIGINT,
             user varchar(100),
             content MEDIUMTEXT,  
             time DATETIME)"""
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def insert_db(msg_id, msg_user, msg_text, msg_time):
    db = pymysql.connect(**DATABASE)
    cursor = db.cursor()
    sql = """INSERT INTO group_message(id,user,content,time) VALUE
     ({},'{}','{}','{}')""".format(msg_id, msg_user, msg_text, msg_time)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def search_db(text, page=1):
    db = pymysql.connect(**DATABASE)
    cursor = db.cursor()
    search_sql = "SELECT * FROM group_message WHERE locate('{}',content) ORDER BY time DESC LIMIT {}, {}".format(text, (
            page - 1) * SEARCH_PAGE_SIZE, SEARCH_PAGE_SIZE)

    count_sql = "SELECT count(id) FROM group_message WHERE locate('{}',content)".format(text)

    try:
        cursor.execute(search_sql)
        messages = cursor.fetchall()
        result = [{'id': row[0], 'user': row[1], 'text': row[2], 'time': row[3]} for row in messages]
        cursor.execute(count_sql)
        count = cursor.fetchall()[0][0]

    except:
        result = []
        count = -1

    db.close()
    return result, count


def get_document(msg_id):
    db = pymysql.connect(**DATABASE)
    cursor = db.cursor()
    sql = "SELECT content,user, time FROM group_message WHERE id={}".format(msg_id)

    try:
        cursor.execute(sql)
        message = cursor.fetchall()[0]
        result = {'text': message[0], 'user': message[1], 'time': message[2]}

    except:
        result = None

    db.close()
    return result
