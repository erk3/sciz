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
var TrollsController = require('../controllers/trollsController.js');
var TemplatesController = require('../controllers/templatesController.js');
var PublicController = require('../controllers/publicController.js');
var HookController = require('../controllers/hookController.js');
var PadController = require('../controllers/padController.js');

var APIRoutes = function(passport) {
  
  // POST routes
  router.post('/authenticate', AuthController.authenticate);
  router.post('/signup', AuthController.signup);
  router.post('/profile', passport.authenticate('jwt', {session: false}), allowAuthenticated(UserController.updateProfile));
  router.post('/creategroup', passport.authenticate('jwt', {session: false}), allowAuthenticated(AdminController.createGroup));
  router.post('/pad', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.user, PadController.updatePad));
  router.post('/admin/hooks', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.addHook));
  router.post('/admin/group', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.updateGroup));
  router.post('/bot/hooks', passport.authenticate('jwt', {session: false}), allowOnlyHook(HookController.request));
  router.post('/admin/confs', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.updateConfs));
  router.post('/selfassoc', passport.authenticate('jwt', {session: false}), allowAuthenticated(AdminController.acceptInvite));
  router.post('/admin/invite', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.inviteUser));
  router.post('/admin/assoc', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.updateAssocRole));
  router.post('/trolls/update', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, TrollsController.updateTroll));

  // GET routes
  router.get('/public/stats', PublicController.getStats);
  router.get('/profile', passport.authenticate('jwt', {session: false}), allowAuthenticated(UserController.getProfile));
  router.get('/pad', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.user, PadController.getPad));
  router.get('/events', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.user, EventsController.getEvents));
  router.get('/usersList', passport.authenticate('jwt', {session: false}), allowAuthenticated(UserController.getUsersList));
  router.get('/trolls', passport.authenticate('jwt', {session: false}), allowAuthenticated(TrollsController.getTrolls));
  router.get('/templates', passport.authenticate('jwt', {session: false}), allowAuthenticated(TemplatesController.getTemplate));
  router.get('/bot/hooks', passport.authenticate('jwt', {session: false}), allowOnlyHook(HookController.getNotifs));
  router.get('/admin/hooks', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.getHooks));
  router.get('/admin/confs', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.getConfs));
  router.get('/admin/assocs', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.getAssocs));
  router.get('/assocs', passport.authenticate('jwt', {session: false}), allowAuthenticated(AdminController.getAllRealAssocs));

  // DELETE routes
  router.delete('/admin/hooks', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.revokeHook));
  router.delete('/admin/group', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.deleteGroup));
  router.delete('/profile', passport.authenticate('jwt', {session: false}), allowAuthenticated(UserController.deleteUser));
  router.delete('/admin/selfassoc', passport.authenticate('jwt', {session: false}), allowAuthenticated(AdminController.leaveGroup));
  router.delete('/admin/assoc', passport.authenticate('jwt', {session: false}), allowAuthorized(config.accessLevels.admin, AdminController.excludeGroup));

  return router;
};

module.exports = APIRoutes;
