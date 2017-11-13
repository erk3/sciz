'use strict'; 

var sequelize = require('sequelize');
var MetamobTemplate = {};

/*
 * Definition
 */
MetamobTemplate.name = 'Metamob';
MetamobTemplate.table = 'metamobs';

MetamobTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  nom: {type: sequelize.STRING},
  determinant: {type: sequelize.STRING},
  blason_url: {type: sequelize.STRING}
};

MetamobTemplate.modelOptions = {
  name: {
    singular: 'metamob',
    plural: 'metamobs'
  }
};

module.exports = MetamobTemplate;
