#!/bin/bash
python robot.py &
python json_receive.py &

if [ $USER_BOT -eq 1 ]
    then
        python userbot.py
else
    echo "userbot模式未开启"
fi