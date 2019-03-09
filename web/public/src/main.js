// VUEJS IMPORT
import 'babel-polyfill';
import Vue from 'vue';

// VUE RESOURCE IMPORT
import VueResource from 'vue-resource';
Vue.use(VueResource);
Vue.http.options.root = '/api/';

// VUETIFY IMPORT
import Vuetify from 'vuetify';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import 'vuetify/dist/vuetify.min.css';
import '@fortawesome/fontawesome-free/css/all.css';
Vue.use(Vuetify, {iconfont: 'fa'});

// VUE NATIVE NOTIFICATION
import VueNativeNotification from 'vue-native-notification';
Vue.use(VueNativeNotification, { requestOnNotify: true });

// VUE CLIPBOARD
import VueClipboard from 'vue-clipboard2';
Vue.use(VueClipboard);

// VUE CLICK OUTSIDE
import vClickOutside from 'v-click-outside'
Vue.use(vClickOutside)

// MOMENT
import VueMoment from 'vue-moment';
Vue.use(VueMoment);

// LODASH
import VueLodash from 'vue-lodash';
Vue.use(VueLodash);

// COOKIES
import VueCookies from 'vue-cookies';
Vue.use(VueCookies);

// STORE (VUEX)
import store from '~/src/store.js';

// ROUTES
import router from '~/src/routes.js';

// MAIN
import AppMain from '~/src/main.vue';
import Images from './assets/images/*.*';

Vue.mixin({
	methods:{
		isAuthenticated: function () {
			return this.$store.getters.isAuthenticated();
		},
		userData: function () {
			return this.$store.getters.userData;
		},
		displayMinMax: function (min, max, short) {
			if (min && max) {
				if (min === max) {
					if (short) {
						return max;
					}
					return 'égal à ' + max;
				}
				if (short) {
					return min + ' - ' + max;
				}
				return 'entre ' + min + ' et ' + max;
			} else if (max) {
				if (short) {
					return '< ' + max;
				}
				return 'inférieur à' + max;
			} else if (min) {
				if (short) {
					return '> ' + min;
				}
				return 'supérieur à' + min;
			}
			return '-';
		},
		boolean2french: function (bool) {
			if (bool === undefined || bool === null) {
				return '-';
			}
			return (bool) ? 'Oui' : 'Non';
  	},
	},
	data() {
		Image: {
			return {
      	Image(name) {
					return Object.values(Images[name])[0];
      	}
	    }
	  }
	}
})

var vm = new Vue({
	el: '#main',
	router,
	store,
	render: h => h(AppMain)
});
