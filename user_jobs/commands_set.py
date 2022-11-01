import telegram


def set_bot_commands(context: telegram.ext.CallbackContext):
    commands = [
        ('help', '获取搜索帮助'),
        ('chat_id', '获取当前聊天的ID，即Group ID或User ID'),
        ('start', '在当前群组启用Bot(开始记录检索聊天)'),
        ('stop', '在当前群组停用Bot'),
        ('delete', '删除已停用的聊天记录')
    ]

    context.bot.set_my_commands(commands)
