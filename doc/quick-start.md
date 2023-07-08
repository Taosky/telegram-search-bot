## 快速搭建

以最简单的方式运行本项目, 复杂点的用法详见[advanced-use.md](advanced-use.md)

---

### 创建Bot

1. 与[@botfather](https://t.me/botfather)对话按照步骤创建Bot, 记录`token`备用

2. 设置Inline Mode: 选择你的Bot进入Bot Settings, Inline Mode开启, Edit inline placeholder, 设置为`@{user} [keywords] {page}`

3. 关闭[Privacy mode](https://core.telegram.org/bots#privacy-mode), 选择你的Bot进入Bot Settings, Group Privacy - Turn off

4. 按照喜好设置其他选项, 将Bot添加到Group, 设置权限读取发送信息（userbot模式不需要加入群组, 见[advanced-use.md](advanced-use.md#UserBot模式)）


### 配置运行镜像

1. 新建目录用于存放配置和数据库文件 `mkdir tgbot && cd tgbot`,
	
2. 下载配置文件 
	`wget https://github.com/Taosky/telegram-search-bot/raw/master/extra/docker-compose.yml`

3. 修改`docker-compose.yml`中的`BOT_TOKEN=xxxx:xxxxx`为上一步获取的token, 其余内容无需修改

4. `docker-compose up -d`后台执行

5. 使用`docker-compose pull` 和 `docker-compose up -d --remove-orphans`可更新到最新的镜像 (建议先查看更新内容)


### 群组内启用Bot

1. 首先要确认是否**超级群组(supergroup)**（右键消息有copy link选项）, 人数较多的群组应该会自动升级, 手动升级需要将群组类型设置为`Public`（立即生效, 可再改回Private）

2. `/start`: 在目标群内启用（**需管理员/创建者**）

3. 如需检索历史记录, 见[advanced-use.md](advanced-use.md#导入历史记录)

---


### 其他命令
1. `/stop`: 在目标群内停用记录和搜索功能, 消息记录会保存在数据库（**需管理员/创建者**）

2. `/delete`: 在目标群已停用的情况下, 用于删除数据库中的消息记录（**需管理员/创建者**）


### 提示
- 如遇查询结果为空, 可能是TG的Bug导致, 需要把机器人踢出群, 重新拉进群
- Inline Mode具有缓存效果, 故连续重复搜索可能不会加载新的消息
- 修改Inline Mode placeholder需要重启客户端生效
- Inline Mode可以在任意聊天框使用, 可以在收藏夹不公开的进行查询（仍需为群成员才可查询）