<!-- TEMPLATE -->
<template>
	<v-layout justify-center align-center fill-height id="home-view">
		<v-flex xs6 text-xs-center>
      <v-card flat tile class="transparent">
        <v-img :src="Image('logo')" contain max-height="200px"></v-img>

        <v-card-text primary-title>
						<h3 class="headline mb-2"><u>S</u>ystème de <u>C</u>hauve-souris <u>I</u>nterdimensionnel pour <u>Z</u>humain</h3>
						<p>Déjà {{user_count}} utilisateurs inscrits et {{event_count_last_month}} événements traités le mois dernier !</p>
        </v-card-text>

        <v-card-actions>
					<v-spacer></v-spacer>
					<v-btn icon @click="show_desc = !show_desc">
            <v-icon>{{ show_desc ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
          </v-btn>
					<v-spacer></v-spacer>
        </v-card-actions>

				<v-slide-y-transition>
          <v-card-text v-show="show_desc">
						<p class="caption">
							SCIZ est une interface tactique tournée vers <a href="http://www.mountyhall.com/">MountyHall</a> et destinée aux groupes de chasse.<br/>
							Sa fonction première est d'aggréger, consolider, conserver et partager automagiquement les notifications mail envoyées par le jeu à chaque trõll.<br/>
							Il permet en particulier de retrouver ces informations sur Miaou, Hangouts ou Discord.
						</p>
          </v-card-text>
        </v-slide-y-transition>

				<v-window v-model="step" v-if="!isAuthenticated()">
					<!-- LOGIN -->
					<v-window-item :value="1">
						<v-form v-model="valid_form_login" @keyup.native.enter="authenticate" v-on:submit.prevent>
			        <v-card-actions>
								<v-layout row wrap>
									<v-flex d-flex>
										<v-layout row wrap justify-center>
											<v-text-field label="Identifiant" prepend-icon="fas fa-user" v-model="id" hint="Votre numéro de trõll" :error="id !== '' && error" :rules="[emptyRule, idRule]" required browser-autocomplete="username" name="username"></v-text-field>
											<v-spacer></v-spacer>
											<v-text-field label="Mot de passe" prepend-icon="fas fa-lock" v-model="pwd" :append-icon="show_pwd ? 'visibility_off' : 'visibility'" :type="show_pwd ? 'text' : 'password'" @click:append="show_pwd = !show_pwd" :error="pwd !== '' && error" :rules="[emptyRule]" required hint="Perdu votre mot de passe ? <a href='https://games.mountyhall.com/mountyhall/Messagerie/MH_Messagerie.php?cat=3&dest=104126' target='_blank'>Contactez moi !</a>" browser-autocomplete="current-password" name="password"></v-text-field>
										</v-layout>
									</v-flex>
									<v-flex d-flex xs12 class="mt-3">
										<v-layout row wrap justify-center>
			          			<v-btn color="primary" depressed @click="authenticate" class="ma-1" :disabled="id === '' || pwd === ''">Connexion</v-btn>
	    		      			<v-btn depressed @click="step++; error=false" class="ma-1">Inscription</v-btn>
										</v-layout>
									</v-flex>
								</v-layout>
			        </v-card-actions>
			      </v-form>
					</v-window-item>
					<!-- REGISTER -->
      		<v-window-item :value="2">
						<v-form v-model="valid_form_register" @keyup.native.enter="register">
							<v-alert v-model="error" type="error" :dismissible=true> {{error_msg}} </v-alert>
							<v-card-actions>
								<v-layout row wrap>
									<v-flex d-flex>
										<v-layout row wrap justify-center>
											<v-text-field label="Identifiant" prepend-icon="fas fa-user" v-model="id" hint="Votre numéro de trõll" :error="id !== '' && error" :rules="[emptyRule, idRule]" required></v-text-field>
											<v-spacer></v-spacer>
											<v-text-field label="Code d'accès à MountyHall" prepend-icon="fas fa-key" v-model="pwd_mh" :error="pwd_mh !== '' && error" hint="<a href='http://sp.mountyhall.com/hashing.php' target='_blank'>Qu'est ce que c'est ?</a>" :rules="[emptyRule]" required></v-text-field>
										</v-layout>
									</v-flex>
									<v-flex d-flex>
										<v-layout row wrap justify-center>
											<v-text-field label="Mot de passe" prepend-icon="fas fa-lock" v-model="pwd" :append-icon="show_pwd ? 'visibility_off' : 'visibility'" :type="show_pwd ? 'text' : 'password'" @click:append="show_pwd = !show_pwd" :error="pwd !== '' && error" counter :rules="[emptyRule, pwdRule]" :success="pwdMatch(false)" required browser-autocomplete="new-password"></v-text-field>
											<v-spacer></v-spacer>
											<v-text-field label="Confirmation" prepend-icon="fas fa-lock" v-model="pwd2" :append-icon="show_pwd ? 'visibility_off' : 'visibility'" :type="show_pwd ? 'text' : 'password'" @click:append="show_pwd = !show_pwd" :error="pwd2 !== '' && error" counter :rules="[emptyRule]" :error-messages="pwdMatch(true)" :success="pwdMatch(false)" required browser-autocomplete="new-password"></v-text-field>
										</v-layout>
									</v-flex>
									<v-flex d-flex xs12 class="mt-3">
										<v-layout row wrap justify-center>
											<v-btn depressed @click="step--; error=false">Connexion</v-btn>
											<v-btn color="primary" depressed @click="register" :disabled="id === '' || pwd === '' || pwd !== pwd2 || pwd_mh === ''">Inscription</v-btn>
										</v-layout>
									</v-flex>
								</v-layout>
			        </v-card-actions>
			      </v-form>
					</v-window-item>
				</v-window>
      </v-card>
    </v-flex>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	import { EventBus } from '~/src/store.js'
	import { stats } from '~/src/api.js'

	export default {
    name: 'HomeView',
		data: () => ({
			id: '',
			pwd: '',
			pwd2: '',
			pwd_mh: '',
			user_count: 0,
			event_count_last_month: 0,
			error: false,
			error_msg: '',
      show_desc: false,
			show_pwd: false,
			step: 1,
			valid_form_login: false,
			valid_form_register: false,
			emptyRule: v => !!v || "",
			idRule: v => /^\d+$/.test(v) || "Numéro de trõll invalide",
			pwdRule: v => v.length >= 8 || "Au moins 8 caractères"
    }),
		methods: {
			pwdMatch (error) {
				if (this.pwd === '' || this.pwd2 === '') {
					return error ? '' : false
				} else {
					return (this.pwd === this.pwd2) ? (error ? '' : true) : (error ? 'Le mot de passe ne correspond pas' : false)
				}
			},
    	authenticate () {
				if (this.id !== '' && this.pwd !== '') {
      		this.$store.dispatch('login', {id: this.id, pwd: this.pwd })
						.then(() => {
							if(this.$route.params.nextUrl !== undefined && this.$route.params.nextUrl !== null) {
              	this.$router.push(this.$route.params.nextUrl);
							} else {
								this.$router.push('/event');
							}
						});
				}
			},
	    register () {
      	this.$store.dispatch('register', {id: this.id, pwd: this.pwd, pwd2: this.pwd2, pwd_mh: this.pwd_mh })
	        .then(() => this.$router.push('/profil'))
	    }
	  },
		beforeMount () {
			stats()
				.then(res => {
					if (res.status === 200) {
						this.user_count = res.data['user_count'];
						this.event_count_last_month = res.data['event_count_last_month'];
					}
				})
 		},
		mounted () {
			EventBus.$on('failedRegistering', err => {this.error = true; this.error_msg = err})
			EventBus.$on('failedAuthentication', () => this.error = true)
	  },
	  beforeDestroy () {
	    EventBus.$off('failedRegistering')
	    EventBus.$off('failedAuthentication')
	  }
  }
</script>
