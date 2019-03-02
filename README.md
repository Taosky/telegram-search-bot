# telegram-search-bot

为了解决Telegram中文搜索相关问题而写的机器人，可以称之为复读机，后面可能添加更多功能。

## Requirements
- VPS/其他主机
- MySQL
- Python
- Web Server （可选）


## Usage
0. 虚拟环境（可选）
1. 安装依赖: `pip install -r requirements.txt`。
2. 修改`config.py`。
3. 轮询模式直接 `python robot.py`启动即可；如果需要Webhook模式，根据情况修改`robot.py`最后几行。

## Develop
#### Handler
`user_handlers`中的模块用于接受群组消息实现一些功能，只需要实现回调函数并添加`handler`即可添加一个模块（默认的`text`已被占用，如需要修改`msg_store.py`）。

#### Jobs
`user_jobs`中的模块用于实现定时任务（间隔运行，定时需手动判断），同上，添加`job_info`即可。
 

### Update

#### 2019-03-02
- 重写了大量代码，更换MYSQL数据库为SQLITE，使用ORM，简化后续的开发及方便用户配置。
- 增加排除ID的配置。
- 增加图片、视频、语音、音频的复读。
- 增加群员获取数据库的命令。
- 存储信息过程中过滤机器人的信息。
- Bot的用户名无需手动设置。
- 修复管理员权限模式下的无权限不能复读的问题。 


