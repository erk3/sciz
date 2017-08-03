# -*- coding: utf-8 -*-
import asyncio, datetime, logging, time
from asyncio.subprocess import PIPE
import hangups
import plugins
import threadmanager

logger = logging.getLogger(__name__)

internal = {}

def _initialise(bot):
    config_sciz_events = bot.get_config_option("sciz_events") or {}
    if not config_sciz_events:
        return

    _new_config = {}
    if isinstance(config_sciz_events, list):
        if "refresh_time" in config_sciz_events:
            _new_config["refresh_time"] = 30
        if "conv_title" in config_sciz_events:
            _new_config["conv_title"] = "SCIZ"
        if "cmd" in config_sciz_events:
            _new_config["cmd"] = ["/usr/bin/false"]
        config_sciz_events = _new_config

    logger.info("timing {}".format(config_sciz_events))

    plugins.start_asyncio_task(sciz_events, config_sciz_events)


@asyncio.coroutine
def sciz_events(bot, config_sciz_events):
 
    last_run = [0, 0]

    while True:
        timestamp = time.time()

        yield from asyncio.sleep(5)

        if "refresh_time" in config_sciz_events and timestamp - last_run[0] > config_sciz_events["refresh_time"]:
            for conv in bot.conversations.catalog:
                if bot.conversations.catalog[conv]["title"] == config_sciz_events["conv_title"]:
                    exe = config_sciz_events["cmd"]
                    exe = tuple(exe)
                    proc = yield from asyncio.create_subprocess_exec(*exe, stdout=PIPE, stderr=PIPE)
                    (stdout_data, stderr_data) = yield from proc.communicate()
                    stdout_str = stdout_data.decode(encoding='utf-8').rstrip()
		    #stderr_str = stderr_data.decode(encoding='ISO-8859-1').rstrip()
                    if len(stdout_str) > 0:
                        yield from bot.coro_send_message(conv, stdout_str)
            last_run[0] = timestamp
