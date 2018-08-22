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
  
  var getTrollsWithCapas = function (trolls) {
    var promises = []
    for (var i = 0; i < trolls.length; i++) {
      promises[i] = DB.AssocTrollsCapas.findAll({where: {troll_id: trolls[i].user_id}});
    }
    Promise.all(promises)
      .then(function (capas) {
        for (var i = 0; i < capas.length; i++) {
          trolls[i].dataValues.capas = capas[i];
        }
        res.json(trolls);
      });
  };
  
  DB.Troll.unscoped().findAll({where: where})
    .then(function (trolls) {
      getTrollsWithCapas(trolls);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue :' + error.message});
    });
}

module.exports = TrollsController;
