# coding: utf-8
import sqlite3

conn = sqlite3.connect('bot.db')
cur = conn.cursor()

addColumn = "ALTER TABLE Message ADD COLUMN link TEXT"

print('更新数据表...')
cur.execute(addColumn)

print('完成')
