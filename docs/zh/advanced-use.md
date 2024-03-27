## 高级用法

### 导入历史记录

1. 导出前确认群组为**超级群组(supergroup)**, 否则导入将提示错误

2. Telegram桌面客户端, 点击群组右上角`Export chat history`, 选择JSON格式(仅文本)

3. `python3 import_history.py`, 输入JSON文件路径 ([import_history.py](https://github.com/Taosky/telegram-search-bot/raw/master/extra/import_history.py))


### 特定用户启用停止机器人与删除消息

1. 下载[.config.json](https://github.com/Taosky/telegram-search-bot/raw/master/extra/.config.json)放入在此前创建的配置文件夹内 (`tgbot/`)

2. 编辑 `.config.json` 文件的第二行, 将 `false` 改为 `true`

3. 按照 json 语法在 `group_admins` 字段内添加用户的数字 ID

**注意, 用户仍需在相关群组内为管理员才可以启用、停止机器人与删除消息**


### UserBot模式

此模式下不需要拉Bot进群, 但是需要登陆Telegram账号作为中间商传递消息, 登陆用户成为命令管理员

1. 登陆 [https://my.telegram.org/auth](https://my.telegram.org/auth) 获取Telegram官方的API `ID` 和 `hash`

2. 修改`docker-compose.yml`

```yml
- USER_BOT=1
- USER_BOT_API_ID=1234567
- USER_BOT_API_HASH=xxxxxxxxx

```

3. `docker-compose up -d`后台执行后, 手动执行`docker exec -it tgbot python userbot.py`, 输入用户名和验证码后登陆

4. 与bot对话, 使用`/start 群组ID`启用, `/stop`、`/delete`同理


### WebHook的配置

实测和polling模式速度区别不大, 有需要可以使用
1. 下载[Caddyfile](https://github.com/Taosky/telegram-search-bot/raw/master/extra/Caddyfile)、放入在此前创建的配置文件夹内 (`tgbot/`)

2. 修改`Caddyfile`的域名、路径等信息, 其中多个`route`, 对应多个bot容器（如有需要的话）

3. 修改`docker-compose.yml`, `BOT_MODE`值改为`webhook`, `URL_PATH`和`HOOK_URL`对照`Caddyfile`修改, 取消Caddy部分的注释如创建多个bot容器, 记得修改端口映射防止冲突

4. 如已有http(s)服务器, 可自行反代