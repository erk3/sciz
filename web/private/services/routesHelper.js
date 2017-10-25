'use strict';

exports.allowOnlyUser = function (accessLevel, callback) {
  function checkUserRole(req, res) {
    if (!req.user || !(accessLevel & req.user.role)) {
      res.sendStatus(403);
      return;
    }
    callback(req, res);
  }
  return checkUserRole;
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
