'use strict';

var db = require('../services/database.js');
var Hook = require('../models/hook.js');
var Event = require('../models/event.js');

const Op = db.Op;

var HookController = {}

HookController.getNotifs = function (req, res) {
  
  var hook = req.user;

  Event.scope().findAndCountAll({where: {
    [Op.and]: [
      {id:{[Op.gt]: hook.last_event_id}},
      {notif_to_push: true}
    ]},
    attributes: ['id', 'notif'],
    order: [['id', 'DESC']]
  })
    .then(function (result) {
      res.json(result.rows);
      if (result.count > 0) {
        Hook.update({last_event_id: result.rows[0].id}, {where: {id: hook.id}});
      }
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue :' + error.message});
    });

}

module.exports = HookController;
