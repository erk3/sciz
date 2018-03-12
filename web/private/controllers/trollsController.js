'use strict';

var config = require('../../config.js');
var DB = require('../services/database.js');

var TrollsController = {}

TrollsController.getTrolls = function (req, res) {
  
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
  
  var where = {[DB.Op.and]: [
    {group_id: {[DB.Op.eq]: groupID}},
    {user_id: {[DB.Op.ne]: null}}
  ]};
  
  DB.Troll.findAll({where: where})
    .then(function (trolls) {
      res.json(trolls);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue :' + error.message});
    });
}

module.exports = TrollsController;
