import socket
import json
from database import DBSession, Message, User, Chat
from datetime import datetime
import re

TEMP_FILE_NAME = 'history_temp.json'
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


def strip_user_id(id_):
    id_str = str(id_)
    if id_str.startswith('user'):
        return int(id_str[4:])
    return int(id_str)
    

def insert_chat_or_do_nothing(chat_id, title):
    session = DBSession()
    target_chat = session.query(Chat).get(chat_id)
    if not target_chat:
        new_chat = Chat(id=chat_id, title=title, enable=False)
        session.add(new_chat)
        session.commit()
    session.close()


def insert_user_or_do_nothing(user_id, fullname, username):
    session = DBSession()
    target_user = session.query(User).get(user_id)
    if not target_user:
        new_user = User(id=user_id, fullname=fullname, username=username)
        session.add(new_user)
        session.commit()
    session.close()


def insert_messages(chat_id, f):
    fail_count = 0
    fail_messages = []
    success_count = 0

    json_str = ''
    while True:
        line = f.readline()
        if line.startswith('  {'):
            json_str =''
        
        json_str += line

        if line.startswith('  },'):
            json_str = json_str[:len(json_str)-2]
            message = json.loads(json_str)
            if 'from_id' not in message or 'user' not in message['from_id']:
                continue
        
            insert_user_or_do_nothing(
                message['from_id'][4:], message['from'], message['from'])
            if isinstance(message['text'], list):
                msg_text = ''
                for obj in message['text']:
                    if isinstance(obj, dict):
                        msg_text += obj['text']
                    else:
                        msg_text += obj
            else:
                msg_text = message['text']

            if msg_text == '':
                msg_text == '[其他消息]'
            message_date = datetime.strptime(message['date'], '%Y-%m-%dT%H:%M:%S')
            link_chat_id = str(chat_id)[4:]
            from_id = strip_user_id(message['from_id'])
            new_msg = Message(id=message['id'], link='https://t.me/c/{}/{}'.format(link_chat_id, message['id']), text=msg_text, video='', photo='',
                            audio='', voice='', type='text', category='', from_id=from_id, from_chat=chat_id, date=message_date)

            session = DBSession()
            try:
                session.add(new_msg)
                session.commit()
                success_count += 1
            except Exception as e:
                print(e)
                fail_count += 1
                fail_messages.append(str(message))
            session.close()

        if line.startswith(' ]'):
            break
        

    return success_count, fail_count, fail_messages


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5006))
    server.listen(3)
    while True:
        print("listening......")
        sock, adddr = server.accept()
        print('{}已连接'.format(adddr))
        received = sock.recv(BUFFER_SIZE).decode()
        try:
            filename, filesize = received.split(SEPARATOR)
        except ValueError:
            sock.close()
            continue
        filesize = int(filesize)
        receivedsize = 0
        with open(TEMP_FILE_NAME, 'wb') as f:
            while True:
                bytes_read = sock.recv(BUFFER_SIZE)
                f.write(bytes_read)
                receivedsize += BUFFER_SIZE
                if not bytes_read:
                    break
                if receivedsize >= filesize:
                    print('文件接收结束 {} {}MB\n'.format(
                        filename, round(filesize/1024/1024, 2)))
                    break

        f = open(TEMP_FILE_NAME)
        group_name = None
        group_id = None
        supergroup_flag = 0
        while True:
            line = f.readline()
            if '"id":' in line:
                group_id = re.findall('\d+|-\d+', line)[0]
            if '"name"' in line:
                group_name = re.findall(': "(.*)"', line)[0]
            if 'supergroup' in line:
                supergroup_flag = 1
            if 'messages' in line:
                break
        if not group_name or not group_id:
            f.close()
            sock.send('JSON文件解析出错!\n'.encode())
            sock.close()

        sock.send('检查群组信息...\n'.encode())
        if supergroup_flag != 1:
            f.close()
            sock.send('群组非supergroup!停止导入!\n'.encode())
            sock.close()

        sock.send('导入中...'.encode())
        edited_id = int(group_id) if group_id.startswith('-100') else int(
            '-100' + group_id)
        
        print(edited_id)
        insert_chat_or_do_nothing(edited_id, group_name)
        success_count, fail_count, fail_messages = insert_messages(
            edited_id, f)
        f.close()
        fail_text = ''
        for fail_message in fail_messages:
            fail_text += '{}\n\t'.format(fail_message)
        result_text = '\n导入结果\n\t导入群组: {} ({})\n\t导入成功: {}条\n\t导入失败: {}条\n\t{}'.format(
            group_name, group_id, success_count, fail_count, fail_text)
        sock.sendall(result_text.encode())

        sock.send('\nCtrl+C 直接退出即可'.encode())

main()
