'use strict';

var db = require('../services/database.js');
var Hook = require('../models/hook.js');

var HookController = {}

HookController.test = function (req, res) {
  console.log('ICI hookcontroller test');
  res.json({
    success: true,
    message: 'it works!'
  }); 
}

module.exports = HookController;
