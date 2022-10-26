# telegram-search-bot

一个支持CJK聊天记录搜索的Telegram Bot

Telegram自带搜索对CJK的支持仅限于整句，不支持分词。本项目通过存储聊天记录，进行数据库查询，解决搜索问题。


## Nav

- [Feature](#eature)
- [Requirements](#requirements)
- [Usage](#usage)
	- [Create Bot](#create-bot)
	- [Docker Build And Run](#docker-build-and-run)
	- [Use In Group](#use-in-group)
	- [Import Message History](#import-message-history)
- [Tips](#tips)
- [Update Records](#update-records)
- [Contributors](#contributors)
- [License](#license)

## Feature

- 消息记录搜索
- 消息链接定位
- 支持多个群组

![搜索](https://raw.githubusercontent.com/Taosky/telegram-search-bot/master/preview/search.png)

![复读](https://raw.githubusercontent.com/Taosky/telegram-search-bot/master/preview/link-mode.png)

## Requirements
- Docker部署(外网/代理环境)

## Usage

### Create Bot
0. 与[@botfather](https://t.me/botfather)对话按照步骤创建Bot，记录`token`备用
1. 设置Inline Mode: 选择你的Bot进入Bot Settings，Inline Mode开启，Edit inline placeholder，设置为`[keywords] {page}`
2. 关闭[Privacy mode](https://core.telegram.org/bots#privacy-mode)，选择你的Bot进入Bot Settings，Group Privacy - Turn off
3. 按照喜好设置其他选项，将Bot添加到Group，设置权限读取发送信息

### Docker Build And Run
0. `git clone https://github.com/Taosky/telegram-search-bot.git && cd telegram-search-bot`
1. `docker build -t taosky/telegram-search-bot:v2 .`
2. 修改`docker-compose.yml`, 配置运行模式、Bot ID、映射等
3. 如使用webhook模式，查看Caddyfile进行配置，或手动进行反代设置
4. `docker-compose up -d`后台执行

### Use In Group
0. 首先要确认是否**超级群组(supergroup)**（右键消息有copy link选项），人数较多的群组应该会自动升级，手动升级需要将群组类型设置为`Public`（立即生效，可再改回Private）
1. `/start`: 在目标群内启用（**需管理员/创建者**）。
2. `@your_bot [keywords] {page}`: 用于搜索，`@`无参数为显示历史消息，此时翻页用`* {page}`
3. `/help`: 获取搜索帮助。
4. `/chat_id`: 获取当前Chat的数字ID
5. `/stop`: 在目标群内停用记录和搜索功能，消息记录会保存在数据库（**需管理员/创建者**）
6. `/delete`: 在目标群已停用的情况下，用于删除数据库中的消息记录（**需管理员/创建者**）

### Import Message History
0. 导出前确认群组为**超级群组(supergroup)**，否则导入将提示错误。
1. Telegram桌面客户端，点击群组右上角`Export chat history`，选择JSON格式(仅文本)
2. `http://127.0.0.1:5006`，选择导出的JSON文件上传。

### 只允许特定用户启用、停止机器人与删除消息
0. 复制 `.config.json.example` 为 `.config.json`
1. 编辑 `.config.json` 文件的第二行，将 `false` 改为 `true`
2. 按照 json 语法在 `group_admins` 字段内添加用户的数字 ID。

**注意，用户仍需在相关群组内为管理员才可以启用、停止机器人与删除消息**

## Tips
- Inline Mode具有缓存效果，故连续重复搜索可能不会加载新的消息
- Inline Mode placeholder修改需要重启客户端
 
## Update Records
#### 2022-10-24
- 优化了在 inline mode下发送 /help 的逻辑
- 更好的权限控制
- 修改了引用消息时引号的用法

#### 2022-06-15
- 修复导入历史记录Chat ID不匹配的问题
- 修复Message ID重复的问题
- 修复导入历史记录报错的问题

#### 2022-02-17
- 记录和搜索支持多个群组（数据库有变化，要重新导入历史记录）
- 搜索时用户名后显示"@群组"用于区分消息来源
- 在搜索时，根据用户是否为群组成员筛选搜索结果

#### 2022-02-13
- WebHook模式及docker-compose
- 修复inline mode没有鉴权问题
- 修复text为空时报错问题

#### 2022-02-08
- Web界面可导入历史消息（5006端口）

#### 2022-01-06
- Docker化

<details>
<summary>more</summary>

#### 2021-09-20
- 更新python-telegram-bot库
- 重构代码，简化操作

#### 2021-07-03
- 支持多关键词搜索

#### 2021-02-04
- 修复inline mode部分关键词结果不显示问题（特定字符导致的解析错误）

#### 2020-01-11 (V1.0)
- 新增导入历史消息记录。（仅初始化数据库可用，且无法定位）
- 新增原消息链接模式，超级群组可用，通过点击链接定位消息

#### 2019-04-27
- 添加代理选项（酸酸乳的socks5貌似不行，http可用）

#### 2019-04-02
- 修复重复报时。
- 完善README。

#### 2019-03-03
- 修复搜索的页码问题。

#### 2019-03-02
- 重写了大量代码，更换MYSQL数据库为SQLITE，使用ORM，简化后续的开发及方便用户配置。
- 增加排除ID的配置
- 增加图片、视频、语音、音频的复读
- 增加群员获取数据库的命令
- 存储信息过程中过滤机器人的信息
- Bot的用户名无需手动设置
- 修复管理员权限模式下的无权限不能复读的问题。

</details>

## Contributors

<a href="https://github.com/Taosky/telegram-search-bot/graphs/contributors"><img src="https://opencollective.com/telegram-search-bot/contributors.svg?width=890&button=false" /></a>


## License

[MIT](LICENSE) © Taosky
