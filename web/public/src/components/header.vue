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
                    <v-menu offset-y open-on-hover v-if='maisonnee.length > 0'>
						<template v-slot:activator="{ on, attrs }">
					        <v-btn v-bind="attrs" v-on="on" text>Maisonnée</v-btn>
						</template>
						<v-list v-for="troll in maisonnee">
	                        <v-list-item @click='switchMaisonnee(troll.id)'>
					            <v-img class="d-none d-lg-flex" v-if="troll.blason_uri" :src="troll.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="50px" max-width="100px"></v-img>
            					<v-img class="d-none d-lg-flex" v-else :src="Image('unknown')" alt="" contain max-width="100px" max-height="50px"></v-img>
            					<span class="text-capitalize subheading mr-3 d-none d-lg-flex">{{troll.nom}}</span>
                            </v-list-item>
						</v-list>
					</v-menu>
					<v-btn @click="logout()" color="red" text>Déconnexion</v-btn>
				</v-row>
			</v-col>
		</v-row>
	</v-app-bar>
</template>

<!-- SCRIPT -->
<script>
import { getMaisonnee, loginAs } from '~/src/api.js';

export default {
	name: 'HeaderView',
	data() {
		return {
            maisonnee: []
	    }
    },
    methods: {
		logout() {
			this.$store.commit('logout');
			this.$router.push('/');
		},
        switchMaisonnee(id) {
            loginAs(id)
				.then(res => {
					if (res.status === 200) {
                        window.location.reload();
                    }
				});
        }
	},
    beforeMount() {
        if (this.$store.getters.isAuthenticated()) {
            getMaisonnee()
				.then(res => {
					if (res.status === 200) {
                        this.maisonnee = res.data['maisonnee'];
					}
				});
        }
    }
}
</script>
