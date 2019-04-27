# telegram-search-bot

为了解决Telegram中文搜索相关问题而写的机器人，可以称之为复读机，后面可能添加更多功能。

写了一篇博客文章记录了一下过程，供参考：https://mou.science/2018/09/21/telegram-robot/

![搜索](https://raw.githubusercontent.com/Taosky/telegram-search-bot/master/preview/search.png)
![复读](https://raw.githubusercontent.com/Taosky/telegram-search-bot/master/preview/repeat.png)


## Feature
- 消息记录、搜索、复读定位（主要功能，解决中文搜索的问题）。
- 定时任务（有能力可根据需要修改，目前是报时，删除文件可取消）。
- 具有定时撤回、排除ID等额外配置。

## Commands
- `@your_bot {keyword} {page}`: 用于搜索，`@`无参数为显示历史消息，此时翻页用`* {page}`，无页码默认第一页，`pagesize`可自行设置。
- `/chatid`: 获取当前聊天的ID，即Group ID或User ID，此功能可在多个聊天中独立使用。
- `/database`: 获取聊天记录的SQLite数据库文件。
- `/help`: 获取使用帮助。

## Requirements
- VPS/其他主机
- Python环境
- Web Server（可选，WebHook模式需要）

## Usage

### 代码部署运行
0. 虚拟环境（可选）
1. 安装依赖: `pip install -r requirements.txt`。
2. 修改`config.py`。
3. 轮询模式直接 `python robot.py`启动即可；如果需要WebHook模式，根据情况修改`robot.py`最后几行，并设置好`Nginx`等Web Server，比较麻烦请自行了解。


### 机器人创建设置
0. 与[@botfather](https://t.me/botfather)对话按照步骤创建Bot，记录`token`备用。
1. 设置Inline Mode: 选择你的Bot进入Bot Settings，Inline Mode开启，Edit inline placeholder，发送`{keyword} {page}`。
2. 关闭[Privacy mode](https://core.telegram.org/bots#privacy-mode)，选择你的Bot进入Bot Settings，Group Privacy - Turn off。
3. 按照喜好设置其他选项，将Bot添加到Group。
4. 修改`config.py`中`TOKEN`运行代码，在Group中使用`/chatid`获得`Group ID`，修改`config.py`中的`GROUP_ID`，重新运行代码即可正常使用。

## Tips
- Inline Mode具有缓存效果，故连续重复搜索可能不会加载新的消息。
- Inline Mode placeholder更新需要重启客户端。
- 数据库连续获取并不会更新。


## Develop
#### Handler
`user_handlers`中的模块用于接受群组消息实现一些功能，只需要实现回调函数并添加`handler`即可添加一个模块（默认的`text`已被占用，如需要修改`msg_store.py`）。

#### Jobs
`user_jobs`中的模块用于实现定时任务（间隔运行，定时需手动判断），同上，添加`job_info`即可。
 

### Update

#### 2019-04-27
- 添加代理选项（酸酸乳的socks5貌似不行，http可用）

#### 2019-04-02
- 修复重复报时。
- 完善README。

#### 2019-03-03
修复搜索的页码问题。

#### 2019-03-02
- 重写了大量代码，更换MYSQL数据库为SQLITE，使用ORM，简化后续的开发及方便用户配置。
- 增加排除ID的配置。
- 增加图片、视频、语音、音频的复读。
- 增加群员获取数据库的命令。
- 存储信息过程中过滤机器人的信息。
- Bot的用户名无需手动设置。
- 修复管理员权限模式下的无权限不能复读的问题。 


