<!-- TEMPLATE -->
<template>
	<v-col>
    	<!-- LOGO -->
		<v-img :src="Image('logo')" contain max-height="200px"></v-img>
		<!-- SCIZ -->
		<v-card-text primary-title class="text-center">
			<h3 class="headline mb-2"><u>S</u>ystème de <u>C</u>hauve-souris <u>I</u>nterdimensionnel pour <u>Z</u>humain</h3>
			<!-- DESCRIPTION -->
			<v-spacer></v-spacer>
			<v-btn icon @click="show_desc = !show_desc">
				<v-icon size="16px">fas {{ show_desc ? 'fa-chevron-up' : 'fa-chevron-down' }}</v-icon>
			</v-btn>
			<v-spacer></v-spacer>
			<v-slide-y-transition>
				<p class="caption" v-show="show_desc">
				SCIZ est un outil tourné vers <a href="https://www.mountyhall.com/">MountyHall</a> et destiné aux groupes de chasse.<br/>
				Sa fonction première est d'aggréger, consolider, conserver et partager automagiquement les notifications mail envoyées par le jeu à chaque trõll.<br/>
				Il permet en particulier de retrouver ces informations sur Mountyzilla, Miaou ou Discord.
				</p>
			</v-slide-y-transition>
		</v-card-text>
		<!-- LOGIN / REGISTER -->
		<v-row justify="center">
            <v-btn color="primary" depressed href="/api/login" class="ma-1" type="submit" v-if="!isAuthenticated()">Connexion</v-btn>
		</v-row>
		<v-row justify="center">
            <v-chip v-if="show_error" class="ma-2" color="error" text-color="white" @click="show_error = false">
                Erreur d'authentification MountyHall
            </v-chip>
		</v-row>
	</v-col>
</template>

<!-- SCRIPT -->
<script>
import { API_URL } from '~/src/api.js'

export default {
	name: 'HomeView',
	data: () => ({
		show_desc: false,
        show_error: false
	}),
    beforeMount() {
        this.show_error = this.$route.query.error;
    }
}
</script>

<!-- STYLE -->
<style>
    .v-text-field__details {padding-top: 10px}
</style>
