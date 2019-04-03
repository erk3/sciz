import axios from 'axios'

// DEBUG MODE ONLY
const API_URL = 'http://127.0.0.1:8080/api'
// PRODUCTION MODE ONLY
// const API_URL = '/api'

// INTERCEPTORS

// Ensure a cross-browser no-cache for xhr
axios.interceptors.request.use(function (config) {
    config.url += '?t=' + Date.now();
		return config;
  }, function (error) {
    return Promise.reject(error);
  });

// HOME
export function stats() {
	return axios.get(API_URL + '/stats');
}

export function authenticate(userData) {
	return axios.post(API_URL + '/login', userData);
}

export function register(userData) {
  return axios.post(API_URL + '/register', userData);
}

// MOBS
export function getMobs() {
	return axios.get(API_URL + '/mobs');
}

export function getnbCDM() {
	return axios.get(API_URL + '/nbCDM');
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

export function resetPassword(pwdData) {
  return axios.post(API_URL + '/resetPassword', pwdData);
}

// COTERIES
export function getGroups(withWebPad, withInvites, withHooks) {
	var url = API_URL + '/groups';
	if (withWebPad) {
		url += '/withwebpad'
	}
	if (withInvites) {
		url += '/withinvites'
	}
	if (withHooks) {
		url += '/withhooks'
	}
	return axios.get(url);
}

export function getGroup(id, withWebPad) {
	var url = API_URL + '/group/' + id;
	if (withWebPad) {
		url += '/webpad'
	}
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

// MAP
export function getMapUser() {
	var path = API_URL + '/map/user';
	return axios.get(path);
}

export function getMapData(type, days, portee, pos_x, pos_y, pos_n) {
	var path = API_URL + '/map/data/' + type + '/' + days + '/' + portee + '/' + pos_x + '/' + pos_y;
	if (pos_n !== undefined) {
		path += '/' + pos_n
	}
	return axios.get(path);
}

export function getMapCount(type, days, portee, pos_x, pos_y, pos_n) {
	var path = API_URL + '/map/count/' + type + '/' + days + '/' + portee + '/' + pos_x + '/' + pos_y;
	if (pos_n !== undefined) {
		path += '/' + pos_n
	}
	return axios.get(path);
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

export function request(req) {
	return axios.post(API_URL + '/user/request', req)
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
