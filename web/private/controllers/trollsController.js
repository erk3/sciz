'use strict';

var config = require('../../config.js');
var DB = require('../services/database.js');

var TrollsController = {}

TrollsController.getTrolls = function (req, res) {
  
  DB.AssocUsersGroups.scope().findAll({where: {user_id: req.user.id}, attributes: ['group_id']})
    .then(function (groups_id) {
      var where = {[DB.Op.and]: [
        {group_id: {[DB.Op.in]: groups_id.map(o => o.group_id)}},
        {user_id: {[DB.Op.ne]: null}}
      ]};
  
      DB.Troll.findAll({where: where})
        .then(function (trolls) {
          var unique_trolls = []
          for (var i = 0; i < trolls.length; i++) {
            if (!unique_trolls.some(o => o.id === trolls[i].id)) {
              unique_trolls.push(trolls[i]);
            }
          }
          res.json(unique_trolls);
        })
        .catch(function(error) {
          res.status(500).json({message: 'Une erreur est survenue :' + error.message});
        });
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue :' + error.message});
    });
}

module.exports = TrollsController;
