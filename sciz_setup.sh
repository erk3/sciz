#!/bin/bash

PATH_SCIZ_CONF=confs/sciz.ini
PATH_WEB_CONF=web/config.js

while getopts ":s:m:o:h:d:p:" opt; do
  case $opt in
    s) secret="$OPTARG"
    ;;
    m) mysql_password="$OPTARG"
    ;;
    o) mysql_port="$OPTARG"
    ;;
    h) mysql_host="$OPTARG"
    ;;
    d) maildir_path="$OPTARG"
    ;;
    p) node_port="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ ! -z "$mysql_password" ]; then
  sed -i -r "s/(passwd = )(.*)/\1$mysql_password/g;" $PATH_SCIZ_CONF
  sed -i -r "s/(password: )'(.*)'/\1'$mysql_password'/g;" $PATH_WEB_CONF
fi
if [ ! -z "$secret" ]; then
  sed -i -r "s/(secret: )'(.*)'/\1'$secret'/g;" $PATH_WEB_CONF
fi
if [ ! -z "$node_port" ]; then
  sed -i -r "s/(port_server: )(.*)/\1$node_port/g;" $PATH_WEB_CONF
fi
if [ ! -z "$mysql_port" ]; then
  sed -i -r "s/(port = )(.*)/\1$mysql_port/g;" $PATH_SCIZ_CONF
  sed -i -r "s/(port: )(.*),/\1$mysql_port,/g;" $PATH_WEB_CONF
fi
if [ ! -z "$mysql_host" ]; then
  sed -i -r "s/(host = )(.*)/\1$mysql_host/g;" $PATH_SCIZ_CONF
  sed -i -r "s/(host: )'(.*)',/\1'$mysql_host',/g;" $PATH_WEB_CONF
fi
if [ ! -z "$maildir_path" ]; then
  sed -i -r "s|(maildir_path = )(.*)|\1$maildir_path|g;" $PATH_SCIZ_CONF
fi
