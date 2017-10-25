'use strict';

var router = require('express').Router();

var config = require('../../config.js');
var allowOnlyUser = require('../services/routesHelper.js').allowOnlyUser;
var allowOnlyHook = require('../services/routesHelper.js').allowOnlyHook;
var AuthController = require('../controllers/authController.js');
var UserController = require('../controllers/userController.js');
var AdminController = require('../controllers/adminController.js');
var EventsController = require('../controllers/eventsController.js');
var HookController = require('../controllers/hookController.js');

var APIRoutes = function(passport) {
  
  // POST routes
  router.post('/authenticate', AuthController.authenticate);
  router.post('/profile', passport.authenticate('jwt', {session: false}), allowOnlyUser(config.accessLevels.user, UserController.updateProfile));
  router.post('/admin/hooks', passport.authenticate('jwt', {session: false}), allowOnlyUser(config.accessLevels.admin, AdminController.addHook));

  // GET routes
  router.get('/profile', passport.authenticate('jwt', {session: false}), allowOnlyUser(config.accessLevels.user, UserController.getProfile));
  router.get('/events', passport.authenticate('jwt', {session: false}), allowOnlyUser(config.accessLevels.user, EventsController.getEvents));
  router.get('/bot/hooks', passport.authenticate('jwt', {session: false}), allowOnlyHook(HookController.getNotifs));
  router.get('/admin/hooks', passport.authenticate('jwt', {session: false}), allowOnlyUser(config.accessLevels.admin, AdminController.getHooks));

  // DELETE routes
  router.delete('/admin/hooks', passport.authenticate('jwt', {session: false}), allowOnlyUser(config.accessLevels.admin, AdminController.revokeHook));

  return router;
};

module.exports = APIRoutes;
