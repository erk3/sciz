'use strict';

var JWTStrategy = require('passport-jwt').Strategy;
var ExtractJwt = require('passport-jwt').ExtractJwt;

var User = require('./../models/user.js');
var config = require('./../../config.js');

function hookJWTStrategy(passport) {
  var options = {};

  options.secretOrKey = config.keys.secret;
  options.jwtFromRequest = ExtractJwt.fromAuthHeader();
  options.ignoreExpiration = false;

  passport.use(new JWTStrategy(options, function (JWTPayload, callback) {
    User.findOne({where: {id: JWTPayload.id}})
      .then(function (user) {
        if(!user) {
          callback(null, false);
          return;
        }
        callback(null, user);
      });
  }));
}

module.exports = hookJWTStrategy;
