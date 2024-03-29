import axios from 'axios'

// DEBUG MODE ONLY
//export const API_URL = 'http://127.0.0.1:8080/api'
//export const API_URL = 'https://www.sciz.fr/api'
// PRODUCTION MODE ONLY
export const API_URL = '/api'

// INTERCEPTORS

// Ensure a cross-browser no-cache for xhr
/*
axios.interceptors.request.use(function (config) {
		config.url += '?t=' + Date.now();
		return config;
	}, function (error) {
		return Promise.reject(error);
	});
	*/

// MOBS
export function getMobs(req) {
	return axios.post(API_URL + '/mobs', req);
}

export function getnbCDM() {
	return axios.get(API_URL + '/nbCDM');
}

// MH_CALL
export function doMHCall(script) {
	return axios.post(API_URL + '/mh_sp_call/' + script);
}

// PROFIL
export function getUsersList(coterie_id) {
	return axios.get(API_URL + '/users/' + coterie_id);
}

export function getProfil() {
	return axios.get(API_URL + '/profil');
}

export function saveProfil(userData) {
	return axios.post(API_URL + '/profil', userData);
}

export function deleteProfil() {
	return axios.delete(API_URL + '/profil');
}

export function getMhCalls(page) {
	return axios.get(API_URL + '/calls/' + page);
}

// MAISONNEE
export function getMaisonnee() {
	var url = API_URL + '/maisonnee';
	return axios.get(url);
}

export function loginAs(id) {
	var url = API_URL + '/login_as/' + id;
	return axios.post(url);
}

// COTERIES
export function getGroups(withInvites, withHooks) {
	var url = API_URL + '/groups';
	if (withInvites) {
		url += '/withinvites'
	}
	if (withHooks) {
		url += '/withhooks'
	}
	return axios.get(url);
}

export function getGroup(id) {
	var url = API_URL + '/group/' + id;
	return axios.get(url);
}

export function setGroup(id, groupData) {
	return axios.post(API_URL + '/group/' + id, groupData);
}

export function acceptInvite(id, partage) {
	return axios.post(API_URL + '/share/invite/' + id, partage);
}

export function declineInvite(id) {
	return axios.delete(API_URL + '/share/invite/' + id);
}

export function deleteShare(coterie_id) {
	return axios.delete(API_URL + '/shares/' + coterie_id);
}

export function deleteGroup(coterie_id) {
	return axios.delete(API_URL + '/group/' + coterie_id);
}

export function createGroup(groupData) {
	return axios.post(API_URL + '/group/create', groupData);
}

export function getPartages(id) {
	return axios.get(API_URL + '/shares/' + id);
}

// HOOKS
export function renewHook(hook_id) {
	return axios.post(API_URL + '/hook/renew/' + hook_id);
}

export function getFormat(hook_id) {
	return axios.get(API_URL + '/hook/format/' + hook_id)
}

export function saveFormat(hook_id, format) {
	return axios.post(API_URL + '/hook/format/' + hook_id, format)
}

export function getBestiaire(req) {
	return axios.post(API_URL + '/bestiaire', req)
}

export function resetFormat(hook_id) {
	return axios.delete(API_URL + '/hook/format/' + hook_id)
}

// EVENTS
export function getEvents(coterie_id, limit, offset, lastID, revert) {
	if (limit === undefined) {
		limit = 25;
	}
	if (offset === undefined) {
		offset = 0;
	}
	if (lastID === undefined) {
		lastID = 0;
	}
	var url = API_URL + '/events/' + coterie_id + '/' + limit + '/' + offset + '/' + lastID;
	if (revert) {
		url += '/revert'
	}
	return axios.get(url);
}

export function deleteEvent(event_id) {
	return axios.delete(API_URL + '/events/' + event_id);
}
