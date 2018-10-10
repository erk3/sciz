'use strict'; 

var sequelize = require('sequelize');
var LieuTemplate = {};

/*
 * Definition
 */
LieuTemplate.name = 'Lieu';
LieuTemplate.table = 'lieux';

LieuTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  nom: {type: sequelize.STRING},
  pos_x: {type: sequelize.INTEGER},
  pos_y: {type: sequelize.INTEGER},
  pos_n: {type: sequelize.INTEGER},
  last_seen: {type: sequelize.DATE}
};

LieuTemplate.modelOptions = {
  name: {
    singular: 'lieu',
    plural: 'lieux'
  }
};

module.exports = LieuTemplate;
