'use strict'; 

var Sequelize = require('sequelize');

var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var db = require('../services/database.js');

var modelDefinition = {  
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
    autoIncrement: true
  },
  nom: {
    type: Sequelize.STRING,
    allowNull: false
  },
  jwt: {
    type: Sequelize.STRING,
  },
  revoked: {
    type: Sequelize.BOOLEAN,
    defaultValue: false
  },
  last_event_id: {
    type: Sequelize.INTEGER,
    defaultValue: 0
  }
};

var modelOptions = {
  hooks: {
    afterCreate: createNoExpirationJWT
  }
};

var HookModel = db.define('hooks', modelDefinition, modelOptions);

function createNoExpirationJWT(hook) {
  var token = 'JWT ' + jwt.sign(
    {
      type: 'hook',
      id: hook.id,
      nom: hook.nom
    },
    config.keys.secret
  );
  HookModel.update({jwt: token}, {where: {id: hook.id}});
}

module.exports = HookModel;
