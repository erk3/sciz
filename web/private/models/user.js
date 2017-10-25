'use strict'; 

var Sequelize = require('sequelize');
var bcrypt = require('bcrypt');

var config = require('../../config.js');
var db = require('../services/database.js');
var TrollModel = require('./troll.js');
var CDMModel = require('./cdm.js');
var MobModel = require('./mob.js');

var modelDefinition = {  
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  pseudo: {
    type: Sequelize.STRING,
  },
  pwd: {
    type: Sequelize.STRING,
    allowNull: false
  },
  mh_apikey: {
    type: Sequelize.STRING,
  },
  role: {
    type: Sequelize.INTEGER,
    defaultValue: config.userRoles.user
  }
};

var modelOptions = {
  instanceMethods: {
    comparePasswords: comparePasswords
  },
  hooks: {
    beforeValidate: hashPassword,
    afterFind: changeTrollBlasonURL
  },
  defaultScope: {
    include: [{model: TrollModel, as: 'troll'}]
  }
};

var UserModel = db.define('users', modelDefinition, modelOptions);
UserModel.hasOne(TrollModel, {as: 'troll', foreignKey: 'id'});

function comparePasswords(pwd, callback) {
  bcrypt.compare(pwd, this.pwd, function(error, isMatch) {
    if(error) {
      return callback(error);
    }
    return callback(null, isMatch);
  });
}

function changeTrollBlasonURL(user) { 
  if (user && user.troll && user.troll.blason_url.startsWith('http://www.mountyhall.com/images/Blasons/Blason_PJ')) { 
    user.troll.blason_url = 'http://blason.mountyhall.com/Blason_PJ/' + user.troll.id; 
  } 
}

function hashPassword(user) {
  if(user.changed('pwd')) {
    return bcrypt.hash(user.pwd, 10).then(function(pwd) {
      user.pwd = pwd;
    });
  }
}

module.exports = UserModel;
