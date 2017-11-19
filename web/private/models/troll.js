'use strict'; 

var sequelize = require('sequelize');
var TrollTemplate = {}

/*
 *  Methods
 */
TrollTemplate.changeBlasonURL = function (troll) {
  if (troll && troll.blason_url && troll.blason_url.startsWith('http://www.mountyhall.com/images/Blasons/Blason_PJ')) {
    troll.blason_url = 'http://blason.mountyhall.com/Blason_PJ/' + troll.id;
  } else if (troll && !troll.blason_url) {
    troll.blason_url = 'http://blason.mountyhall.com/Blason_PJ/MyNameIsNobody.gif';
  }
  return troll;
};

/*
 * Definition
 */
TrollTemplate.name = 'Troll';
TrollTemplate.table = 'trolls';

TrollTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: 'PrimaryKeyConstraint',
    allowNull: false
  },
  group_id: {
    type: sequelize.INTEGER,
    primaryKey: 'PrimaryKeyConstraint',
    allowNull: false
  },
  user_id: {type: sequelize.INTEGER},
  nom: {type: sequelize.STRING},
  race: {type: sequelize.STRING},
  blason_url: {type: sequelize.STRING}
};

TrollTemplate.modelOptions = {
  name: {
    singular: 'troll',
    plural: 'trolls'
  },
  hooks: {
    afterFind: TrollTemplate.changeBlasonURL
  }
};
module.exports = TrollTemplate;

