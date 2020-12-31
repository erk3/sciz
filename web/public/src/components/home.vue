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
				<v-icon size="16px">fas {{ show_desc ? 'fa-chevron-down' : 'fa-chevron-up' }}</v-icon>
			</v-btn>
			<v-spacer></v-spacer>
			<v-slide-y-transition>
				<p class="caption" v-show="show_desc">
					SCIZ est un outil tourné vers <a href="https://www.mountyhall.com/">MountyHall</a> et destiné aux groupes de chasse.<br/>
					Sa fonction première est d'aggréger, consolider, conserver et partager automagiquement les notifications mail envoyées par le jeu à chaque trõll.<br/>
					Il permet en particulier de retrouver ces informations sur Mountyzilla, Miaou, Hangouts ou Discord.
				</p>
			</v-slide-y-transition>
		</v-card-text>
		<!-- LOGIN / REGISTER -->
		<v-row justify="center">
			<v-col cols="6">
				<v-window v-model="step" v-if="!isAuthenticated()">
					<!-- LOGIN -->
					<v-window-item :value="1">
						<v-form v-model="valid_form_login" @keyup.native.enter="authenticate" v-on:submit.prevent>
							<v-row>
								<v-col class="mr-1">
									<v-text-field label="Numéro de trõll" v-model="id" :error="id !== '' && error" :rules="[emptyRule, idRule]" required autocomplete="username" name="username">
										<template v-slot:prepend><v-icon size="20px">fas fa-user</v-icon></template>
									</v-text-field>
								</v-col>
								<v-col class="ml-1">
									<v-text-field label="Mot de passe" v-model="pwd" :type="show_pwd ? 'text' : 'password'" :error="pwd !== '' && error" :rules="[emptyRule]" autocomplete="current-password" name="password">
										<template v-slot:prepend><v-icon size="20px">fas fa-lock</v-icon></template>
										<template v-slot:append><v-icon size="20px" @click="show_pwd = !show_pwd">fas {{ show_pwd ? 'fa-eye' : 'fa-eye-slash' }}</v-icon></template>
									</v-text-field>
								</v-col>
							</v-row>
							<v-card-text class="text-center pt-0">
								<v-btn plain @click="step=2; error=false; reset=true;"><a class="caption">Mot de passe oublié ?</a></v-btn>
							</v-card-text>
							<v-row>
								<v-col align="right">
									<v-btn color="primary" depressed @click="authenticate" class="ma-1" :disabled="id === '' || pwd === ''" type="submit">Connexion</v-btn>
								</v-col>
								<v-col align="left">
									<v-btn depressed @click="step=2; error=false" class="ma-1">Inscription</v-btn>
								</v-col>
							</v-row>
						</v-form>
					</v-window-item>
					<!-- REGISTER -->
					<v-window-item :value="2">
						<v-form v-model="valid_form_register" @keyup.native.enter="register">
							<v-alert v-model="error" type="error" :dismissible=true> {{error_msg}} </v-alert>
							<v-row>
								<v-col class="mr-1">
									<v-text-field label="Numéro de trõll" v-model="id" :error="id !== '' && error" :rules="[emptyRule, idRule]" required>
										<template v-slot:prepend><v-icon size="20px">fas fa-user</v-icon></template>
									</v-text-field>
								</v-col>
								<v-col class="ml-1">
									<v-text-field label="Code d'accès à MountyHall" v-model="pwd_mh" :error="pwd_mh !== '' && error" hint="<a href='http://sp.mountyhall.com/hashing.php' target='_blank'>Qu'est ce que c'est ?</a>" :rules="[emptyRule]" required>
										<template v-slot:prepend><v-icon size="20px">fas fa-key</v-icon></template>
										<template v-slot:message='{ message }'><span v-html="message"></span></template>
									</v-text-field>
								</v-col>
							</v-row>
							<v-row>
								<v-col class="mr-1">
									<v-text-field label="Mot de passe" v-model="pwd" :type="show_pwd ? 'text' : 'password'" :error="pwd !== '' && error" counter :rules="[emptyRule, pwdRule]" :success="pwdMatch(false)" required autocomplete="new-password">
										<template v-slot:prepend><v-icon size="20px">fas fa-lock</v-icon></template>
										<template v-slot:append><v-icon size="20px" @click="show_pwd = !show_pwd">fas {{ show_pwd ? 'fa-eye' : 'fa-eye-slash' }}</v-icon></template>
									</v-text-field>
								</v-col>
								<v-col class="ml-1">
									<v-text-field label="Confirmation" v-model="pwd2" :type="show_pwd ? 'text' : 'password'" :error="pwd2 !== '' && error" counter :rules="[emptyRule]" :error-messages="pwdMatch(true)" :success="pwdMatch(false)" required autocomplete="new-password">
										<template v-slot:prepend><v-icon size="20px">fas fa-lock</v-icon></template>
										<template v-slot:append><v-icon size="20px" @click="show_pwd = !show_pwd">fas {{ show_pwd ? 'fa-eye' : 'fa-eye-slash' }}</v-icon></template>
									</v-text-field>
								</v-col>
							</v-row>
							<v-row>
								<v-col align="right">
									<v-btn depressed @click="step=1; error=false; reset=false;">Connexion</v-btn>
								</v-col>
								<v-col align="left">
									<v-btn color="primary" depressed @click="register" :disabled="id === '' || pwd === '' || pwd !== pwd2 || pwd_mh === ''">{{ reset ? 'Réinitialisation' : 'Inscription' }}</v-btn>
								</v-col>
							</v-row>
						</v-form>
					</v-window-item>
				</v-window>
			</v-col>
		</v-row>
	</v-col>
</template>

<!-- SCRIPT -->
<script>
	import { EventBus } from '~/src/store.js'

	export default {
		name: 'HomeView',
		data: () => ({
			id: '',
			pwd: '',
			pwd2: '',
			pwd_mh: '',
			error: false,
			error_msg: '',
			show_desc: false,
			show_pwd: false,
			step: 1,
			reset: false,
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
						})
				}
			},
			register () {
				if (this.reset) {
					this.$store.dispatch('reset', {id: this.id, pwd: this.pwd, pwd2: this.pwd2, pwd_mh: this.pwd_mh })
						.then(() => this.$router.push('/profil'))
				} else {
					this.$store.dispatch('register', {id: this.id, pwd: this.pwd, pwd2: this.pwd2, pwd_mh: this.pwd_mh })
						.then(() => this.$router.push('/profil'))
				}
			}
		},
		mounted () {
			EventBus.$on('failedRegistering', err => {this.error = true; this.error_msg = err})
			EventBus.$on('failedReset', err => {this.error = true; this.error_msg = err})
			EventBus.$on('failedAuthentication', () => this.error = true)
		},
		beforeDestroy () {
			EventBus.$off('failedRegistering')
	    	EventBus.$off('failedReset')
	    	EventBus.$off('failedAuthentication')
	  	}
	}
</script>

<!-- STYLE -->
<style>
	.v-text-field__details {padding-top: 10px}
</style>