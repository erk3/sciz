const path = require('path');
const request = require('request');

var config;
var db;
var ws;

/*
 * Plugin init
 */

exports.name = "sciz";

exports.provider = {
	key: "sciz",
	command: "sciz",
	botName: "SCIZ-Bot",
	botAvatar: {src:'url', key:'https://i.imgur.com/sfd9VyY.png'},
	botInfo: {location: 'quelque part entre un troll et son zhumain',
		lang: 'fr',
		description: "je suis une chauve-souris" },
	help: "permet d'interagir avec SCIZ",
	detailedHelp: "#lang-md"
								+ "\n * `!!sciz request [help|$cli]` requête l'instance SCIZ associée a cette salle"
								+ "\n * `!!sciz unregister` supprime le hook associé à la salle"
								+ "\n * `!!sciz register $url $jwt` enregistre un hook pour cette salle"
								+ "\n * `!!sciz callback` affiche le point d'accès du plugin SCIZ pour ce serveur"
}

const providers = [exports.provider];

function initProvider(p){
	return this.getBot(p.botName)
		.then(function(bot){
			p.bot = bot;
			if (p.botAvatar.src === bot.avatarsrc && p.botAvatar.key === bot.avatarkey) {
				return;
			}
			bot.avatarsrc = p.botAvatar.src;
			bot.avatarkey = p.botAvatar.key;
			return this.updateUser(bot);
		})
		.then(function(){
			return this.getUserInfo(p.bot.id);
		})
		.then(function(info){
			if (info.description === p.botInfo.description) {
				return;
			}
			return this.updateUserInfo(p.bot.id, p.botInfo);
		})
		.then(function(){
			return p;
		});
}

exports.init = function(miaou){
	config = miaou.config;
	db = miaou.db;
	ws = miaou.lib("ws");
	miaou.requestTag({
		name: "MountyHall",
		description:
			"https://games.mountyhall.com/mountyhall/Images/Troll_accueil_1.jpg\n"
			+ "*[MountyHall](https://www.mountyhall.com) est un jeu de rôles et d'aventures"
			+ " en ligne permettant aux participants d'incarner un Troll en quête d'aventures. "
			+ "Le jeu se déroule en tour-par-tour d'une durée de 12 heures durant lesquelles"
			+ " les joueurs peuvent faire agir leur Troll en dépensant jusqu'à 6 Points d'Actions.*\n"
			+ "Donner ce tag à une salle Miaou apporte de nombreuses fonctions liées au jeu MountyHall."
	});
	return db.upgrade(exports.name, path.resolve(__dirname, 'sql'))
		.then(function(){
			return db.on(providers)
				.each(initProvider)
				.finally(db.off);
		});
}

/*
 * Route
 */

exports.registerRoutes = function(map){
	providers.forEach(function(p){
		var route = "/" + p.key + "-webhook";
		require('../../libs/anti-csrf.js').whitelist(route);
		map('post', route, (req, res) => scizCalling(p, req, res), true, true);
	});
}


function scizCalling(p, req, res){
	var	jwt = req.headers['authorization'];
	var notifs = req.body;
	if (!jwt || !notifs) {
		return res.status(400).json({message: 'Bad request'});
	}
	res.send('');
	return db.on()
		.then(function(){
			return this.queryOptionalRow(
				"SELECT room FROM sciz WHERE jwt = $1",
				[jwt],
				"sciz / get room"
			);
		})
		.then(function(row){
			if (row && row.room) {
				for (var i = 0; i < notifs.length; i++) {
					ws.botMessage(p.bot, row.room, notifs[i].notif);
				}
			}
		})
		.finally(db.off);
}

/*
 * Commands
 */

exports.registerCommands = function(cb){
	providers.forEach(function(p){
		cb({
			name: p.command,
			fun: ct => onCommand.call(this, ct, p),
			help: p.help,
			detailedHelp: p.detailedHelp
		});
	});
}

function onCommand(ct, p){
	var m;
	if ((m = ct.args.match(/^register\s+([^\s]+)\s+(JWT\s[^\s]+)/))) {
		ct.silent = true;
		ct.nostore = true;
		ct.shoe.checkAuth("admin");
		ws.botMessage(p.bot, ct.shoe.room.id, "Hook SCIZ enregistré pour cette salle");
		return registerRoom.call(this, ct, p, m[1], m[2]);
	}
	if ((m = ct.args.match(/^unregister/))) {
		ct.shoe.checkAuth("admin");
		ws.botMessage(p.bot, ct.shoe.room.id, "Hook SCIZ supprimé pour cette salle");
		return unregisterRoom.call(this, ct, p);
	}
	if ((m = ct.args.match(/^callback/))) {
		ct.shoe.checkAuth("admin");
		ws.botMessage(p.bot, ct.shoe.room.id, config.server + "/" + p.key + "-webhook");
		return;
	}
	if ((m = ct.args.match(/^request(\s+([^\s]+))?(\s+([^\s]+))?(\s+([^\s]+))?/))) {
		ct.shoe.checkAuth("write");
		var arg1 = m[2] ? m[2] : 'help';
		return requestSCIZ.call(this, ct, p, arg1, m[4], m[6]);
	}
	ws.botMessage(p.bot, ct.shoe.room.id, "Commande invalide ou incomplète. `!!help !!" + p.command + "`");
}

function registerRoom(ct, p, url, jwt){
	return db.on()
		.then(function(){
			return this.execute(
				"INSERT INTO sciz (room, url, jwt) VALUES ($1, $2, $3)"
				+ "ON CONFLICT (room) DO UPDATE SET url = $2, jwt = $3;",
				[ct.shoe.room.id, url, jwt],
				"sciz / insert or update hook"
			);
		})
		.finally(db.off);
}

function unregisterRoom(ct, p){
	return db.on()
		.then(function(){
			return this.execute(
				"DELETE FROM sciz WHERE room = $1;",
				[ct.shoe.room.id],
				"sciz / delete hook"
			);
		})
		.finally(db.off);
}

function requestSCIZ(ct, p, arg1, arg2, arg3){
	/* N.B: args check done SCIZ side */
	return db.on()
		.then(function(){
			return this.queryOptionalRow(
				"SELECT url, jwt FROM sciz WHERE room = $1",
				[ct.shoe.room.id],
				"sciz / get hook"
			);
		})
		.then(function(row){
			if (!row || !row.url || !row.jwt) {
				ws.botMessage(p.bot, ct.shoe.room.id, 'Aucun hook SCIZ n\'est enregistré pour cette salle `!!help !!'
					+ p.command + '`');
			}
			var options = {
				method: 'POST',
				url: row.url,
				headers: {
					'Authorization': row.jwt
				},
				json: {'arg1': arg1, 'arg2': arg2, 'arg3': arg3}
			};
			request(options, function(error, response, body){
				if (!error) {
					if (response.statusCode === 200) {
						ws.botMessage(p.bot, ct.shoe.room.id, body.message);
					}
				} else {
					ws.botMessage(p.bot, ct.shoe.room.id,
						'SCIZ est inaccessible ou les paramères du hook enregistrés sont erronés `!!help !!'
						+ p.command + '`');
				}
			});
		})
		.finally(db.off);
}

