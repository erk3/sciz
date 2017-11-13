'use strict'; 

var sequelize = require('sequelize');
var AssocUsersGroupsTemplate = {};

/*
 * Definition
 */
AssocUsersGroupsTemplate.name = 'AssocUsersGroups';
AssocUsersGroupsTemplate.table = 'assoc_users_groups';

AssocUsersGroupsTemplate.modelDefinition = {  
  user_id: {type: sequelize.INTEGER, primaryKey: true},
  group_id: {type: sequelize.INTEGER, primaryKey: true},
  role: {type: sequelize.INTEGER}
};

AssocUsersGroupsTemplate.modelOptions = {
  name: {
    singular: 'assoc_users_groups',
    plural: 'assoc_users_groups'
  }
};

module.exports = AssocUsersGroupsTemplate;
