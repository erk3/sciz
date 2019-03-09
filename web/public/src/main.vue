<!-- TEMPLATE -->
<template>
	<v-app :dark="this.$store.getters.mode === 'dark'">
		<HeaderView></HeaderView>
		<v-content>
			<v-container fluid pa-0 ma-0 fill-height>
				<router-view></router-view>
			</v-container>
		</v-content>
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
	        families: ['Roboto:100,300,400,500,700,900', 'Montserrat:100,300,400,500,700,900']
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
.application, [class^="display-"],	[class^="body-"], .headline, .subheading, .title, .caption {
	font-family: Montserrat !important;
}
.v-parallax {
	height: 100%;
	min-height: 380px;
}
.v-parallax [class^="display-"], .v-parallax .title {
	text-shadow: 0 1px 10px rgba(0, 0, 0, 0.8);
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
