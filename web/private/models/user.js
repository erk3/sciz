'use strict'; 

var bcrypt = require('bcrypt');
var sequelize = require('sequelize');
var TrollTemplate = require('./troll.js');
var UserTemplate = {}

/*
 * Methods
 */
UserTemplate.comparePasswords = function (pwd, callback) {
  bcrypt.compare(pwd, this.pwd, function (error, isMatch) {
    if (error) {
      return callback(error);
    }
    return callback(null, isMatch);
  });
}

UserTemplate.hashPassword = function (user) {
  if (user.changed('pwd')) {
    return bcrypt.hash(user.pwd, 10).then(function (pwd) {
      user.pwd = pwd;
    });
  }
}

/*
 * Definition
 */
UserTemplate.name = 'User';
UserTemplate.table = 'users';

UserTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  pseudo: {
    type: sequelize.STRING,
  },
  pwd: {
    type: sequelize.STRING,
    allowNull: false
  },
  mh_apikey: {
    type: sequelize.STRING,
  },
  session_duration: {
    type: sequelize.INTEGER,
  },
  dyn_sp_refresh: {
    type: sequelize.INTEGER,
  },
  static_sp_refresh: {
    type: sequelize.INTEGER,
  },
};

UserTemplate.modelOptions = {
  name: {
    singular: 'user',
    plural: 'users',
  },
  hooks: {
    beforeValidate: UserTemplate.hashPassword,
    afterFind: function (user) {
      if (user && user.trolls) {
        user.trolls.forEach(TrollTemplate.changeBlasonURL);
      }
    }
  }
};

module.exports = UserTemplate;
