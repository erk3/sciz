#!/usr/bin/env bash

# WARNING: python virtualenv must be created as follow before running this script
# git clone https://github.com/hangoutsbot/hangoutsbot.git
# EDIT hangoutsbot/requirements.txt and delete plugins dependencies and delete version constraint of aiohttp
# virtualenv -p python3 $DIR/venv
# source $DIR/venv/bin/activate
# pip3 install -r $DIR/hangoutsbot/requirements.txt
# pip3 install -r $DIR/requirements.txt
# deactivate

# AT FIRST START
# Pass the '/bot botalias /sciz' command as admin to the bot

# Get CWD fr this script
DIR="$(cd "$(dirname "$0")" && pwd)"

# Check for venv directory
if [ ! -d "$DIR/venv" ]; then
	echo "No python virtualenv!"
	exit 1
fi

# Copy the plugin
cp $DIR/sciz_bot_hangouts.py $DIR/hangoutsbot/hangupsbot/plugins/sciz.py

# Start the bot with our configuration files
$DIR/venv/bin/python3 $DIR/hangoutsbot/hangupsbot/hangupsbot.py --cookies $DIR/cookies.json --memory $DIR/memory.json --config $DIR/config.json
