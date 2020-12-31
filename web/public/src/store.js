// VUEX IMPORT
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

// BUS EVENT
export const EventBus = new Vue()

// Imports of AJAX functions
import axios from 'axios';
import { authenticate, register, reset, saveProfil } from '~/src/api.js'

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
	// Login
	login(context, userData) {
    	return authenticate(userData)
			.then(response => context.commit('setCookie', response.data ))
			  .catch(error => EventBus.$emit('failedAuthentication', error));
	},
	// Register
  	register(context, userData) {
    	return register(userData)
			.then(response => context.commit('setCookie', response.data))
      		.catch(error => EventBus.$emit('failedRegistering', error.response.data.message));
	  },
	// reset
	reset(context, userData) {
    	return reset(userData)
			.then(response => context.commit('setCookie', response.data))
      		.catch(error => EventBus.$emit('failedReset', error.response.data.message));
  	},
	// saveProfil
  	saveProfil(context, userData) {
    	return saveProfil(userData)
			.then(response => {
				context.commit('setName', userData.pseudo);
      				EventBus.$emit('savedProfil', response.data.message);
			})
      		.catch(error => EventBus.$emit('failedSavingProfil', error.response.data.message));
  	}
}

// Isolated data mutations
const mutations = {
	// Cookie
  	setCookie (state, payload) {
		state.jwt = payload.jwt;
		state.user = payload.user;
		// Set cookie
		const data = JSON.parse(atob(state.jwt.split('.')[1]));
		window.$cookies.set('sciz', state, new Date(data.exp * 1000), '/', data.dom, data.secure);
		// Set the authorization header
		axios.defaults.headers.common['Authorization'] = state.jwt;
  	},
	// setName
  	setName (state, nom) {
		state.user.nom = nom;
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
		state.user = {}
		window.$cookies.remove('sciz');
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
			if (!state.jwt || state.jwt.split('.').length < 3) {
	    		return false;
	  		}
	  		const data = JSON.parse(atob(state.jwt.split('.')[1]));
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
