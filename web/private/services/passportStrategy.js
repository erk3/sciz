'use strict';

var JWTStrategy = require('passport-jwt').Strategy;
var ExtractJwt = require('passport-jwt').ExtractJwt;
var config = require('./../../config.js');
var DB = require('../services/database.js');

function hookJWTStrategy(passport) {
  var options = {};

  options.secretOrKey = config.keys.secret;
  options.jwtFromRequest = ExtractJwt.fromAuthHeader();
  options.ignoreExpiration = false;

  passport.use(new JWTStrategy(options, function (JWTPayload, callback) {
    if (JWTPayload.type === 'user') {
      DB.User.findOne({where: {id: JWTPayload.id}})
        .then(function (user) {
          if(!user) {
            callback(null, false);
            return;
          }
          callback(null, user);
        });
    } else if (JWTPayload.type === 'hook') {
      DB.Hook.findOne({where: {name: JWTPayload.name, group_id: JWTPayload.group_id}})
        .then(function (hook) {
          if(!hook) {
            callback(null, false);
            return;
          }
          callback(null, hook);
        });
    } else {
      callback(null, false);
    }
  }));
}

module.exports = hookJWTStrategy;
