'use strict';

var JWTStrategy = require('passport-jwt').Strategy;
var ExtractJwt = require('passport-jwt').ExtractJwt;

var User = require('./../models/user.js');
var Hook = require('./../models/hook.js');
var config = require('./../../config.js');

function hookJWTStrategy(passport) {
  var options = {};

  options.secretOrKey = config.keys.secret;
  options.jwtFromRequest = ExtractJwt.fromAuthHeader();
  options.ignoreExpiration = false;

  passport.use(new JWTStrategy(options, function (JWTPayload, callback) {
    if (JWTPayload.type === 'user') {
      User.findOne({where: {id: JWTPayload.id}})
        .then(function (user) {
          if(!user) {
            callback(null, false);
            return;
          }
          callback(null, user);
        });
    } else if (JWTPayload.type === 'hook') {
      Hook.findOne({where: {id: JWTPayload.id}})
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
