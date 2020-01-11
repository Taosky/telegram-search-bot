# coding: utf-8

# BotFather提供的Token
TOKEN = 'xxxxxxx'

# 需要使用机器人的群（由于Inline Mode获取ID的问题，目前一个机器人只能用于一个群）
GROUP_ID = -31415926

# 排除ID列表
EXCEPT_IDS = [123456, ]

# 每页搜索结果数量
SEARCH_PAGE_SIZE = 10

# 一定时间自动撤回Bot发出的消息
AUTO_DELETE = True
SENT_DELETE_DELAY = 70

# 原消息链接（此模式无命令，消息由用户发出，需超级群组）
LINK_MODE = False
LINK_ID = 12312313  # https://t.me/c/12312313/xxxxx（自行右键消息复制链接查看，取中间数字）

# 代理
PROXY = False
PROXY_URL = 'http://127.0.0.1:1080'
