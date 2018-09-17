'use strict';

var config = require('../../config.js');
var DB = require('../services/database.js');

var ViewController = {}

ViewController.getView = function (req, res) {
  
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
    
  var where_troll = {[DB.Op.and]: [ {user_id: {[DB.Op.not]: null}}, {group_id: groupID} ]};
  
  DB.Troll.unscoped().findAll({where: where_troll, attributes: ['id', 'nom', 'pos_x', 'pos_y', 'pos_n', 'last_seen', 'base_vue', 'bonus_vue_phy', 'bonus_vue_mag']})
    .then(function (trolls) {
      
      var troll = trolls.find(function (troll) { return troll.id === req.user.id; });
      var origX = (req.query.origX) ? parseInt(req.query.origX) : (troll.pos_x || 0);
      var origY = (req.query.origY) ? parseInt(req.query.origY) : (troll.pos_y || 0);
      var origN = (req.query.origN) ? parseInt(req.query.origN) : (troll.pos_n || 0);
      var portee = (req.query.portee) ? parseInt(req.query.portee) : (troll.base_vue || 0) + (troll.bonus_vue_phy || 0) + (troll.bonus_vue_mag || 0);
      
      var where_orig_x = {
        [DB.Op.and]: [
          {pos_x: {[DB.Op.gte]: origX - portee}},
          {pos_x: {[DB.Op.lte]: origX + portee}}
        ]
      };

      var where_orig_y = {
        [DB.Op.and]: [
          {pos_y: {[DB.Op.gte]: origY - portee}},
          {pos_y: {[DB.Op.lte]: origY + portee}}
        ]
      };

      var where_orig_n = {
        [DB.Op.and]: [
          {pos_n: {[DB.Op.gte]: origN - (portee / 2)}},
          {pos_n: {[DB.Op.lte]: origN + (portee / 2)}}
        ]
      };

      var where_group_troll = {[DB.Op.and]: [ {group_id: groupID}, where_orig_x, where_orig_y, where_orig_n ]};
      
      var where_group_mob = {[DB.Op.and]: [ {group_id: groupID}, {dead: {[DB.Op.not]: true}}, where_orig_x, where_orig_y, where_orig_n ]};

      var where_no_group = {[DB.Op.and]: [ where_orig_x, where_orig_y, where_orig_n ]};
     
      var promises = []
      
      promises[0] = DB.Troll.unscoped().findAll({where: where_group_troll, attributes: ['id', 'nom', 'pos_x', 'pos_y', 'pos_n', 'last_seen']});
      promises[1] = DB.Mob.unscoped().findAll({where: where_group_mob, attributes: ['id', 'nom', 'age', 'tag', 'pos_x', 'pos_y', 'pos_n', 'last_seen']});
      promises[2] = DB.Lieu.unscoped().findAll({where: where_no_group, attributes: ['id', 'nom', 'pos_x', 'pos_y', 'pos_n']});
     
      Promise.all(promises)
        .then(function (objs) {
          var trollView = {
            id: req.user.id,
            origine: {x: origX, y: origY, n: origN, portee: portee},
            gTrolls: trolls,
            trolls: objs[0],
            mobs: objs[1],
            lieux: objs[2]
          };
          res.json(trollView);
        })
        .catch(function(error) {
          res.status(500).json({message: 'Une erreur est survenue :' + error.message});
        });
    });
}

module.exports = ViewController;
