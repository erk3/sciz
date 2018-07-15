'use strict'; 

var sequelize = require('sequelize');
var TrollTemplate = require('./troll.js');
var PortalTemplate = {};

/*
 * Definition
 */
PortalTemplate.name = 'Portal';
PortalTemplate.table = 'portals';

PortalTemplate.modelDefinition = {  
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
  posx: {type: sequelize.STRING},
  posy: {type: sequelize.STRING},
  posn: {type: sequelize.STRING},
  dst_posx: {type: sequelize.STRING},
  dst_posy: {type: sequelize.STRING},
  dst_posn: {type: sequelize.STRING},
  disp_posx: {type: sequelize.STRING},
  disp_posy: {type: sequelize.STRING},
  disp_posn: {type: sequelize.STRING},
};

PortalTemplate.modelOptions = {
  name: {
    singular: 'portal',
    plural: 'portals'
  },
  hooks: {
    afterFind: function (portal) {
      if (portal && portal.troll) {
        TrollTemplate.changeBlasonURL(portal.troll);
      }
    }
  }
};

module.exports = PortalTemplate;
