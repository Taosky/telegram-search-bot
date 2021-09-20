from telegram.ext import CommandHandler

from utils import read_config, write_config


def start(update, context):
    config = read_config()
    msg_text = ''
    if not update.message.chat.type == 'supergroup':
        msg_text = '仅在超级群组中可用'
    else:
        group_id = update.effective_chat.id
        if not config or config['group_id'] != group_id:
            write_config({'group_id':group_id})
            msg_text = '成功启用'
        else:
            msg_text = '前期已启用, 删除程序目录下.config.json文件重置'

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg_text)


# Command: start bot
handler = CommandHandler('start', start)