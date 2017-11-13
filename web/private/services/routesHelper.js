'use strict';

exports.allowAuthenticated = function (callback) {
  function checkUser(req, res) {
    var user = req.user;
    if (!user) {
      res.sendStatus(403);
      return;
    }
    callback(req, res);
  }
  return checkUser;
};

exports.allowAuthorized = function (accessLevel, callback) {
  function checkRole(req, res) {
    var user = req.user;
    var groupID = req.query.groupID;
    groupID = (groupID) ? groupID : req.body.groupID;
    if (!user || !groupID || !user.assocs) { 
      res.sendStatus(403);
      return;
    }
    for (var i = 0; i < user.assocs.length; i++) {
      if (user.assocs[i].group_id == groupID) {
        if (user.assocs[i].role & accessLevel) {
          callback(req, res);
          return;
        }
        break;
      }
    }
    res.sendStatus(403);
  }
  return checkRole;
};

exports.allowOnlyHook = function (callback) {
  function checkHookValidity(req, res) {
    var hook = req.user;
    if (!hook || hook.revoked !== false) {
      res.sendStatus(403);
      return;
    }
    callback(req, res);
  }
  return checkHookValidity;
};
