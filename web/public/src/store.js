// VUEX IMPORT
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

// BUS EVENT
export const EventBus = new Vue()

// Imports of AJAX functions
import axios from 'axios';
import { saveProfil } from '~/src/api.js'

// Single source of data
const state = {
    jwt: '',
	user: {},
	mode: 'light',
	coterieID: -1,
	coterieName: '',
}

// Asynchronous operations
const actions = {
	// saveProfil
	saveProfil(context, userData) {
		return saveProfil(userData)
			.then(response => {
				EventBus.$emit('savedProfil', response.data.message);
			})
			.catch(error => EventBus.$emit('failedSavingProfil', error.response.data.message));
	}
}

// Isolated data mutations
const mutations = {
	// Cookie
	setSession (state, jwt) {
        state.jwt = jwt;
		const data = JSON.parse(atob(jwt.split('.')[1]));
        state.user = {'id': data.identity, 'nom': data.nom, 'blason_uri': data.blason_uri}
		// window.$cookies.set('sciz', state, new Date(data.exp * 1000), '/', data.dom, data.secure);
		// Set the authorization header
		axios.defaults.headers.common['Authorization'] = jwt;
	},
	// Mode
	setMode (state, mode) {
		state.mode = mode;
		localStorage.setItem('mode', state.mode);
	},
	// CoterieID
	setCoterieID (state, coterieID) {
		state.coterieID = coterieID;
		localStorage.setItem('coterieID', JSON.stringify(state.coterieID));
	},
	// CoterieName
	setCoterieName (state, coterieName) {
		state.coterieName = coterieName;
		localStorage.setItem('coterieName', JSON.stringify(state.coterieName));
	},
	// Logout
	logout(state) {
		state.jwt = '';
		state.user = {};
		window.$cookies.remove('sciz_session');
	}
}

// Reusable data accessors
const getters = {
	// userData
	userData(state) {
		return state.user;
	},
	// Mode
	mode(state) {
		return state.mode;
	},
	// Coterie ID
	coterieID(state) {
		return state.coterieID;
	},
	// Coterie Name
	coterieName(state) {
		return state.coterieName;
	},
	// isAuthenticated
	isAuthenticated(state) {
		return () => {
		    var jwt = state.jwt;
			if (!jwt || jwt.split('.').length < 3) {
				return false;
			}
			const data = JSON.parse(atob(jwt.split('.')[1]));
			const exp = new Date(data.exp * 1000);
			const now = new Date();
			if (!(now < exp)) {
				mutations.logout(state);
			}
			return now < exp;
		}
	}
}

// MAIN STORE
const store = new Vuex.Store({
	state,
	actions,
	mutations,
	getters
})

export default store
