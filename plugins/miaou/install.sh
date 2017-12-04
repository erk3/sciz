#!/bin/bash

ROOT_PATH=`dirname $0`
PLUGIN_PATH="$ROOT_PATH/plugin"
DEPLOY_PATH="../../../miaou/plugins/sciz"

# installing the plugin in the plugins directory of the miaou installation
rm -rf $DEPLOY_PATH
cp -r $PLUGIN_PATH $DEPLOY_PATH
