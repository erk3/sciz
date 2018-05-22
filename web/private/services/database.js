'use strict';

var config = require('../../config.js');
var sequelize = require('sequelize');

var AssocUsersGroupsTemplate = require('../models/assoc_users_groups.js');
var UserTemplate = require('../models/user.js');
var TrollTemplate = require('../models/troll.js');
var MobTemplate = require('../models/mob.js');
var MetamobTemplate = require('../models/metamob.js');
var GroupTemplate = require('../models/group.js');
var ConfTemplate = require('../models/conf.js');
var HookTemplate = require('../models/hook.js');
var BattleTemplate = require('../models/battle.js');
var AATemplate = require('../models/aa.js');
var CDMTemplate = require('../models/cdm.js');
var PiegeTemplate = require('../models/piege.js');
var PortalTemplate = require('../models/portal.js');
var IDCTemplate = require('../models/idc.js');
var EventTemplate = require('../models/event.js');
var PadTemplate = require('../models/pad.js');

/*
 * Main database connection
 */
var DB = new sequelize(
  config.db.name,
  config.db.user,
  config.db.password,
  config.db.details
);

/*
 * Models definition
 */
var Templates = [];
Templates.push(AssocUsersGroupsTemplate);
Templates.push(UserTemplate);
Templates.push(TrollTemplate);
Templates.push(MobTemplate);
Templates.push(MetamobTemplate);
Templates.push(GroupTemplate);
Templates.push(ConfTemplate);
Templates.push(HookTemplate);
Templates.push(BattleTemplate);
Templates.push(AATemplate);
Templates.push(CDMTemplate);
Templates.push(PiegeTemplate);
Templates.push(PortalTemplate);
Templates.push(IDCTemplate);
Templates.push(EventTemplate);
Templates.push(PadTemplate);

Templates.forEach(function (Template) {
  DB[Template.name] = DB.define(Template.table, Template.modelDefinition, Template.modelOptions);
});

/*
 * Models additions and associations
 */
// Assocs Users Groups
DB.AssocUsersGroups.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id', onDelete: 'cascade'});
DB.AssocUsersGroups.belongsTo(DB.User, {foreignKey: 'user_id', targetKey: 'id', onDelete: 'cascade'});
// User
DB.User.prototype.comparePasswords = UserTemplate.comparePasswords;
DB.User.hasMany(DB.Troll, {foreignKey: 'user_id', sourceKey: 'id'});
DB.User.hasMany(DB.AssocUsersGroups, {as: 'assocs', foreignKey: 'user_id', sourceKey: 'id'});
// Should be hasOne but Sequelize does not support sourceKey for hasOne at the moment
// DB.User.hasOne(DB.Group, {foreignKey: 'id', sourceKey: 'default_group_id'});
DB.User.hasMany(DB.Group, {foreignKey: 'id', sourceKey: 'default_group_id'});
// Troll
DB.Troll.belongsTo(DB.User, {foreignKey: 'user_id', targetKey: 'id', onDelete: 'set null'});
DB.Troll.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id', onDelete: 'cascade'});
DB.Troll.hasMany(DB.Piege, {foreignKey: 'troll_id', sourceKey: 'id'});
DB.Troll.hasMany(DB.CDM, {foreignKey: 'troll_id', sourceKey: 'id'});
DB.Troll.hasMany(DB.AA, {foreignKey: 'troll_id', sourceKey: 'id'});
DB.Troll.hasMany(DB.Battle, {as: 'atts', foreignKey: 'att_troll_id', sourceKey: 'id'});
DB.Troll.hasMany(DB.Battle, {as: 'defs', foreignKey: 'def_troll_id', sourceKey: 'id'});
// Mob
DB.Mob.hasMany(DB.CDM, {foreignKey: 'mob_id', sourceKey: 'id'});
DB.Mob.hasMany(DB.Battle, {as: 'atts', foreignKey: 'att_mob_id', sourceKey: 'id'});
DB.Mob.hasMany(DB.Battle, {as: 'defs', foreignKey: 'def_mob_id', sourceKey: 'id'});
DB.Mob.belongsTo(DB.Metamob, {foreignKey: 'metamob_id', targetKey: 'id'});
DB.Mob.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
// Metamob
DB.Metamob.hasMany(DB.Mob, {foreignKey: 'metamob_id', sourceKey: 'id'});
// Group
DB.Group.hasMany(DB.AssocUsersGroups, {as: 'assocs', foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.Conf, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.Troll, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.Mob, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.Hook, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.Event, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.Battle, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.AA, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.CDM, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.Piege, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.Portal, {foreignKey: 'group_id', sourceKey: 'id'});
DB.Group.hasMany(DB.IDC, {foreignKey: 'group_id', sourceKey: 'id'});
// Conf
DB.Conf.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
// Hook
DB.Hook.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
// Battle
DB.Battle.belongsTo(DB.Troll, {as: 'att_troll', foreignKey: 'att_troll_id', targetKey: 'id'});
DB.Battle.belongsTo(DB.Troll, {as: 'def_troll', foreignKey: 'def_troll_id', targetKey: 'id'});
DB.Battle.belongsTo(DB.Mob, {as: 'att_mob', foreignKey: 'att_mob_id', targetKey: 'id'});
DB.Battle.belongsTo(DB.Mob, {as: 'def_mob', foreignKey: 'def_mob_id', targetKey: 'id'});
DB.Battle.belongsTo(DB.Piege, {foreignKey: 'piege_id', targetKey: 'id'});
DB.Battle.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
// Should be hasOne but Sequelize does not support sourceKey for hasOne at the moment
// DB.Battle.hasOne(DB.Event, {foreignKey: 'battle_id'});
DB.Battle.hasMany(DB.Event, {foreignKey: 'battle_id', sourceKey: 'id'});
// AA
DB.AA.belongsTo(DB.Troll, {as: 'troll', foreignKey: 'troll_id', targetKey: 'id'});
DB.AA.belongsTo(DB.Troll, {as: 'troll_cible', foreignKey: 'troll_cible_id', targetKey: 'id'});
DB.AA.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
// Should be hasOne but Sequelize does not support sourceKey for hasOne at the moment
// DB.AA.hasOne(DB.Event, {foreignKey: 'aa_id', sourceKey: 'id'});
DB.AA.hasMany(DB.Event, {foreignKey: 'aa_id', sourceKey: 'id'});
// CDM
DB.CDM.belongsTo(DB.Troll, {foreignKey: 'troll_id', targetKey: 'id'});
DB.CDM.belongsTo(DB.Mob, {foreignKey: 'mob_id', targetKey: 'id'});
DB.CDM.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
// Should be hasOne but Sequelize does not support sourceKey for hasOne at the moment
// DB.CDM.hasOne(DB.Event, {foreignKey: 'cdm_id', sourceKey: 'id'});
DB.CDM.hasMany(DB.Event, {foreignKey: 'cdm_id', sourceKey: 'id'});
// Piege
DB.Piege.belongsTo(DB.Troll, {foreignKey: 'troll_id', targetKey: 'id'});
DB.Piege.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
DB.Piege.hasMany(DB.Battle, {foreignKey: 'piege_id', sourceKey: 'id'});
// Should be hasOne but Sequelize does not support sourceKey for hasOne at the moment
// DB.Piege.hasOne(DB.Event, {foreignKey: 'piege_id', sourceKey: 'id'});
DB.Piege.hasMany(DB.Event, {foreignKey: 'piege_id', sourceKey: 'id'});
// Portal
DB.Portal.belongsTo(DB.Troll, {foreignKey: 'troll_id', targetKey: 'id'});
DB.Portal.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
// Should be hasOne but Sequelize does not support sourceKey for hasOne at the moment
// DB.Portal.hasOne(DB.Event, {foreignKey: 'portal_id', sourceKey: 'id'});
DB.Portal.hasMany(DB.Event, {foreignKey: 'portal_id', sourceKey: 'id'});
// IDC
DB.IDC.belongsTo(DB.Troll, {foreignKey: 'troll_id', targetKey: 'id'});
DB.IDC.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});
// Should be hasOne but Sequelize does not support sourceKey for hasOne at the moment
// DB.IDC.hasOne(DB.Event, {foreignKey: 'idc_id', sourceKey: 'id'});
DB.IDC.hasMany(DB.Event, {foreignKey: 'idc_id', sourceKey: 'id'});
// Event
DB.Event.belongsTo(DB.Battle, {foreignKey: 'battle_id', targetKey: 'id'});
DB.Event.belongsTo(DB.CDM, {foreignKey: 'cdm_id', targetKey: 'id'});
DB.Event.belongsTo(DB.AA, {foreignKey: 'aa_id', targetKey: 'id'});
DB.Event.belongsTo(DB.Piege, {foreignKey: 'piege_id', targetKey: 'id'});
DB.Event.belongsTo(DB.Portal, {foreignKey: 'portal_id', targetKey: 'id'});
DB.Event.belongsTo(DB.IDC, {foreignKey: 'idc_id', targetKey: 'id'});
DB.Event.belongsTo(DB.Group, {foreignKey: 'group_id', targetKey: 'id'});

/*
 * Scopes
 */
// Assocs
DB.AssocUsersGroups.addScope('defaultScope', {include: [{model: DB.Group}, {model: DB.User.unscoped(), attributes: ['id', 'pseudo']}]}, {override: true});
// Mob
DB.Mob.addScope('defaultScope', {include: [{model: DB.Metamob}]}, {override: true});
// Battle
DB.Battle.addScope('defaultScope', {
  include: [
    {model: DB.Mob, as: 'att_mob', where: sequelize.where(sequelize.col('battle.group_id'), sequelize.col('battle->att_mob.group_id')), required: false},
    {model: DB.Mob, as: 'def_mob', where: sequelize.where(sequelize.col('battle.group_id'), sequelize.col('battle->def_mob.group_id')), required: false},
    {model: DB.Troll, as: 'att_troll', where: sequelize.where(sequelize.col('battle.group_id'), sequelize.col('battle->att_troll.group_id')), required: false},
    {model: DB.Troll, as: 'def_troll', where: sequelize.where(sequelize.col('battle.group_id'), sequelize.col('battle->def_troll.group_id')), required: false}
  ]},
  {override: true}
);
// AA
DB.AA.addScope('defaultScope', {
  include: [
    {model: DB.Troll, as: 'troll', where: sequelize.where(sequelize.col('aa.group_id'), sequelize.col('aa->troll.group_id')), required: false},
    {model: DB.Troll, as: 'troll_cible', where: sequelize.where(sequelize.col('aa.group_id'), sequelize.col('aa->troll_cible.group_id')), required: false}
  ]},
  {override: true}
);
// CDM
DB.CDM.addScope('defaultScope', {
  include: [
    {model: DB.Mob, where: sequelize.where(sequelize.col('cdm.group_id'), sequelize.col('cdm->mob.group_id')), required: false},
    {model: DB.Troll, where: sequelize.where(sequelize.col('cdm.group_id'), sequelize.col('cdm->troll.group_id')), required: false}
  ]},
  {override: true}
);
// PIEGE
DB.Piege.addScope('defaultScope', {
  include: [
    {model: DB.Troll, where: sequelize.where(sequelize.col('piege.group_id'), sequelize.col('piege->troll.group_id')), required: false}
  ]},
  {override: true}
);
// PORTAL
DB.Portal.addScope('defaultScope', {
  include: [
    {model: DB.Troll, where: sequelize.where(sequelize.col('portal.group_id'), sequelize.col('portal->troll.group_id')), required: false}
  ]},
  {override: true}
);
// IDC
DB.IDC.addScope('defaultScope', {
  include: [
    {model: DB.Troll, where: sequelize.where(sequelize.col('idc.group_id'), sequelize.col('idc->troll.group_id')), required: false}
  ]},
  {override: true}
);
// User
DB.User.addScope('defaultScope', {include: [{model: DB.Troll}, {model: DB.AssocUsersGroups, as: 'assocs'}]}, {override: true});
// Events
DB.Event.addScope('defaultScope', {include: [{model: DB.CDM}, {model: DB.Battle}, {model: DB.Piege}, {model: DB.Portal}, {model: DB.IDC}, {model: DB.AA}]}, {override: true});

module.exports = DB;
