<!-- TEMPLATE -->
<template>
  <v-toolbar app fixed clipped-left>
		<!-- MAIN MENU -->
		<v-layout fill-height justify-start align-start row wrap class="hidden-xs-only">
			<!-- LOGO -->
			<v-img :src="Image('logo')" alt="" contain max-width="120px" height="100%"></v-img>
			<!-- LEFT SIDE -->
			<v-toolbar-items>
				<v-btn :to="{name: 'HomeView'}" v-if="!isAuthenticated()" flat>Accueil</v-btn>
				<v-btn :to="{name: 'EventView'}" v-if="isAuthenticated()" flat>Volière</v-btn>
				<v-btn :to="{name: 'BestiaryView'}" v-if="isAuthenticated()" flat>Bestiaire</v-btn>
				<v-btn :to="{name: 'PadView'}" v-if="isAuthenticated()" flat>Calepin</v-btn>
			</v-toolbar-items>
			<!-- RIGHT SIDE -->
			<v-spacer></v-spacer>
			<v-toolbar-items v-if="isAuthenticated()">
				<v-menu offset-y>
					<v-btn slot="activator" flat>
						<v-toolbar-side-icon class="ma-0">
							<v-img v-if="userData().blason_uri" :src="userData().blason_uri" :lazy-src="Image('unknown')" alt="" height="100%"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain height="100%"></v-img>
						</v-toolbar-side-icon>
						<v-toolbar-title class="ma-1"><span class="text-capitalize subheading">{{userData().nom}}</span><v-icon>arrow_drop_down</v-icon></v-toolbar-title>
					</v-btn>
        	<v-list>
						<v-list-tile :to="{name: 'ProfilView'}">Gérer mon profil</v-list-tile>
						<v-list-tile :to="{name: 'ShareView'}">Gérer mes coteries</v-list-tile>
						<v-divider></v-divider>
          	<v-list-tile @click="logout()" class="red--text text-darken1">Déconnexion</v-list-tile>
        	</v-list>
      	</v-menu>
			</v-toolbar-items>	
		</v-layout>
		<!-- SMALL SIZE MENU -->
		<v-layout class="hidden-sm-and-up">
			<v-menu>
			  <v-toolbar-side-icon slot="activator">
					<v-img :src="Image('logo')" alt=""></v-img>
			  </v-toolbar-side-icon>
				<v-list>
					<v-list-tile :to="{name: 'HomeView'}" v-if="!isAuthenticated()">Accueil</v-list-tile>
					<v-list-tile :to="{name: 'EventView'}" v-if="isAuthenticated()">Volière</v-list-tile>
					<v-list-tile :to="{name: 'BestiaryView'}" v-if="isAuthenticated()">Bestiaire</v-list-tile>
					<v-list-tile :to="{name: 'PadView'}" v-if="isAuthenticated()">Calepins</v-list-tile>
					<v-divider v-if="isAuthenticated()"></v-divider>
					<v-list-tile v-if="isAuthenticated()" :to="{name: 'ProfilView'}">Gérer mon profil</v-list-tile>
					<v-list-tile v-if="isAuthenticated()" :to="{name: 'ShareView'}">Gérer mes coteries</v-list-tile>
					<v-divider v-if="isAuthenticated()"></v-divider>
          <v-list-tile v-if="isAuthenticated()" @click="logout()" class="red--text text-darken1">Déconnexion</v-list-tile>
				</v-list>
			</v-menu>	
		</v-layout>
  </v-toolbar>
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

<!-- STYLE -->
<style>
.disable-events {
  pointer-events: none
}
</style>
