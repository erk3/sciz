// IMPORTS
import Vue from 'vue';
import Router from 'vue-router';
import HomeView from '~/src/components/home.vue';
import EventView from '~/src/components/event.vue';
import BestiaryView from '~/src/components/bestiary.vue';
import PadView from '~/src/components/pad.vue';
import ProfilView from '~/src/components/profil.vue';
import ShareView from '~/src/components/share.vue';
import PageNotFoundView from '~/src/components/404.vue';

// Store (VUEX) must be imported here and not in main.js
import store from '~/src/store.js'

// ROUTES
var router = new Router({
	mode: 'history',
	routes: [
		{
      path: '/',
      redirect: '/home'
    },
		{
			path: '/home',
			name: 'HomeView',
			component: HomeView
		},
		{
			path: '/event',
			name: 'EventView',
			component: EventView,
			meta: {
				requiresAuth: true
			}
		},
		{
			path: '/bestiary',
			name: 'BestiaryView',
			component: BestiaryView,
			meta: {
				requiresAuth: true
			}
		},
		{
			path: '/pad',
			name: 'PadView',
			component: PadView,
			meta: {
				requiresAuth: true
			}
		},
		{
			path: '/profil',
			name: 'ProfilView',
			component: ProfilView,
			meta: {
				requiresAuth: true
			}
		},
		{
			path: '/share',
			name: 'ShareView',
			component: ShareView,
			meta: {
				requiresAuth: true
			}
		},
		{
			path: '*',
			name: 'PageNotFoundView',
			component: PageNotFoundView
		}
	]
});

router.beforeEach((to, from, next) => {
	// Try to auto-authenticate
	if (!store.getters.isAuthenticated()) {
		var cookie = window.$cookies.get('sciz');
		if (cookie) {
			store.commit('setCookie', cookie);
	  }
	}
	// Guard for non-authenticated user
	if (to.meta.requiresAuth && !store.getters.isAuthenticated()) {
		next({
      path: '/',
      params: { nextUrl: to.fullPath }
    });
  } else {
  	next();
  }
});

// Must be done after router.beforeEach definition
Vue.use(Router);

export default router;
