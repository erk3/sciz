<!-- TEMPLATE -->
<template>
	<v-layout row justify-center align-center ill-height id="profil-view" ma-5>
		<!-- SIDEBAR -->
		<v-card flat tile floating class="transparent d-inline-block text-xs-center hidden-sm-and-down">
			<v-navigation-drawer app floating value="true">
				<v-layout align-center justify-end fill-height>
					<v-flex xs12 pl-5>
						<v-img v-if="userData().blason_uri" :src="userData().blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="300px"></v-img>
						<v-img v-else :src="Image('unknown')" alt="" contain max-height="300px"></v-img>
						<br/><h3 class="text-capitalize subheading">{{userData().nom}}</h3>
						<h5 class="text-capitalize caption">({{userData().id}})</h5>
					</v-flex>
				<v-layout>
			</v-navigation-drawer>
		</v-card>
		<v-flex xs12 md10 text-xs-center>
			<v-snackbar v-model="error" color="error" :timeout="6000" top>
      	{{ error_msg }}
      	<v-btn dark flat @click="error = false">Fermer</v-btn>
    	</v-snackbar>
			<v-snackbar v-model="success" color="success" :timeout="6000" top>
      	{{ success_msg }}
      	<v-btn dark flat @click="success = false">Fermer</v-btn>
    	</v-snackbar>
			<v-snackbar v-model="info" color="info" :timeout="6000" top>
	  		{{ info_msg }}
		    <v-btn dark flat @click="info = false">Fermer</v-btn>
		  </v-snackbar>
			<v-card flat tile class="transparent">
				<v-form v-model="valid">
				<!-- SCIZ PREFS -->
				<v-expansion-panel expand inset :value="[true]">
      		<v-expansion-panel-content hide-actions readonly>
        		<div slot="header" class="title">Mon profil SCIZ</div>
        		<v-card>
        			<v-card-text>
								<v-layout row wrap align-center justify-center fill-height>
									<v-flex xs8 class="text-xs-center">
										Votre adresse SCIZ<br/>
										<v-tooltip bottom>
											<v-chip slot="activator" v-clipboard:copy="user.sciz_mail" @click="info_msg = 'Adresse copiée dans le presse-papier'; info = true;">
													<v-avatar><v-img :src="Image('logo')" contain></v-img></v-avatar>
													{{user.sciz_mail}}
											</v-chip>
											<span>Cliquer pour copier</span>
										</v-tooltip>
										<br/><br/>
										<v-text-field label="Pseudonyme" v-model="user.pseudo" hint="Lorsque possible, votre pseudonyme remplacera votre nom dans SCIZ"></v-text-field><br/>
										<v-text-field label="Courriel" v-model="user.user_mail" hint="Votre courriel est uniquement utilisé pour vous retourner vos codes de transfert et contrôler l'expéditeur des notifications envoyées à votre boite aux lettres SCIZ" :rules="[mailRule]"></v-text-field><br/>
										<v-tooltip top>
											<v-slider label="Durée de session" v-model="user.session" :thumb-size="24" thumb-label="always" min="1" max="24" always-dirty hint="Durée maximum en heures avant déconnexion de votre session SCIZ" persistent-hint slot="activator"></v-slider>
											<span>Reconnexion nécessaire avant application de la modification</span>
										</v-tooltip><br/>
										<v-switch label="Utiliser le mode sombre" v-model="mode" :input-value="mode" true-value="dark" false-value="light" @change="switchMode(mode)"></v-switch><br/>
										<v-tooltip top>
											<v-switch slot="activator" label="Contribuer au partage communautaire" v-model="user.community_sharing"></v-switch>
											<span>Partage anonyme et sans identifiant des CdM et de votre vue (trõlls exclus)</span>
										</v-tooltip><br/>
										<!-- RESET PWD DIALOG -->
										<v-dialog v-model="pwd_dialog" max-width="50%">
											<v-btn slot="activator">Modifier mon mot de passe</v-btn>
											<v-form v-model="valid_pwd">
							      	<v-card>
							        	<v-card-title class="headline">Modifier mon mot de passe</v-card-title>
												<v-snackbar v-model="error_pwd" color="error" :timeout="6000" top>
      										{{ error_pwd_msg }}
      										<v-btn dark flat @click="error_pwd = false">Fermer</v-btn>
    										</v-snackbar>
												<v-layout column ma-5>
													<v-flex xs6>
														<v-text-field label="Ancien mot de passe" prepend-icon="fas fa-unlock" v-model="pwd" :append-icon="show_pwd ? 'visibility_off' : 'visibility'" :type="show_pwd ? 'text' : 'password'" @click:append="show_pwd = !show_pwd" :error="pwd !== '' && error_pwd" required></v-text-field>
														<br/>
														<v-text-field label="Nouveau mot de passe" prepend-icon="fas fa-lock" v-model="new_pwd" :append-icon="show_pwd ? 'visibility_off' : 'visibility'" :type="show_pwd ? 'text' : 'password'" @click:append="show_pwd = !show_pwd" :error="new_pwd !== '' && error_pwd" counter :rules="[pwdRule]" :success="pwdMatch(false)" required></v-text-field>
														<v-text-field label="Confirmation" prepend-icon="fas fa-lock" v-model="new_pwd2" :append-icon="show_pwd ? 'visibility_off' : 'visibility'" :type="show_pwd ? 'text' : 'password'" @click:append="show_pwd = !show_pwd" :error="new_pwd2 !== '' && error_pwd" counter :error-messages="pwdMatch(true)" :success="pwdMatch(false)" required></v-text-field>
													</v-flex>
												</v-layout>
							        	<v-card-actions>
							          	<v-spacer></v-spacer>
							          	<v-btn @click="pwd_dialog = false">Annuler</v-btn>
							          	<v-btn class="primary" @click="resetPwd()" :disabled="!valid_pwd || pwd === '' || new_pwd === '' || new_pwd2 === ''">Modifier</v-btn>
							        	</v-card-actions>
							      	</v-card>
											</v-form>
							    	</v-dialog>
									</v-flex>
								</v-layout>
        			</v-card-text>
        		</v-card>
      		</v-expansion-panel-content>
    		</v-expansion-panel>
				<!-- MH PREFS -->
     		<v-expansion-panel expand inset :value="[true]">
      		<v-expansion-panel-content hide-actions readonly>
        		<div slot="header" class="title">Mon profil MountyHall</div>
						<br/>
        		<v-card>
        			<v-card-text class="text-xs-center">
        				<v-layout align-center justify-center>
									<v-flex xs8>
									<v-text-field label="Mot de passe d'application" v-model="user.pwd_mh" hint="<a href='http://sp.mountyhall.com/hashing.php'>Qu'est ce que c'est ?</a><br/><br/><span class='orange--text text--lighten-1'>Mountyhall fixe des <a href='http://sp.mountyhall.com'>limites journalières</a> d'appel par trõll, veillez à ne pas les dépasser tous outils tiers confondus !</span>" persistent-hint></v-text-field><br/>
									<v-slider label="Limite d'appel aux scripts dynamiques" v-model="user.max_sp_dyn" :thumb-size="24" thumb-label="always" min="0" max="16" always-dirty hint="Maximum d'appels <b class='red--text'>automatiques</b> aux scripts publiques dynamiques par jour" persistent-hint></v-slider><br/><br/>
									<v-tooltip left>
										<v-progress-circular slot="activator" rotate="90" size="100" width="15" :value="user.count_sp_dyn/24*100" :color="user.count_sp_dyn <= user.max_sp_dyn ? 'green' : (user.count_sp_dyn <= 18 ? 'orange' : 'red')">{{ user.count_sp_dyn }}</v-progress-circular> 
										<span>Maximum 24</span>
									</v-tooltip> <span class="ml-4 body-1">appels aux scripts dynamiques ces dernières 24 heures</span><br/>
									<br/><br/>
									<v-tooltip top>
										<v-btn slot="activator" small color="warning" dark @click="mh_call('profil4')" :disabled="sp_call_disabled">Rafraichir mon profil</v-btn>
										<span>1 appel au script dynamique Profil4</span>
									</v-tooltip>
									<v-tooltip top>
										<v-btn slot="activator" small color="warning" dark @click="mh_call('vue2')" :disabled="sp_call_disabled">Rafraichir ma vue</v-btn>
										<span>1 appel au script dynamique Vue2</span>
									</v-tooltip>
									</v-flex>
								</v-layout>	
							</v-card-text>
							<!-- MH calls -->
							<v-card-actions v-if="max_pages > 0">
								<v-spacer></v-spacer>
								<v-btn icon @click="show_calls = !show_calls">
            			<v-icon>{{ show_calls ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
          			</v-btn>
								<v-spacer></v-spacer>
        			</v-card-actions>
							<v-slide-y-transition>
          			<v-card-text v-show="show_calls" class="text-xs-center">
									<v-data-table :headers="headers" :items="calls" class="elevation-1" hide-actions disable-initial-sort>
    								<template slot="items" slot-scope="props">
								      <td v-if="props.item.manual">Manuel</td>
								      <td v-else>Automatique</td>
								      <td>{{ props.item.nom }}</td>
								      <td>{{ props.item.type }}</td>
								      <td>{{ props.item.time | moment('utc', 'DD/MM/YYYY HH:mm:ss') }}</td>
											<td class="green--text" v-if="props.item.status == 0">Succès</td>
											<td class="red--text" v-else-if="props.item.status == 1">Paramètres incorrects</td>
											<td class="red--text" v-else-if="props.item.status == 2">Troll inexistant</td>
											<td class="red--text" v-else-if="props.item.status == 3">Mot de passe incorrect</td>
											<td class="red--text" v-else-if="props.item.status == 4">Entretien MH</td>
											<td class="red--text" v-else-if="props.item.status == 5">SP temporairement désactivés</td>
											<td class="red--text" v-else-if="props.item.status == 6">Troll désactivé</td>
											<td class="red--text" v-else>Erreur inconnue</td>
								    </template>
								  </v-data-table>
									<v-pagination class="mt-5" v-model="page" :length="max_pages" :total-visible="7" @input="getCalls" next-icon="fas fa-angle-right" prev-icon="fas fa-angle-left"></v-pagination>
          			</v-card-text>
        			</v-slide-y-transition>
        		</v-card>
      		</v-expansion-panel-content>
    		</v-expansion-panel>
			</v-form>
			</v-card>
			<!-- BOTTOM BUTTONS -->
			<v-btn class="info" @click="saveProfil()" @keyup.native.enter="saveProfil()" :disabled="!valid">Sauvegarder</v-btn>
			<v-dialog v-model="delete_dialog" max-width="50%">
				<v-btn slot="activator" class="error">Supprimer mon compte</v-btn>
      	<v-card>
        	<v-card-title class="headline">Supprimer votre compte SCIZ ?</v-card-title>
					<v-card-text>Cette action est définitive et irréversible.<br/>Les informations que vous avez déjà partagées avec d'autres utilisateurs leurs seront toujours accessibles.</v-card-text>
        	<v-card-actions>
          	<v-spacer></v-spacer>
          	<v-btn @click="delete_dialog = false">Annuler</v-btn>
          	<v-btn class="error" @click="deleteAccount()">Supprimer</v-btn>
        	</v-card-actions>
      	</v-card>
    	</v-dialog>
    </v-flex>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	import { EventBus } from '~/src/store.js'
	import { getProfil, deleteProfil, getMhCalls, resetPassword, doMHCall } from '~/src/api.js'
	
	export default {
    name: 'ProfilView',
		data: () => ({
			valid: true,
			delete_dialog: false,
			error: false,
			error_msg: '',
			success: false,
			success_msg: '',
			sp_call_disabled: false,
			info: false,
			info_msg: '',
			show_calls: false,
			mode: '',
			page: 1,
			max_pages: 1,
			headers: [
          { text: 'Origine', align: 'center', value: 'manual' },
          { text: 'Nom', align: 'center', value: 'nom' },
          { text: 'Type', align: 'center', value: 'type' },
          { text: 'Horodatage', align: 'center', value: 'time' },
          { text: 'Statut', align: 'center', value: 'status' }
        ],
			calls: [],
			user: {
				pseudo: '',
				sciz_mail: '',
				user_mail: '',
				session: 1,
				pwd_mh: '',
				max_sp_dyn: 1,
				community_sharing: true,
			},
			valid_pwd: true,
			error_pwd: false,
			error_pwd_msg: '',
			pwd_dialog: false,
			show_pwd: false,
			pwd: '',
			new_pwd: '',
			new_pwd2: '',
			pwdRule: v => v.length >= 8 || "Au moins 8 caractères",
			mailRule: v => /^$|(^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$)/.test(v) || 'Adresse mail invalide !'
		}),
		beforeMount () {
			getProfil()
				.then(res => {
					if (res.status === 200) {
						this.user.pseudo = res.data['pseudo'] || '';
						this.user.sciz_mail = res.data['sciz_mail'] || '';
						this.user.user_mail = res.data['user_mail'] || '';
						this.user.session = res.data['session'] || '';
						this.user.pwd_mh = res.data['pwd_mh'] || '';
						this.user.max_sp_dyn = res.data['max_sp_dyn'] || '';
						this.user.max_sp_sta = res.data['max_sp_sta'] || '';
						this.user.community_sharing = res.data['community_sharing'];
						this.user.count_sp_dyn = res.data['count_sp_dyn'] || '';
						this.user.count_sp_sta = res.data['count_sp_sta'] || '';
					}
				});
			this.getCalls();
		},
		methods: {
			mh_call (script) {
				this.sp_call_disabled = true;
				doMHCall(script)
					.then(res => { 
						this.success = true;
						this.success_msg = res.data.message;
						if (['profil4', 'vue2'].indexOf(script) > -1) {
							this.user.count_sp_dyn += 1;
						}
						this.getCalls();
						this.sp_call_disabled = false;
					})
					.catch(err => {
						this.error = true;
						if (err.response && err.response.data && err.response.data.message) {
							this.error_msg = err.response.data.message;
						} else {
							this.error_msg = 'Une erreur est survenue...';
						}
						this.sp_call_disabled = false;
					});
			},
			switchMode (mode) {
				this.$store.commit('setMode', mode);
			},
			saveProfil () {
				this.$store.dispatch('saveProfil', this.user)
					.then(() => {});
			},
			deleteAccount () {
				deleteProfil()
					.then(() => { 
						this.$store.commit('logout');
						this.$router.push('/');
					});
			},
			resetPwd () {
				resetPassword({ 'pwd': this.pwd, 'new_pwd': this.new_pwd, 'new_pwd2': this.new_pwd2 })
					.then(res => { 
						if (res.status === 200) {
							this.success = true;
							this.success_msg = res.data.message;
							this.pwd_dialog = false;
						}
					})
					.catch(err => {
						this.error_pwd = true;
						this.error_pwd_msg = 'Données invalides...';
					});
			},
			getCalls () {
				getMhCalls(this.page)
					.then(res => {
						if (res.status === 200) {
							this.max_pages = Math.ceil(res.data['total'] / 10) || 0;
							this.calls = res.data['calls'] || [];
						}	
					});
			},
			pwdMatch (error) {
				if (this.new_pwd === '' || this.new_pwd2 === '') {
					return error ? '' : false
				} else {
					return (this.new_pwd === this.new_pwd2) ? (error ? '' : true) : (error ? 'Le mot de passe ne correspond pas' : false)
				}
			}
		},
  	mounted () {
			this.mode = this.$store.getters.mode;
			EventBus.$on('savedProfil', msg => {this.success = true; this.success_msg = msg});
			EventBus.$on('failedSavingProfil', err => {this.error = true; this.error_msg = err});
	  },
	  beforeDestroy () {
	    EventBus.$off('savedProfil');
	    EventBus.$off('failedSavingProfil');
	  }
	}
</script>
