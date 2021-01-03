<!-- TEMPLATE -->
<template>
	<v-app-bar app fixed clipped-left>
		<!-- MAIN MENU -->
		<v-row align="center" justify="center" no-gutters>
			<!-- LOGO -->
			<v-img class="d-none d-md-flex" :src="Image('logo')" alt="" contain max-width="100px" max-height="50px" class="pa-3 mr-3 ml-3"></v-img>
			<!-- LEFT SIDE -->
			<v-col align="left">
				<v-btn :to="{name: 'HomeView'}" v-if="!isAuthenticated()" text>Accueil</v-btn>
				<v-btn :to="{name: 'EventView'}" v-if="isAuthenticated()" text >Volière</v-btn>
				<v-btn :to="{name: 'BestiaryView'}" v-if="isAuthenticated()" text >Bestiaire</v-btn>
				<v-btn :to="{name: 'PadView'}" v-if="isAuthenticated()" text >Calepin</v-btn>
			</v-col>
			<!-- RIGHT SIDE -->
			<v-col align="right" v-if="isAuthenticated()">
				<v-row align="center" justify="end">
					<v-img class="d-none d-lg-flex" v-if="userData().blason_uri" :src="userData().blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="50px" max-width="100px"></v-img>
					<v-img class="d-none d-lg-flex" v-else :src="Image('unknown')" alt="" contain max-width="100px" max-height="50px"></v-img>
					<span class="text-capitalize subheading mr-3 d-none d-lg-flex">{{userData().nom}}</span>
					<v-divider vertical class="d-none d-lg-flex"></v-divider>
					<v-btn :to="{name: 'ProfilView'}" text class="ml-3">Profil</v-btn>
					<v-btn :to="{name: 'ShareView'}" text >Coteries</v-btn>
					<v-btn @click="logout()" color="red" text>Déconnexion</v-btn>
				</v-row>
			</v-col>
		</v-row>
	</v-app-bar>
</template>

<!-- SCRIPT -->
<script>
export default {
	name: 'HeaderView',
	methods: {
		logout () {
			this.$store.commit('logout');
			this.$router.push('/');
		}
	}
}
</script>
