'use strict'; 

var sequelize = require('sequelize');
var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var HookTemplate = {};

/*
 * Methods
 */
var createNoExpirationJWT = function (hook) {
  var token = 'JWT ' + jwt.sign(
    {
      type: 'hook',
      id: hook.id,
      group_id: hook.group_id,
      name: hook.name
    },
    config.keys.secret
  );
  hook.jwt = token;
};

/*
 * Definition
 */
HookTemplate.name = 'Hook';
HookTemplate.table = 'hooks';

HookTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
    autoIncrement: true
  },
  name: {
    type: sequelize.STRING,
    unique: true,
    allowNull: false
  },
  jwt: {
    type: sequelize.STRING,
  },
  revoked: {
    type: sequelize.BOOLEAN,
    defaultValue: false
  },
  last_event_id: {
    type: sequelize.INTEGER,
    defaultValue: 0
  }
};

HookTemplate.modelOptions = {
  name: {
    singular: 'hook',
    plural: 'hooks'
  },
  hooks: {
    beforeCreate: createNoExpirationJWT
  }
};

module.exports = HookTemplate;
