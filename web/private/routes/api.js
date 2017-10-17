'use strict';

var router = require('express').Router();

var config = require('../../config.js');
var allowOnly = require('../services/routesHelper.js').allowOnly;
var AuthController = require('../controllers/authController.js');
var UserController = require('../controllers/userController.js');

var APIRoutes = function(passport) {
  // POST routes
  router.post('/authenticate', AuthController.authenticate);
  router.post('/profile', passport.authenticate('jwt', {session: false}), allowOnly(config.accessLevels.user, UserController.updateProfile));

  // GET routes
  router.get('/profile', passport.authenticate('jwt', {session: false}), allowOnly(config.accessLevels.user, UserController.getProfile));

  return router;
};

module.exports = APIRoutes;
