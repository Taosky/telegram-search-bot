# telegram-search-bot

一个支持关键词和用户名搜索群聊记录的Telegram Bot

Telegram自带搜索对CJK等语言的支持仅限于整句, 不支持分词查找。本项目通过存储聊天记录, 进行数据库查询, 解决搜索问题。

### 目录

- [功能](#功能)
- [安装](#安装)
- [使用](#使用)
- [更新记录](#更新记录)
- [贡献者](#贡献者)
- [License](#license)

### 功能

- 群聊消息记录和多个关键词搜索（可翻页）
- 定位消息位置
- 带限制的命令控制
- 支持多群组查询（判断是否群成员）
- 支持用户名搜索
- 消息编辑后数据库同步更新

![预览](/preview/preview.png)
![演示](/preview/full.gif)

### 安装

如无特殊需求参照[quick-start.md](quick-start.md)

特殊用法见[advanced-use.md](advanced-use.md)

### 使用

- `@你的Bot @用户名 关键词1 关键词2... 页码`: 用于搜索, 以下是几个搜索的例子

  `@mybot ` 显示全部记录, 默认第 `1`页；

  `@mybot * 2` 显示全部消息记录的第 `2`页；

  `@mybot 天气 3` 搜索包含关键词 `天气`的消息记录并翻至第 `3`页

  `@mybot @Taosky 天气 4` 搜索群成员 `Taosky`（full name关键词）的包含 `天气`关键词的消息记录并翻至第 `4`页
- `/help`: 获取搜索帮助
- `/chat_id`: 获取当前Chat的数字ID


## 贡献者

<a href="https://github.com/Taosky/telegram-search-bot/graphs/contributors"><img src="https://opencollective.com/telegram-search-bot/contributors.svg?width=890&button=false" /></a>

## License

[MIT](LICENSE) © Taosky
