'use strict';

var config = require('../../config.js');
var DB = require('../services/database.js');

const {spawn} = require('child_process');

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

TrollsController.updateTroll = function (req, res) {
  
  var groupID = (req.body.groupID) ? parseInt(req.body.groupID) : 0;
  var trollID = (req.body.trollID) ? parseInt(req.body.trollID) : 0;
  
  DB.Group.findOne({where: {id: groupID}})
    .then(function (group) {

      var args = ['sciz.py', '-g', group.flat_name, '-r', trollID, 'update'];

      const child = spawn('python', args, {
        shell: false,
        cwd: config.sciz.bin
      });

      var data = '';
      var err = '';

      child.stdout.on('data', (data_out) => {
        data += data_out;
      });

      child.stderr.on('data', (data_err) => {
        err += data_err;
      });

      child.on('close', (code) => {
        if (data) {
          res.json({message: data});
        } else {
          res.status(500).json({message: 'Une erreur est survenue !' + data_err});
        }
      });
  })
  .catch(function (error) {
    res.status(400).json({message: 'Une erreur est survenue ! ' + error.message});
  });

}

module.exports = TrollsController;
