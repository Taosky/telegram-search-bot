# telegram-search-bot

一个支持关键词和用户名搜索群聊记录的Telegram Bot

Telegram自带搜索对CJK等语言的支持仅限于整句，不支持关键词（3202年中仍未支持）。本项目通过存储聊天记录，进行数据库查询，解决搜索问题。


### 目录

- [功能](#功能)
- [所需环境](#所需环境)
- [搭建和配置](#搭建和配置)
- [使用方法](#使用方法)
- [其他功能](#其他功能)
- [提示](#提示)
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

![预览](preview/preview.png)
![演示](preview/full.gif)


### 所需环境
- Docker Compose
- 外网/代理环境

---

### 搭建和配置

#### 第一步：创建Bot
0. 与[@botfather](https://t.me/botfather)对话按照步骤创建Bot，记录`token`备用
1. 设置Inline Mode: 选择你的Bot进入Bot Settings，Inline Mode开启，Edit inline placeholder，设置为`@{user} [keywords] {page}`
2. 关闭[Privacy mode](https://core.telegram.org/bots#privacy-mode)，选择你的Bot进入Bot Settings，Group Privacy - Turn off
3. 按照喜好设置其他选项，将Bot添加到Group，设置权限读取发送信息

#### 第二步：配置运行镜像
0. **镜像支持amd64、arm64**
1. 新建目录用于存放配置文件和数据库 `mkdir tgbot && cd tgbot`,
	
	下载相关配置文件和功能文件

	`wget https://github.com/Taosky/telegram-search-bot/raw/master/.config.json.example`

	`wget https://github.com/Taosky/telegram-search-bot/raw/master/Caddyfile`

	`wget https://github.com/Taosky/telegram-search-bot/raw/master/docker-compose.yml`

	`wget https://github.com/Taosky/telegram-search-bot/raw/master/import_history.py`

2. 修改`docker-compose.yml`, 配置运行模式、Bot Token等，配置[特定用户启用停止机器人与删除消息](#特定用户启用停止机器人与删除消息)(可选)
3. 如使用webhook模式，查看Caddyfile进行配置，或手动进行反代设置
4. `docker-compose up -d`后台执行

#### 第三步：群组内启用Bot
0. 首先要确认是否**超级群组(supergroup)**（右键消息有copy link选项），人数较多的群组应该会自动升级，手动升级需要将群组类型设置为`Public`（立即生效，可再改回Private）
1. `/start`: 在目标群内启用（**需管理员/创建者**）

#### 可选：导入历史记录
0. 导出前确认群组为**超级群组(supergroup)**，否则导入将提示错误。
1. Telegram桌面客户端，点击群组右上角`Export chat history`，选择JSON格式(仅文本)
2. `python3 import_history.py`，输入JSON文件路径

---

### 使用方法
0. `@你的Bot @用户名 关键词1 关键词2... 页码`: 用于搜索，以下是几个搜索的例子
   
	 `@mybot ` 显示全部记录，默认第`1`页；
	 
	 `@mybot * 2` 显示全部消息记录的第`2`页；

	 `@mybot 天气 3` 搜索包含关键词`天气`的消息记录并翻至第`3`页

	 `@mybot @Taosky 天气 4` 搜索群成员`Taosky`（full name关键词）的包含`天气`关键词的消息记录并翻至第`4`页


1. `/help`: 获取搜索帮助
2. `/chat_id`: 获取当前Chat的数字ID

---

### 其他功能
#### 特定用户启用停止机器人与删除消息
0. 复制 `.config.json.example` 为 `.config.json`
1. 编辑 `.config.json` 文件的第二行，将 `false` 改为 `true`
2. 按照 json 语法在 `group_admins` 字段内添加用户的数字 ID

**注意，用户仍需在相关群组内为管理员才可以启用、停止机器人与删除消息**


#### 停用和删除记录
1. `/stop`: 在目标群内停用记录和搜索功能，消息记录会保存在数据库（**需管理员/创建者**）
2. `/delete`: 在目标群已停用的情况下，用于删除数据库中的消息记录（**需管理员/创建者**）

---

### 提示
- 如遇查询结果为空，可能是TG的Bug导致，需要把机器人踢出群，重新拉进群
- Inline Mode具有缓存效果，故连续重复搜索可能不会加载新的消息
- 修改Inline Mode placeholder需要重启客户端生效
- Inline Mode可以在任意聊天框使用，可以在收藏夹不公开的进行查询（仍需为群成员才可查询）

--- 

### 更新记录
#### 2023-05-17
- 更新包版本
- 新增按用户搜索功能
- 尝试把文档写的清晰点

#### 2022-11-26
- 优化历史记录导入方式
- 解决Python Json读入内存爆炸问题

#### 2022-11-23 ([#24](https://github.com/Taosky/telegram-search-bot/pull/24))
- 一些优化和整活

#### 2022-11-12 
- 构建镜像到ghcr.io([#22](https://github.com/Taosky/telegram-search-bot/pull/22))
- 一些小改动，完善配置和说明

#### 2022-11-06 
- 修复了导入消息链接无法跳转问题

#### 2022-10-31 ([#21](https://github.com/Taosky/telegram-search-bot/pull/21))
- 支持消息编辑后数据库同步更新

#### 2022-10-30 ([#21](https://github.com/Taosky/telegram-search-bot/pull/21))
- 支持索引频道、匿名管理消息。
- 修复了一些 BUG

#### 2022-10-24 ([#19](https://github.com/Taosky/telegram-search-bot/pull/19))
- 优化了在 inline mode下发送 /help 的逻辑
- 更好的权限控制
- 修改了引用消息时引号的用法


<details>
<summary>more</summary>

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

## 贡献者

<a href="https://github.com/Taosky/telegram-search-bot/graphs/contributors"><img src="https://opencollective.com/telegram-search-bot/contributors.svg?width=890&button=false" /></a>


## License

[MIT](LICENSE) © Taosky
