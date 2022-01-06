import telegram

def set_bot_commands(context: telegram.ext.CallbackContext):
    commands = [('help','获取使用帮助'), ('chat_id','获取当前聊天的ID，即Group ID或User ID'),('start','启用Bot(开始记录检索聊天)')]
    context.bot.set_my_commands(commands)
