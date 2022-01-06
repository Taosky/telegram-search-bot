
# telegram-search-bot

为了解决Telegram中文搜索相关问题而写的机器人，可以称之为复读机，后面可能添加更多功能。

![搜索](https://raw.githubusercontent.com/Taosky/telegram-search-bot/master/preview/search.png)
![复读](https://raw.githubusercontent.com/Taosky/telegram-search-bot/master/preview/link-mode.png)


## Feature
- 消息记录、搜索、复读定位（主要功能，解决中文搜索的问题）。
- 定时任务（有能力可根据需要修改，目前是报时，删除文件可取消）。
- 具有定时撤回、排除ID等额外配置。

## Requirements
- Docker部署(外网/代理)

## Usage

### 机器人创建设置
0. 与[@botfather](https://t.me/botfather)对话按照步骤创建Bot，记录`token`备用。
1. 设置Inline Mode: 选择你的Bot进入Bot Settings，Inline Mode开启，Edit inline placeholder，发送`[keywords] {page}`。
2. 关闭[Privacy mode](https://core.telegram.org/bots#privacy-mode)，选择你的Bot进入Bot Settings，Group Privacy - Turn off。
3. 按照喜好设置其他选项，将Bot添加到Group，设置权限读取发送信息。

### Docker构建运行
0. `git clone https://github.com/Taosky/telegram-search-bot.git && cd telegram-search-bot`
1. `docker build -t taosky/telegram-search-bot:v2 .`
2. 修改`映射路径`、`token`、`代理（可删掉）`，执行
````bash
    sudo docker run -d -v /home/xxx/telegram-search-bot/bot.db:/app/bot.db \
    -e BOT_TOKEN=12345:abcdefg \
    -e https_proxy=http://127.0.0.1:7890 \
    --network host \
    --restart always \
    --name tgbot \
    taosky/telegram-search-bot:v2
````


### 群内使用
- `/start`启用
- `@your_bot [keywords] {page}`: 用于搜索，`@`无参数为显示历史消息，此时翻页用`* {page}`。
- `/help`: 获取使用帮助。

### <del导入历史记录</del>

## Tips
- Inline Mode具有缓存效果，故连续重复搜索可能不会加载新的消息。
- Inline Mode placeholder更新需要重启客户端。
 

## Update
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
- 新增原消息链接模式，超级群组可用，通过点击链接定位消息，见图片。
![链接](https://raw.githubusercontent.com/Taosky/telegram-search-bot/master/preview/link-mode.png)

#### 2019-04-27
- 添加代理选项（酸酸乳的socks5貌似不行，http可用）

#### 2019-04-02
- 修复重复报时。
- 完善README。

#### 2019-03-03
- 修复搜索的页码问题。

#### 2019-03-02
- 重写了大量代码，更换MYSQL数据库为SQLITE，使用ORM，简化后续的开发及方便用户配置。
- 增加排除ID的配置。
- 增加图片、视频、语音、音频的复读。
- 增加群员获取数据库的命令。
- 存储信息过程中过滤机器人的信息。
- Bot的用户名无需手动设置。
- 修复管理员权限模式下的无权限不能复读的问题。 


