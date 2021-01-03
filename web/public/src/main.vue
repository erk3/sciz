<!-- TEMPLATE -->
<template>
	<v-app>
		<HeaderView></HeaderView>
		<v-main>
			<v-container fluid pa-0 ma-0 fill-height>
				<router-view></router-view>
			</v-container>
		</v-main>
		<FooterView></FooterView>
	</v-app>
</template>

<!-- SCRIPT -->
<script>
import WebFontLoader from 'webfontloader';
import HeaderView from '~/src/components/header.vue';
import FooterView from '~/src/components/footer.vue';

export default {
	name: 'AppMain',
	components: { HeaderView, FooterView },
	beforeMount () {
		// Set dark/light mode
		var mode = localStorage.getItem('mode');
		this.$store.commit('setMode', (mode === null) ? 'light' : mode);
		this.$vuetify.theme.dark = mode === 'dark';
		// Set last coterie ID
		var coterieID = localStorage.getItem('coterieID');
		this.$store.commit('setCoterieID', (coterieID === null) ? -1 : JSON.parse(coterieID));
		var coterieName = localStorage.getItem('coterieName');
		this.$store.commit('setCoterieName', (coterieName === null) ? '' : JSON.parse(coterieName));
	},
	mounted () {
		// Loadt the fonts
		WebFontLoader.load({
			google: {
				families: ['Roboto:400', 'Montserrat:400'],
			},
			active: this.setFontLoaded
		});
	},
	methods: {
		setFontLoaded () {
			this.$emit('font-loaded')
		}
	}
}
</script>

<!-- STYLE -->
<style>
.v-application, [class^="display-"], [class^="body-"], .headline, .subheading, .title, .caption {
	font-family: Roboto !important;
	font-size: 14px;
}
.theme--dark.v-application {
	background: #303030;
	color: #fff;
}
.theme--light.v-application {
	background: #fafafa;
	color: rgba(0,0,0,.87);
}
.v-icon {
	display: inline-flex;
}
.v-navigation-drawer {
	z-index: 0;
	background-color: transparent !important;
}
.v-image__image--preload {
	filter: unset !important;
}
</style>
