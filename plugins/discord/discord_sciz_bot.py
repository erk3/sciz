#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import argparse, configparser, codecs, sys
import asyncio, aiohttp, json
from discord import Game
from discord.ext.commands import Bot

# Consts
DEFAULT_CHARSET     = "utf-8"
CONF_SECTION_BOT    = "bot"
CONF_SECTION_SCIZ   = "sciz"

# Main
if __name__ == '__main__':

    # Command line arguments handling
    parser = argparse.ArgumentParser(
            description='Bot SCIZ pour Discord',
            epilog='From Põm³ with love')
    
    parser.add_argument('-c', '--conf',
            metavar='CONFIG_FILE', type=str, default='conf.ini',
            help='specify the .ini configuration file')
    
    args = parser.parse_args()
  
    # Load the configuration file
    config = configparser.RawConfigParser()
    with codecs.open(args.conf, 'r', DEFAULT_CHARSET) as fp:
        config.readfp(fp)

    # Get the bot conf
    token = config.get(CONF_SECTION_BOT, "token")
    channel_id = config.get(CONF_SECTION_BOT, "channel_id")
    prefix = config.get(CONF_SECTION_BOT, "prefix")
    
    # Get the sciz conf
    hook_url = config.get(CONF_SECTION_SCIZ, "hook_url")
    jwt = config.get(CONF_SECTION_SCIZ, "jwt")
    refresh = config.getint(CONF_SECTION_SCIZ, "refresh")
    
    # Create the bot
    client = Bot(command_prefix=prefix)

    # Define bot events
    @client.event
    async def on_ready():
        await client.change_presence(game=Game(name="with bats"))
        print("Logged in as " + client.user.name)

    # Define bot commands
    @client.command()
    async def request(args):
        arg1 = arg2 = arg3 = None
        sargs = args.split(' ') if args else list(args)
        arg1 = sargs[0] if len(sargs) > 0 else ''
        arg2 = sargs[1] if len(sargs) > 1 else ''
        arg3 = sargs[2] if len(sargs) > 2 else ''
        async with aiohttp.ClientSession(headers={'Authorization': jwt}) as session:
            raw_response = await session.post(hook_url, data={'arg1': arg1, 'arg2': arg2, 'arg3': arg3})
            response = await raw_response.text()
            response = json.loads(response)
            raw_response.release()
            await client.say(response['message'])

    # Define bot routine
    async def fetch_sciz(channel_id, hook_url, jwt, refresh):
        await client.wait_until_ready()
        while not client.is_closed:
            await asyncio.sleep(refresh)
            try:
                async with aiohttp.ClientSession(headers={'Authorization': jwt}) as session:
                    raw_response = await session.get(hook_url)
                    response = await raw_response.text()
                    response = json.loads(response)
                    raw_response.release()
                    for r in response:
                        await client.send_message(client.get_channel(channel_id), r['notif'])
            except Exception as e:
                print(e, file=sys.stderr)

    # Start the bot
    client.loop.create_task(fetch_sciz(channel_id, hook_url, jwt, refresh))
    client.run(token)

