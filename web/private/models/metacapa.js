'use strict'; 

var sequelize = require('sequelize');
var MetacapaTemplate = {};

/*
 * Definition
 */
MetacapaTemplate.name = 'Metacapa';
MetacapaTemplate.table = 'metacapas';

MetacapaTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  nom: {type: sequelize.STRING},
  type: {type: sequelize.STRING},
  subtype: {type: sequelize.STRING},
  pa: {type: sequelize.INTEGER}
};

MetacapaTemplate.modelOptions = {
  name: {
    singular: 'metacapa',
    plural: 'metacapas'
  }
};

module.exports = MetacapaTemplate;
