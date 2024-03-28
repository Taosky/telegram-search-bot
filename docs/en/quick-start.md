## Quick Start

Run this project in the simplest way possible, please refer to [advanced-use.md](advanced-use.md)  for the usage of complex point.

---

### Create Bot

1. Chat with [@botfather](https://t.me/botfather)Follow the steps to create a bot and record the `token`.

2. Enable Inline Mode: Go to Bot Settings of your bot, change `Inline Mode` option to `enable`, Edit inline placeholder, type `@{user} [keywords] {page}`.

3. Disable [Privacy mode](https://core.telegram.org/bots#privacy-mode), Go to Bot Settings of your bot,`Group Privacy` - `Turn off`

4. Set other options according to preferences, add Bot to Group, set permissions to read and send messages（userbot mode does not require joining a group, see [advanced-use.md](advanced-use.md#UserBot-Mode)）


### Configure Docker Compose

1. Create a new directory to store configuration and database files `mkdir tgbot && cd tgbot`
	
2. Download Configuration File 
	`wget https://github.com/Taosky/telegram-search-bot/raw/master/extra/docker-compose.yml`

3. Edit `docker-compose.yml`, change `BOT_TOKEN` value to your bot's token, change `LANG` to `en_US` for English version.

4. `docker-compose up -d` to run in background.

5. If you want to update , run `docker-compose pull` to get the latest image, then run `docker-compose up -d --remove-orphans` to recreate and run container (checking the updated content first)


### Enable Bot in Group

1.Firstly, it is necessary to confirm whether your group is a **supergroup** (can see a copy link option in the right-click message). 

	Groups with a large number of people should be automatically upgraded to supergroup, and manual upgrading requires setting the group type to 'Public' (effective immediately, can be changed back to 'Private')

2. Ensure that the bot has permission to read messages.

3. `/start`: Enable bot in current group (**need admin/creator send this command**). For groups with thousands of members, it may be necessary to grant bot administrator privileges.

4. The bot will only record chat messages after enabled, If want to import history, see [advanced-use.md](advanced-use.md#Import-History-Records)

5. If the bot not work, try kicking the bot and adding to group again. See [#Tips](#tips) for more info.

---


### Other Commands
1. `/stop`: Deactivate recording and search functions within the target group, and message records will be still saved in the database (**need admin/creator**).

2. `/delete`: Used to delete message records in the database when the target group has been deactivated (**need admin/creator**).


### Tips
- If the query result is empty, it may be caused by a bug in Telegram, and the robot needs to be kicked out of the group and added back into the group.

- The inline mode has a caching effect, so repeated searches in a short period of time may not load new messages.

- Modifying the Inline Mode placeholder requires restarting the client to take effect

- Inline Mode can be used in any chat box and can be queried in `Saved Messages` that are not publicly available (it still needs the target group member)