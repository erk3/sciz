#!/bin/bash

PATH_SCIZ_CONF=confs/sciz.ini
PATH_WEB_CONF=web/config.js

while getopts ":s:m:o:h:c:d:p:b:w:" opt; do
  case $opt in
    s) secret="$OPTARG"
    ;;
    m) mysql_password="$OPTARG"
    ;;
    o) mysql_port="$OPTARG"
    ;;
    h) mysql_host="$OPTARG"
    ;;
    c) pf_conf_file="$OPTARG"
    ;;
    d) maildir_path="$OPTARG"
    ;;
    p) node_port="$OPTARG"
    ;;
    b) bin_path="$OPTARG"
    ;;
    w) domain_name="$OPTARG"
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
if [ ! -z "$bin_path" ]; then
  sed -i -r "s/(bin: )'(.*)'/\1'$bin_path'/g;" $PATH_WEB_CONF
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
  sed -i -r "s|(maildirs_base_path = )(.*)|\1$maildir_path|g;" $PATH_SCIZ_CONF
fi
if [ ! -z "$pf_conf_file" ]; then
  sed -i -r "s|(postfix_accounts_conf_file = )(.*)|\1$pf_conf_file|g;" $PATH_SCIZ_CONF
fi
if [ ! -z "$domain_name" ]; then
  sed -i -r "s/(domain_name = )(.*)/\1$domain_name/g;" $PATH_SCIZ_CONF
fi
