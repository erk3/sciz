'use strict'; 

var sequelize = require('sequelize');
var GroupTemplate = {};

/*
 * Definition
 */
GroupTemplate.name = 'Group';
GroupTemplate.table = 'groups';

GroupTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
    autoIncrement: true
  },
  name: {
    type: sequelize.STRING,
    unique: true,
    allowNull: false
  },
  desc: {
    type: sequelize.STRING,
  },
  blason_url: {
    type: sequelize.STRING,
  }
};

GroupTemplate.modelOptions = {
  name: {
    singular: 'group',
    plural: 'groups'
  }
};

module.exports = GroupTemplate;
