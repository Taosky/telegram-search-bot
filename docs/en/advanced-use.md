## Advanced Usage

### Import History Records

1. Confirm that the group is a **supergroup** before exporting, otherwise importing will prompt an error message.

2. Use Telegram Desktop, Click on the top right corner of the group `Export chat history`, choose JSON (text).

3. `python3 import_history.py`, enter JSON file path ([import_history.py](https://github.com/Taosky/telegram-search-bot/raw/master/extra/import_history.py)).


### Specific users start / stop robots and delete messages

1. Download [.config.json](https://github.com/Taosky/telegram-search-bot/raw/master/extra/.config.json), put it in the previously created configuration folder (`tgbot/`).

2. Modify the second line of the file `.config.json`, change `false` to `true`.

3. Add the user's numeric ID in the 'group.admins' field according to JSON syntax.

**Note that users still need to be administrators in the relevant group to enable, stop robots, and delete messages.**


### UserBot Mode

In this mode, there is no need to pull Bots into the group, but it is necessary to log in to the Telegram account as an intermediary to transmit messages, and the logged in user becomes the command administrator.

1. Login to [https://my.telegram.org/auth](https://my.telegram.org/auth) get Telegram API `ID` and `hash`.

2. Edit`docker-compose.yml`.

```yml
- USER_BOT=1
- USER_BOT_API_ID=1234567
- USER_BOT_API_HASH=xxxxxxxxx

```

3. `docker-compose up -d` to run in background, run `docker exec -it tgbot python userbot.py`, Login after entering username and verification code.

4. Chat with your bot, `/start <GroupID>` to enable bot, `/stop`、`/delete` as the same.


### WebHook
There is not much difference in speed compared to polling mode.

1. Download[Caddyfile](https://github.com/Taosky/telegram-search-bot/raw/master/extra/Caddyfile)、put it in the previously created configuration folder (`tgbot/`).

2. Modify the domain name, path, and other information of the `Caddyfile`, Multiple `route` correspond to multiple bot containers (if needed).

3. Edit `docker-compose.yml`, change `BOT_MODE` value to `webhook`, change `URL_PATH` and `HOOK_URL` .

4. If already have an HTTP (s) server, you can reverse it yourself.