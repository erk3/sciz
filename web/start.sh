#!/bin/bash
( nohup node server.js 2>&1 & echo $! > sciz.pid ) | tee -a server.log &
