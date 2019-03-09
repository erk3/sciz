#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import sys, asyncio, aiohttp, json, redis, re
from discord import Game
from discord.ext.commands import Bot

# CONSTS
DEFAULT_CHARSET = 'utf-8'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
DISCORD_BOT_TOKEN = ''
DISCORD_PREFIX = '!'
SCIZ_URL_BASE = 'https://www.sciz.fr/api/hook'
#SCIZ_URL_BASE = 'http://127.0.0.1:8080/api/hook'
SCIZ_URL_EVENTS = SCIZ_URL_BASE + '/events'
SCIZ_URL_REQUEST = SCIZ_URL_BASE + '/request'
SCIZ_INTERVAL = 1

# MAIN
if __name__ == '__main__':

    # Connect to REDIS
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    # Create the bot
    bot = Bot(command_prefix=DISCORD_PREFIX)

    # Define bot events
    @bot.event
    async def on_ready():
        await bot.change_presence(game=Game(name='Mountyhall'))
        print('Logged in as ' + bot.user.name)

    # Define bot commands
    @bot.command(name='sciz', pass_context=True)
    async def _sciz_request(ctx, *args):
        # Get useful things
        args = ' '.join(args).strip()
        channel_id = ctx.message.channel.id
        jwt = r.get(channel_id)
        # Handle ping
        if args == 'ping':
            await bot.say('pong')
            return
        # Handle unregister
        if args == 'unregister':
            r.delete(channel_id)
            r.save()
            await bot.say('Hook supprimé pour ce canal')
            return
        # Handle register
        m = re.search('register (.*)', args)
        if m is not None:
            r.set(channel_id, m.group(1))
            r.save()
            await bot.say('Hook enregistré pour ce canal')
            return
        # Handle no JWT
        if jwt is None:
            await bot.say('Pas de hook enregistré pour ce canal')
            return
        # Handle request
        try:
            async with aiohttp.ClientSession(headers = {'Authorization': jwt.decode(DEFAULT_CHARSET)}) as session:
                raw_response = await session.post(SCIZ_URL_REQUEST, json={'req': args})
                if raw_response.status == 200:
                    response = await raw_response.text()
                    response = json.loads(response)
                    if 'message' in response:
                        i, l = 0, len(response['message'])
                        for m in response['message']:
                            if i < l - 1:
                                m += "\n-\n"
                            await bot.say(m)
                            i += 1
                raw_response.release()
        except Exception as e:
            print(e, file=sys.stderr)
            pass

    # Define bot routine (SCIZ events)
    async def _sciz_fetch_events(url, interval):
        await bot.wait_until_ready()
        while not bot.is_closed:
            await asyncio.sleep(interval)
            try:
                for channel_id in r.keys('*'):
                    jwt = r.get(channel_id)
                    async with aiohttp.ClientSession(headers = {'Authorization': jwt.decode(DEFAULT_CHARSET)}) as session:
                        raw_response = await session.get(url)
                        if raw_response.status == 200:
                            response = await raw_response.text()
                            response = json.loads(response)
                            if 'events' in response:
                                for e in response['events']:
                                    if 'message' in e:
                                        await bot.send_message(bot.get_channel(channel_id.decode()), e['message'])
                        raw_response.release()
            except Exception as e:
                print(e, file=sys.stderr)
                pass

    # Start the bot
    task = bot.loop.create_task(_sciz_fetch_events(SCIZ_URL_EVENTS, SCIZ_INTERVAL))
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        task.cancel()

