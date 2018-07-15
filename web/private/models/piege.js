'use strict'; 

var sequelize = require('sequelize');
var TrollTemplate = require('./troll.js');
var PiegeTemplate = {};

/*
 * Definition
 */
PiegeTemplate.name = 'Piege';
PiegeTemplate.table = 'pieges';

PiegeTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: 'PrimaryKeyConstraint',
    allowNull: false,
    autoincrement: true
  },
  group_id: {
    type: sequelize.INTEGER,
    primaryKey: 'PrimaryKeyConstraint',
    allowNull: false
  },
  troll_id: {type: sequelize.INTEGER},
  time: {type: sequelize.DATE},
  type: {type: sequelize.STRING},
  posx: {type: sequelize.STRING},
  posy: {type: sequelize.STRING},
  posn: {type: sequelize.STRING},
  mm: {type: sequelize.STRING}
};

PiegeTemplate.modelOptions = {
  name: {
    singular: 'piege',
    plural: 'pieges'
  },
  hooks: {
    afterFind: function (piege) {
      if (piege && piege.troll) {
        TrollTemplate.changeBlasonURL(piege.troll);
      }
    }
  }
};

module.exports = PiegeTemplate;
