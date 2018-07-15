'use strict';

var sequelize = require('sequelize');
var DB = require('../services/database.js');

var PublicController = {}

PublicController.getStats = function (req, res) {
  
  var stats = {};

  DB.User.scope().count()
  .then(function (nbUsers) {
    stats.nbUsers = nbUsers;
    DB.Group.scope().count()
    .then(function (nbGroups) {
      stats.nbGroups = nbGroups;
      var dt = new Date();
      dt.setMonth(dt.getMonth()-1);
      DB.Event.scope().count({where: {time: {[DB.Op.gt]: dt}}})
      .then(function (nbEvents) {
        stats.nbEvents = nbEvents;
        res.json(stats);
      })
    })
  })
  .catch(function(error) {
    res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
  });

}

module.exports = PublicController;
