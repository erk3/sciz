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
  race: {type: Sequelize.STRING},
  blason_url: {type: Sequelize.STRING}
};

var modelOptions = {
  hooks: {
    afterFind: changeBlasonURL
  }
};

var TrollModel = db.define('trolls', modelDefinition, modelOptions);

function changeBlasonURL(troll) {
  if (troll.blason_url.startsWith('http://www.mountyhall.com/images/Blasons/Blason_PJ')) {
    troll.blason_url = 'http://blason.mountyhall.com/Blason_PJ/' + troll.id;
  }
}

module.exports = TrollModel;
