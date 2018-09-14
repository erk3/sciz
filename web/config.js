'use strict';

const Op = require('sequelize').Op;
var config = module.exports;

config.sciz = {
  bin: '/sciz' 
}

config.mh = {
  sp: 'http://sp.mountyhall.com/',
  p_id: 'Numero',
  p_apikey: 'Motdepasse',
  profil2Public_path: 'SP_ProfilPublic2.php'
};

config.server = {
  port_server: 8080
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
    timestamps: false,
    freezeTableName: true
  },
  logging: false
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
