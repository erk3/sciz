# IMPORTS
import sys, asyncio, aiohttp, json, redis, re, logging
import hangups, plugins, threadmanager

# CONSTS
DEFAULT_CHARSET = 'utf-8'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1
SCIZ_URL_BASE = 'https://www.sciz.fr/api/hook'
#SCIZ_URL_BASE = 'http://127.0.0.1:8080/api/hook'
SCIZ_URL_EVENTS = SCIZ_URL_BASE + '/events'
SCIZ_URL_REQUEST = SCIZ_URL_BASE + '/request'
SCIZ_INTERVAL = 1

# GLOBALS
logger = logging.getLogger(__name__)
internal = {}

# Connect to REDIS
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Initialize plugin
def _initialise(bot):
    # Register the commands
    plugins.register_user_command(["register", "unregister", "req"])
    # Start the events pulling task
    plugins.start_asyncio_task(get_events)

# Register routine
async def register(bot, event, *args):
    if len(args) < 1:
        await bot.coro_send_message(event.conv_id, '/sciz register <JWT>')
    else:
        r.set(event.conv_id, args[0])
        r.save()
        await bot.coro_send_message(event.conv_id, 'Hook enregistré pour cette conversation')

# Unregister routine
async def unregister(bot, event, *args):
    r.delete(event.conv_id)
    r.save()
    await bot.coro_send_message(event.conv_id, 'Hook supprimé pour cette conversation')

# Request routine
async def req(bot, event, *args):
    args = ' '.join(args)
    jwt = r.get(event.conv_id)
    if jwt is None:
        await bot.coro_send_message(event.conv_id, 'Pas de hook enregistré pour ce canal')
        return
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
                        await bot.coro_send_message(event.conv_id, m)
                        i += 1
            raw_response.release()
    except Exception as e:
        print(e, file=sys.stderr)

# Get events routine
@asyncio.coroutine
async def get_events(bot):
    while True:
        await asyncio.sleep(SCIZ_INTERVAL)
        try:
            for conv_id in r.keys('*'):
                jwt = r.get(conv_id)
                async with aiohttp.ClientSession(headers = {'Authorization': jwt.decode(DEFAULT_CHARSET)}) as session:
                    raw_response = await session.get(SCIZ_URL_EVENTS)
                    if raw_response.status == 200:
                        response = await raw_response.text()
                        response = json.loads(response)
                        if 'events' in response:
                            for e in response['events']:
                                if 'message' in e:
                                    await bot.coro_send_message(conv_id, e['message'])
                    raw_response.release()
        except Exception as e:
            print(e, file=sys.stderr)

