'use strict';

const Op = require('sequelize').Op;
var config = module.exports;

config.sciz = {
  bin: '/sciz' 
};

config.server = {
  port_server: 80
};

config.db = {
  name: 'sciz', 
  user: 'sciz', 
  password: 'db_passwd'
};

config.db.details = {
  host: '127.0.0.1',
  port: 3306,
  dialect: 'mysql',
  operatorsAliases: Op,
  define: {
    timestamps: false
  }
};

config.keys = {
  secret: 'secret'
};

var userRoles = config.userRoles = {
  guest: 1,     // ...001
  user: 2,     // ...010
  admin: 4     // ...100
};

config.accessLevels = {
  guest: userRoles.user | userRoles.admin | userRoles.guest,    // ...111
  user: userRoles.user | userRoles.admin,                       // ...110
  admin: userRoles.admin                                        // ...100
};
