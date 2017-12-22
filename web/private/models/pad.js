'use strict'; 

var sequelize = require('sequelize');
var PadTemplate = {};

/*
 * Definition
 */
PadTemplate.name = 'Pad';
PadTemplate.table = 'pads';

PadTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  group_id: {
    type: sequelize.INTEGER,
    unique: 'UniqueKeyConstraint'
  },
  value: {type: sequelize.STRING}
};

PadTemplate.modelOptions = {
  name: {
    singular: 'pad',
    plural: 'pads'
  }
};

module.exports = PadTemplate;
