'use strict';

var router = require('express').Router();

var config = require('../../config.js');
var allowOnly = require('../services/routesHelper.js').allowOnly;
var AuthController = require('../controllers/authController.js');
var UserController = require('../controllers/userController.js');
var EventsController = require('../controllers/eventsController.js');

var APIRoutes = function(passport) {
  // POST routes
  router.post('/authenticate', AuthController.authenticate);
  router.post('/profile', passport.authenticate('jwt', {session: false}), allowOnly(config.accessLevels.user, UserController.updateProfile));

  // GET routes
  router.get('/profile', passport.authenticate('jwt', {session: false}), allowOnly(config.accessLevels.user, UserController.getProfile));
  router.get('/events', passport.authenticate('jwt', {session: false}), allowOnly(config.accessLevels.user, EventsController.getEvents));

  return router;
};

module.exports = APIRoutes;
