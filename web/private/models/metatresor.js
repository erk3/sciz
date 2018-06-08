'use strict'; 

var sequelize = require('sequelize');
var MetatresorTemplate = {};

/*
 * Definition
 */
MetatresorTemplate.name = 'Metatresor';
MetatresorTemplate.table = 'metatresors';

MetatresorTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  nom: {type: sequelize.STRING},
  type: {type: sequelize.STRING}
};

MetatresorTemplate.modelOptions = {
  name: {
    singular: 'metatresor',
    plural: 'metatresors'
  }
};

module.exports = MetatresorTemplate;
