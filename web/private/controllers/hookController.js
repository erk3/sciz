'use strict';

var DB = require('../services/database.js');

const {spawn} = require('child_process');

var HookController = {}

HookController.getNotifs = function (req, res) {
  
  var hook = req.user;
  var Op = DB.Op;

  DB.Event.scope().findAndCountAll({where: {
    [Op.and]: [
      {id:{[Op.gt]: hook.last_event_id}},
      {notif_to_push: true},
      {group_id: hook.group_id}
    ]},
    attributes: ['id', 'notif'],
    order: [['time', 'ASC']]
  })
    .then(function (result) {
      console.log(result.rows);
      res.json(result.rows);
      if (result.count > 0) {
        DB.Hook.update({last_event_id: Math.max.apply(Math, result.rows.map(function(o){return o.id;}))}, {where: {id: hook.id}});
      }
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue : ' + error.message});
    });
}

HookController.request = function (req, res) {
  var hook = req.user;
  var groupID = hook.group_id;
  var arg1 = req.body.arg1;
  var arg2 = req.body.arg2;
  var arg3 = req.body.arg3;
  
  if (!arg1) {
    res.status(400).json({message: 'Argument manquant !'});
    return;
  }

  DB.Group.findOne({where: {id: groupID}})
    .then(function (group) {

      var args = ['sciz.py', '-g', group.flat_name, '-r', arg1];
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
  })
  .catch(function (error) {
    res.status(400).json({message: 'Une erreur est survenue ! ' + error.message});
  });
}

module.exports = HookController;
