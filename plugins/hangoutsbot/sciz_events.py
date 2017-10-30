#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio, datetime, logging, time, requests
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
        if "jwt" in config_sciz_events:
            _new_config["jwt"] = ["JWT YourJWTForSCIZHangoutBot"]
        if "url" in config_sciz_events:
            _new_config["url"] = ["http://your.sciz.domain/api/bot/hooks"]
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
                    r = requests.get(config_sciz_events["url"], headers={'Authorization': config_sciz_events["jwt"]})
                    if r.status_code == requests.codes.ok:
                        for n in r.json():
                            if n['notif']:
                                yield from bot.coro_send_message(conv, n['notif'])
            last_run[0] = timestamp
