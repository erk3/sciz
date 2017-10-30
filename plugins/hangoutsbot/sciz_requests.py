#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import os, re, logging, asyncio, requests
from datetime import datetime, timedelta, timezone
from commands import command
import plugins

logger = logging.getLogger(__name__)

def _initialize(bot):
    config_sciz_requests = bot.get_config_option("sciz_requests") or {}
    if not config_sciz_requests:
        return

    _new_config = {}
    if isinstance(config_sciz_requests, list):
        if "jwt" in config_sciz_requests:
            _new_config["jwt"] = ["JWT YourJWTForSCIZHangoutBot"]
        if "url" in config_sciz_requests:
            _new_config["url"] = ["http://your.sciz.domain/api/bot/hooks"]
        config_sciz_requests = _new_config
    logger.info("timing {}".format(config_sciz_requests))

    # Override the load logic and register our commands directly
    cmds = config_sciz_requests.get("commands")
    for cmd, cnf in cmds.items():
        command.register(_spawn, admin=True, final=True, name=cmd)
    logger.info("sciz_requests - %s", ", ".join(['*' + cmd for cmd in cmds]))
    plugins.register_admin_command(list(cmds))

def _spawn(bot, event, *args):
    """Execute a generic command"""
    config = bot.get_config_suboption(event.conv_id, "sciz_requests")
    cmd_config = config["commands"][event.command_name.lower()]

    arg1 = arg2 = arg3 = None
    sargs = cmd_config.get("args").split(' ') if cmd_config.get("args") else list(args)
    arg1 = sargs[0] if len(sargs) > 0 else None
    arg2 = sargs[1] if len(sargs) > 1 else None
    arg3 = sargs[2] if len(sargs) > 2 else None

    logger.info("%s requesting...", event.user.full_name)

    environment = {
        'HANGOUT_USER_CHATID': event.user_id.chat_id,
        'HANGOUT_USER_FULLNAME': event.user.full_name,
        'HANGOUT_CONV_ID':  event.conv_id,
        'HANGOUT_CONV_TAGS': ','.join(bot.tags.useractive(event.user_id.chat_id,
                                                          event.conv_id))
    }
    environment.update(dict(os.environ))

    r = requests.post(config["url"], headers={'Authorization': config["jwt"]}, data=(('arg1', arg1), ('arg2', arg2), ('arg3', arg3)))
    if (r.status_code == requests.codes.ok) and r.json() and r.json()['message']:
        yield from bot.coro_send_message(event.conv_id, r.json()['message'])

