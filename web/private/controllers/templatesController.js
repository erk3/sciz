'use strict';

var DB = require('../services/database.js');
var json_default = require('../templates/default.json');
var json_oukonenest = require('../templates/miaou-oukonenest.json');

var TemplatesController = {}

TemplatesController.getTemplate = function (req, res) {

  var templateName = (req.query.templateName) ? req.query.templateName : null;

  if(templateName === 'default') {
    res.json(json_default);
  } else if(templateName === 'miaou-oukonenest') {
    res.json(json_oukonenest);
  } else {
    res.status(400).json({message: 'Ce template n\'existe pas'});
  }
}

module.exports = TemplatesController;
