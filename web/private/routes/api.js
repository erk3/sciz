'use strict';

var router = require('express').Router();

var config = require('../../config.js');
var allowAuthenticated = require('../services/routesHelper.js').allowAuthenticated;
var allowAuthorized = require('../services/routesHelper.js').allowAuthorized;
var allowOnlyHook = require('../services/routesHelper.js').allowOnlyHook;
var AuthController = require('../controllers/authController.js');
var UserController = require('../controllers/userController.js');
var AdminController = require('../controllers/adminController.js');
var EventsController = require('../controllers/eventsController.js');
var HookController = require('../controllers/hookController.js');

var APIRoutes = function(passport) {
  
  // POST routes
  router.post('/authenticate', AuthController.authenticate);
  router.post('/profile', passport.authenticate('jwt', {session: false}), allowAuthenticated(UserController.updateProfile));
  router.post('/admin/hooks', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.addHook));
  router.post('/admin/group', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.updateGroup));
  router.post('/bot/hooks', passport.authenticate('jwt', {session: false}), allowOnlyHook(HookController.request));
  router.post('/admin/confs', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.updateConfs));

  // GET routes
  router.get('/profile', passport.authenticate('jwt', {session: false}), allowAuthenticated(UserController.getProfile));
  router.get('/events', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.user, EventsController.getEvents));
  router.get('/bot/hooks', passport.authenticate('jwt', {session: false}), allowOnlyHook(HookController.getNotifs));
  router.get('/admin/hooks', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.getHooks));
  router.get('/admin/confs', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.getConfs));

  // DELETE routes
  router.delete('/admin/hooks', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.revokeHook));

  return router;
};

module.exports = APIRoutes;
