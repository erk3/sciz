'use strict'; 

var sequelize = require('sequelize');
var TrollTemplate = require('./troll.js');
var IDTTemplate = {};

/*
 * Definition
 */
IDTTemplate.name = 'IDT';
IDTTemplate.table = 'idts';

IDTTemplate.modelDefinition = {  
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
  metatresor_id: {type: sequelize.INTEGER},
  tresor_id: {type: sequelize.INTEGER},
  troll_id: {type: sequelize.INTEGER},
  time: {type: sequelize.DATE},
  action: {type: sequelize.STRING},
  type: {type: sequelize.STRING},
  templates: {type: sequelize.STRING},
  mithril: {type: sequelize.BOOLEAN},
  effet: {type: sequelize.STRING},
  posx: {type: sequelize.STRING},
  posy: {type: sequelize.STRING},
  posn: {type: sequelize.STRING},
};

IDTTemplate.modelOptions = {
  name: {
    singular: 'idt',
    plural: 'idts'
  },
  hooks: {
    afterFind: function (idt) {
      if (idt && idt.troll) {
        TrollTemplate.changeBlasonURL(idt.troll);
      }
    }
  }
};

module.exports = IDTTemplate;
