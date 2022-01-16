<!-- TEMPLATE -->
<template>
	<v-container justify="center" align="center" class="fill-height" id="profil-view" ma-5>
		<!-- NOTIFICATIONS -->
		<v-snackbar v-model="error" color="error" :timeout="6000" top>
			{{ error_msg }}
			<template v-slot:action="{ attrs }">
				<v-btn dark text @click="error = false" v-bind="attrs">Fermer</v-btn>
			</template>
		</v-snackbar>
		<v-snackbar v-model="success" color="success" :timeout="6000" top>
			{{ success_msg }}
			<template v-slot:action="{ attrs }">
				<v-btn dark text @click="success = false" v-bind="attrs">Fermer</v-btn>
			</template>
		</v-snackbar>
		<v-snackbar v-model="info" color="info" :timeout="6000" top>
			{{ info_msg }}
			<template v-slot:action="{ attrs }">
				<v-btn dark text @click="info = false" v-bind="attrs">Fermer</v-btn>
			</template>
		</v-snackbar>
		<!-- SIDEBAR -->
		<v-navigation-drawer app floating>
			<v-row align="center" justify="center" class="fill-height pl-15">
				<v-col align="center" justify="center">
					<v-img v-if="userData().blason_uri" :src="userData().blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="300px"></v-img>
					<v-img v-else :src="Image('unknown')" alt="" contain max-height="300px"></v-img>
					<br/><h3 class="text-capitalize subheading">{{userData().nom}}</h3>
					<h5 class="text-capitalize caption">({{userData().id}})</h5>
				</v-col>
			</v-row>
		</v-navigation-drawer>
		<!-- MAIN -->
		<v-row align="center" justify="center" class="fill-height">
			<v-col class="col-9">
				<v-form v-model="valid">
					<v-expansion-panels multiple :value="[0,1]">
						<!-- SCIZ PREFS -->
						<v-expansion-panel>
							<v-expansion-panel-header class="title">Profil SCIZ</v-expansion-panel-header>
							<v-expansion-panel-content>
								<v-row align="center" justify="center" class="fill-height">
									<v-col class="col-8 text-center">
										<span class=>Votre adresse SCIZ</span><br/></br>
										<v-tooltip bottom>
											<template v-slot:activator="{ on, attrs }">
												<v-chip v-clipboard:copy="user.sciz_mail" @click="info_msg = 'Adresse copiée dans le presse-papier'; info = true;" v-bind="attrs" v-on="on">
													<v-avatar><v-img :src="Image('logo')" contain></v-img></v-avatar>
													{{user.sciz_mail}}
												</v-chip>
											</template>
											<span>Cliquer pour copier</span>
										</v-tooltip>
										<br/><br/>
										<v-text-field label="Courriel" v-model="user.user_mail" always-dirty hint="Votre courriel est uniquement utilisé pour vous retourner vos codes de transfert et contrôler l'expéditeur des notifications envoyées à votre boite aux lettres SCIZ" :rules="[mailRule]"></v-text-field><br/><br/>
										<v-tooltip top>
											<template v-slot:activator="{ on, attrs }">
												<v-slider label="Durée de session" v-model="user.session" :thumb-size="24" thumb-label="always" min="1" max="24" always-dirty hint="Durée maximum en heures avant déconnexion de votre session SCIZ" persistent-hint v-bind="attrs" v-on="on"></v-slider>
											</template>
											<span>Reconnexion nécessaire avant application de la modification</span>
										</v-tooltip><br/>
										<v-switch label="Utiliser le mode sombre" v-model="mode" :input-value="mode" true-value="dark" false-value="light" @change="switchMode(mode)"></v-switch><br/>
										<br/>
									</v-col>
								</v-row>
							</v-expansion-panel-content>
						</v-expansion-panel>
						<!-- MH PREFS -->
						<v-expansion-panel>
							<v-expansion-panel-header class="title">Profil MountyHall</v-expansion-panel-header>
							<v-expansion-panel-content>
								<v-row align="center" justify="center">
									<v-col class="col-8 text-center">
										<v-text-field label="Mot de passe d'application" v-model="user.pwd_mh" hint="<a href='http://sp.mountyhall.com/hashing.php'>Qu'est ce que c'est ?</a><br/><br/><span class='orange--text text--lighten-1'>Mountyhall fixe des <a href='http://sp.mountyhall.com'>limites journalières</a> d'appel par trõll, veillez à ne pas les dépasser tous outils tiers confondus !</span>" persistent-hint>
											<template v-slot:message='{ message }'><span v-html="message"></span></template>
										</v-text-field><br/><br/>
										<v-slider label="Limite d'appel aux scripts dynamiques" v-model="user.max_sp_dyn" :thumb-size="24" thumb-label="always" min="0" max="16" always-dirty hint="Maximum d'appels <b class='red--text'>automatiques</b> aux scripts publiques dynamiques par jour" persistent-hint>
											<template v-slot:message='{ message }'><span v-html="message"></span></template>
										</v-slider><br/><br/>
										<v-tooltip left>
											<template v-slot:activator="{ on, attrs }">
												<v-progress-circular rotate="90" size="100" width="15" :value="user.count_sp_dyn/24*100" :color="user.count_sp_dyn <= user.max_sp_dyn ? 'green' : (user.count_sp_dyn <= 18 ? 'orange' : 'red')" v-bind="attrs" v-on="on">{{ user.count_sp_dyn }}</v-progress-circular> 
											</template>
											<span>Maximum 24</span>
										</v-tooltip> <span class="ml-4 body-1">appels aux scripts dynamiques ces dernières 24 heures</span><br/>
										<br/><br/>
										<v-tooltip top>
											<template v-slot:activator="{ on, attrs }">
												<v-btn small color="warning" dark @click="mh_call('profil4')" :disabled="sp_call_disabled" v-bind="attrs" v-on="on">Rafraichir mon profil</v-btn>
											</template>
											<span>1 appel au script dynamique Profil4</span>
										</v-tooltip>
										<v-tooltip top>
											<template v-slot:activator="{ on, attrs }">
												<v-btn small color="warning" dark @click="mh_call('vue2')" :disabled="sp_call_disabled" v-bind="attrs" v-on="on">Rafraichir ma vue</v-btn>
											</template>
											<span>1 appel au script dynamique Vue2</span>
										</v-tooltip>
									</v-col>
								</v-row>	
								<!-- MH CALLS -->
								<v-row align="center" justify="center" v-if="max_pages > 0">
									<v-col>
										<v-card-text class="text-center">
											<v-spacer></v-spacer>
											<v-btn icon @click="show_calls = !show_calls">
												<v-icon size="16px">fas {{ show_desc ? 'fa-chevron-up' : 'fa-chevron-down' }}</v-icon>
											</v-btn>
											<v-spacer></v-spacer>
											<v-slide-y-transition>
												<v-data-table v-show="show_calls" :headers="headers" :items="calls" class="elevation-1" hide-default-footer sort-by="">
													<template v-slot:item.manual="{ item }">
														<td class="text-center" v-if="item.manual === true">Manuel</td>
														<td class="text-center" v-else>Automatique</td>				
													</template>
													<template v-slot:item.time="{ item }">
														<td class="text-center" >{{ item.time | moment('utc', 'DD/MM/YYYY HH:mm:ss') }}</td>
													</template>
													<template v-slot:item.status="{ item }">
														<td class="text-center green--text" v-if="item.status === 0">Succès</td>
														<td class="text-center red--text" v-else-if="item.status === 1">Paramètres incorrects</td>
														<td class="text-center red--text" v-else-if="item.status === 2">Troll inexistant</td>
														<td class="text-center red--text" v-else-if="item.status === 3">Mot de passe incorrect</td>
														<td class="text-center red--text" v-else-if="item.status === 4">Entretien MH</td>
														<td class="text-center red--text" v-else-if="item.status === 5">SP temporairement désactivés</td>
														<td class="text-center red--text" v-else-if="item.status === 6">Troll désactivé</td>
														<td class="text-center red--text" v-else>Erreur inconnue</td>
													</template>
												</v-data-table>
												<v-pagination class="mt-5" v-model="page" :length="max_pages" :total-visible="7" @input="getCalls" next-icon="fas fa-angle-right" prev-icon="fas fa-angle-left"></v-pagination>
											</v-slide-y-transition>
										</v-card-text>
									</v-col>
								</v-row>
							</v-expansion-panel-content>
						</v-expansion-panel>
					</v-expansion-panels>
				</v-form>
				<!-- BOTTOM BUTTONS -->
				<v-row align="center" justify="center" class="ma-5">
					<v-col align="center" justify="center">
						<v-btn class="info" @click="saveProfil()" @keyup.native.enter="saveProfil()" :disabled="!valid">Sauvegarder</v-btn>
						<v-dialog v-model="delete_dialog" max-width="50%">
							<template v-slot:activator="{ on, attrs }">
								<v-btn v-bind="attrs" v-on="on" class="error">Supprimer mon compte</v-btn>
							</template>
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
					</v-col>
				</v-row>
			</v-col>
		</v-row>
	</v-container>
</template>

<!-- SCRIPT -->
<script>
import { EventBus } from '~/src/store.js'
import { getProfil, deleteProfil, getMhCalls, doMHCall } from '~/src/api.js'

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
			sciz_mail: '',
			user_mail: '',
			session: 1,
			pwd_mh: '',
			max_sp_dyn: 1,
		},
		mailRule: v => /^$|(^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$)/.test(v) || 'Adresse mail invalide !'
	}),
	beforeMount () {
		getProfil()
			.then(res => {
				if (res.status === 200) {
					this.user.sciz_mail = res.data['sciz_mail'] || '';
					this.user.user_mail = res.data['user_mail'] || '';
					this.user.session = res.data['session'] || '';
					this.user.pwd_mh = res.data['pwd_mh'] || '';
					this.user.max_sp_dyn = res.data['max_sp_dyn'] || '';
					this.user.max_sp_sta = res.data['max_sp_sta'] || '';
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
			this.$vuetify.theme.dark = mode === 'dark';
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
		getCalls () {
			getMhCalls(this.page)
				.then(res => {
					if (res.status === 200) {
						this.max_pages = Math.ceil(res.data['total'] / 10) || 0;
						this.calls = res.data['calls'] || [];
					}	
				});
		},
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
