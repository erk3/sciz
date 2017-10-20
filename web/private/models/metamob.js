'use strict'; 

var Sequelize = require('sequelize');

var db = require('../services/database.js');

var modelDefinition = {  
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  nom: {type: Sequelize.STRING},
  determinant: {type: Sequelize.STRING},
  blason_url: {type: Sequelize.STRING}
};

var modelOptions = {};

var MetamobModel = db.define('metamobs', modelDefinition, modelOptions);

module.exports = MetamobModel;
