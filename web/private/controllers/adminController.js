'use strict';

var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var DB = require('../services/database.js');

var AdminController = {}

/*
 * Confs
 */
function isUnboxConfValueValid(conf) {
  return !(conf.value === '' || conf.value === undefined || conf.value === null) &&
    !conf.value.match(/{[^}]*({|$)/ig) &&
    !conf.value.match(/((^)|})[^{]*}/ig) &&
    !conf.value.match(/{o\.[^{}]*\W[^{}]*}/ig);
}

AdminController.getConfs = function (req, res) {
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
  DB.Conf.findAll({where: {group_id: groupID}})
    .then(function (confs) {
      res.json(confs);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

AdminController.updateConfs = function (req, res) {
  var groupID = (req.body.groupID) ? parseInt(req.body.groupID) : 0;
  var confs = JSON.parse(req.body.confs);
  for (var i = 0 ; i < confs.length; i++) {
    if (isUnboxConfValueValid(confs[i])) {
      var potentialConf = {where: {group_id: groupID, section: confs[i].section, key: confs[i].key}};
      var data = {
        value: confs[i].value
      };
      // FIXME : wait for the result of all the updates before returning a result ?
      DB.Conf.update(data, potentialConf)
        .then(function(result) {})
        .catch(function(error) {});
    }
  }
  res.json({success: true});
}

/*
 * Hooks
 */
AdminController.addHook = function (req, res) { 
  
  var groupID = (req.body.groupID) ? parseInt(req.body.groupID) : 0;
  var data = {
    name: req.body.name,
    url: req.body.url,
    group_id: groupID,
    jwt: null, // this is created by a Sequelize hook, see models/hook.js
    revoked: false,
    last_event_id : 0 // A try to set it to real last event ID is done below
  };

  var createHook = function (data) {
    DB.Hook.findOne({where: {name: data.name, group_id: data.group_id}})
      .then(function (hook) {
        if (!hook) {
          DB.Hook.create(data)
            .then(function (result) {
              res.json({success: true});
            })
            .catch(function(error) {
              res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
            });
        } else {
          res.status(400).json({message: 'Ce hook existe déjà !'});
        }
      });
  };
  
  DB.Event.scope().findOne({where: {group_id: data.group_id}, order: [['id', 'DESC']]})
    .then(function (event) {
      data.last_event_id = event.id;
      createHook(data);
    })
    .catch(function(error) {
      createHook(data);
    });

}

AdminController.getHooks = function (req, res) {
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
  DB.Hook.findAll({where: {group_id: groupID, revoked: false}})
    .then(function (hooks) {
      res.json(hooks);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

AdminController.revokeHook = function (req, res) {
  var id = (req.query.id) ? parseInt(req.query.id) : 0;
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
  DB.Hook.update({revoked: true}, {where: {id: id, group_id: groupID}})
    .then(function () {
      res.json({success: true});
    })
    .catch(function (error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

/*
 * Group
 */
AdminController.updateGroup = function (req, res) {
  var potentialGroup = {where: {id: req.body.groupID}};

  var data = {
    name: req.body.name,
    blason_url: req.body.blason_url,
    desc: req.body.desc,
  };

  var update = function (group, data, res) {
    DB.Group.update(data, group)
    .then(function (result) {
      res.json({success: true});
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
  };

  DB.Group.findOne(potentialGroup)
    .then(function (group) {
      if (!group) {
        res.status(400).json({message: 'Groupe inexistant !'});
      }
      else {
        update(potentialGroup, data, res);
      }
    });
}
                            
AdminController.deleteGroup = function (req, res) {
  var potentialGroup = {where: {id: req.query.groupID}};
  
  DB.Group.destroy(potentialGroup)
    .then(function (group) {
      res.json({success: true});
    })
    .catch(function (error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error});
    });
}

/*
 * Assocs
 */
function updateAssoc (req, res, potentialAssoc, data) {
 
  var update = function (assoc, data, res) {
    DB.AssocUsersGroups.update(data, assoc)
    .then(function (result) {
      res.json({success: true});
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
  };

  DB.AssocUsersGroups.findOne(potentialAssoc)
    .then(function (assoc) {
      if (!assoc) {
        res.status(400).json({message: 'Association inexistante !'});
      }
      else {
        update(potentialAssoc, data, res);
      }
    });
}

AdminController.getAssocs = function (req, res) {
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
  DB.AssocUsersGroups.findAll({where: {group_id: groupID}})
    .then(function (assocs) {
      res.json(assocs);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

AdminController.updateAssocRole = function (req, res) {
  var potentialAssoc = {where: {group_id: req.body.groupID, user_id: req.body.userID}};

  var data = {
    role: req.body.role
  }
  
  if (req.body.role === 2) {
    var potentialAssocAdmin = {where: {group_id: req.body.groupID, role: 4, user_id: {[DB.Op.ne]: req.body.userID}}};
    DB.AssocUsersGroups.findOne(potentialAssocAdmin)
    .then(function (assoc) {
      if (!assoc) {
        res.status(401).json({message: 'Le dernier administrateur ne peut pas être rétrogradé !'});
      } else {
        updateAssoc(req, res, potentialAssoc, data);
      }
    });
  } else {
    updateAssoc(req, res, potentialAssoc, data);
  }
}

AdminController.acceptInvite = function (req, res) {
  var potentialAssoc = {where: {group_id: req.body.groupID, user_id: req.user.id}};

  var data = {
    role: 2,
    pending: false
  }
  
  updateAssoc(req, res, potentialAssoc, data);
}

AdminController.leaveGroup = function (req, res) {
  var potentialAssoc = {where: {group_id: req.query.groupID, user_id: req.user.id}};
  var potentialAssocAdmin = {where: {group_id: req.query.groupID, role: 4, user_id: {[DB.Op.ne]: req.user.id}}};
  DB.AssocUsersGroups.findOne(potentialAssocAdmin)
  .then(function (assoc) {
    if (!assoc) {
      res.status(401).json({message: 'Le dernier administrateur ne peut pas quitter le groupe !'});
    } else {
      DB.AssocUsersGroups.destroy(potentialAssoc)
      .then(function (assoc) {
        res.json({success: true});
      })
      .catch(function (error) {
        res.status(500).json({message: 'Une erreur est survenue ! ' + error});
      });
    }
  });
}

AdminController.excludeGroup = function (req, res) {
  var potentialAssoc = {where: {group_id: req.query.groupID, user_id: req.query.userID}};
  
  if (req.body.userID === req.user.id) {
    res.status(401).json({message: 'Un administraeur ne peut pas s\'exclure lui même !'});
  } else {
    var potentialTroll = {where: {group_id: req.query.groupID, user_id: req.query.userID}};
    var data = {user_id: null}
    DB.Troll.update(data, potentialTroll);
    DB.AssocUsersGroups.destroy(potentialAssoc)
      .then(function (assoc) {
        res.json({success: true});
      })
      .catch(function (error) {
        res.status(500).json({message: 'Une erreur est survenue ! ' + error});
      });
  }
}

module.exports = AdminController;
