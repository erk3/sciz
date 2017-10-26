'use strict';

var db = require('../services/database.js');
var Hook = require('../models/hook.js');
var Event = require('../models/event.js');

const Op = db.Op;
const {spawn} = require('child_process');

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
      res.status(500).json({message: 'Une erreur est survenue : ' + error.message});
    });
}


HookController.request = function (req, res) {
  var arg1 = req.body.arg1;
  var arg2 = req.body.arg2;
  var arg3 = req.body.arg3;
  
  if (!arg1) {
    res.status(400).json({message: 'Argument manquant !'});
    return;
  }

  var args = ['sciz.py', '-r', arg1];
  if (arg2) {
    args.push(arg2);
  }
  if (arg3) {
    args.push(arg3);
  }

  const child = spawn('python', args, {
    shell: false,
    cwd: config.sciz.bin
  });

  var data = '';

  child.stdout.on('data', (data_out) => {
    data += data_out;
  });

  child.on('close', (code) => {
    if (data) {
      res.json({message: data});
    } else {
      res.status(500).json({message: 'Une erreur est survenue !'});
    }
  });
}

module.exports = HookController;
