'use strict'; 

var sequelize = require('sequelize');
var TrollTemplate = require('./troll.js');
var IDCTemplate = {};

/*
 * Definition
 */
IDCTemplate.name = 'IDC';
IDCTemplate.table = 'idcs';

IDCTemplate.modelDefinition = {  
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
  champi_id: {type: sequelize.INTEGER},
  troll_id: {type: sequelize.INTEGER},
  time: {type: sequelize.DATE},
  type: {type: sequelize.STRING},
  qualite: {type: sequelize.STRING},
  posx: {type: sequelize.STRING},
  posy: {type: sequelize.STRING},
  posn: {type: sequelize.STRING},
};

IDCTemplate.modelOptions = {
  name: {
    singular: 'idc',
    plural: 'idcs'
  },
  hooks: {
    afterFind: function (idc) {
      if (idc && idc.troll) {
        TrollTemplate.changeBlasonURL(idc.troll);
      }
    }
  }
};

module.exports = IDCTemplate;
