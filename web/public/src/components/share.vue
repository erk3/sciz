<!-- TEMPLATE -->
<template>
	<v-container justify="center" align="center" class="fill-height pa-0 ma-0" id="share-view">
		<!-- NOTIFICATIONS -->
		<v-snackbar v-model="error_group" color="error" :timeout="6000" top>
			{{ error_group }}
			<template v-slot:action="{ attrs }">
				<v-btn dark text @click="success = false" v-bind="attrs">Fermer</v-btn>
			</template>
		</v-snackbar>
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
		<v-navigation-drawer app clipped fixed permanent>
			<v-app-bar flat class="pa-0 ma-0">
				<v-row align="center" justify="start" class="fill-height" no-gutters>
					<v-col class="col-10"> Mes coteries </v-col>
					<!-- CREATE COTERIE DIALOG -->
					<v-col class="col-2">
						<v-dialog v-model="group_dialog" max-width="50%">
							<template v-slot:activator="{ on, attrs }">
								<v-btn v-bind="attrs" v-on="on" small fab right class="primary"><v-icon size="16px">fas fa-plus</v-icon></v-btn>
							</template>
							<v-card class="pa-5">
								<v-card-title class="headline">Créer une nouvelle coterie</v-card-title>
								<v-row wrap align="center" justify="center" class="fill-height">
									<v-col class="col-5">
										<v-img v-if="coterie_nouvelle.blason_uri" :src="coterie_nouvelle.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="200px"></v-img>
										<v-img v-else :src="Image('unknown')" alt="" contain max-height="200px"></v-img>
									</v-col>
									<v-col class="col-7">
										<v-card-title primary-title>
											<v-row wrap align="center" justify="center" class="fill-height">
												<v-col>
													<v-text-field label="Nom de la coterie" v-model="coterie_nouvelle.nom"></v-text-field>
													<v-text-field label="URI du blason" v-model="coterie_nouvelle.blason_uri"></v-text-field>
													<v-text-field label="Description" v-model="coterie_nouvelle.desc"></v-text-field>
												</v-col>
											</v-row>
										</v-card-title>
									</v-col>
								</v-row>
								<v-card-actions>
									<v-spacer></v-spacer>
									<v-btn @click="group_dialog = false">Annuler</v-btn>
									<v-btn class="primary" @click="createCoterie()" :disabled="!coterie_nouvelle.nom">Créer</v-btn>
								</v-card-actions>
							</v-card>
						</v-dialog>
					</v-col>
				</v-row>
			</v-app-bar>
			<!-- GROUPS LIST -->
			<v-divider></v-divider>
			<v-subheader>Coterie personnelle</v-subheader>
			<v-list>
				<template v-for="(coterie, index) in [coterie_perso]">
					<v-list-item :key="index" @click="switchCoterie(coterie); refreshPartages()" v-model="coterie_courante.id === coterie.id">
						<v-list-item-avatar>
							<v-img v-if="coterie.blason_uri" :src="coterie.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						</v-list-item-avatar>
						<v-list-item-content>{{ coterie.nom }}</v-list-item-content>
					</v-list-item>
				</template>
			</v-list>
			<v-divider v-if="invitations.length > 0"></v-divider>
			<v-subheader v-if="invitations.length > 0">Invitation(s)</v-subheader>
			<v-list>
				<template v-for="(coterie, index) in invitations">
					<v-list-item :key="index" @click="switchCoterie(coterie); refreshPartages()" v-model="coterie_courante.id === coterie.id">
						<v-list-item-avatar>
							<v-img v-if="coterie.blason_uri" :src="coterie.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						</v-list-item-avatar>
						<v-list-item-content>{{ coterie.nom }}</v-list-item-content>
					</v-list-item>
				</template>
			</v-list>
			<v-divider v-if="coteries.length > 0"></v-divider>
			<v-subheader v-if="coteries.length > 0">Coterie(s) de groupe</v-subheader>
			<v-list>
				<template v-for="(coterie, index) in coteries">
					<v-list-item :key="index" @click="switchCoterie(coterie); refreshPartages()" v-model="coterie_courante.id === coterie.id">
						<v-list-item-avatar>
							<v-img v-if="coterie.blason_uri" :src="coterie.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						</v-list-item-avatar>
						<v-list-item-content>{{ coterie.nom }}</v-list-item-content>
					</v-list-item>
				</template>
			</v-list>
		</v-navigation-drawer>
		<!-- COTERIE -->
		<v-row wrap align="center" justify="center" class="fill-height">
			<v-col class="col-8 text-center">
				<v-card class="pa-5 ma-5">
					<!-- DESCRIPTION -->
					<v-row wrap align="center" justify="center" class="fill-height">
						<v-col class="col-5">
							<v-img v-if="coterie_courante.blason_uri" :src="coterie_courante.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="200px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="200px"></v-img>
						</v-col>
						<v-col class="col-7">
							<v-text-field label="Nom de la coterie" v-model="coterie_courante.nom" :disabled="!partage_courant.admin"></v-text-field>
							<v-text-field label="URI du blason" v-model="coterie_courante.blason_uri" :disabled="!partage_courant.admin"></v-text-field>
							<v-text-field label="Description" v-model="coterie_courante.desc" :disabled="!partage_courant.admin"></v-text-field>
						</v-col>
					</v-row>
					<!-- USER SHARE STATE -->
					<v-divider v-if="loaded && coterie_courante.grouped" class="mb-5 mt-5"></v-divider>
					<v-row wrap align="center" justify="center" class="fill-height" v-if="loaded && coterie_courante.grouped">
						<v-col class="col-12" v-if="!partage_courant.pending">Vous partagez</v-col>
						<v-col class="col-12" v-else>Vous avez été invité dans cette coterie, si vous acceptez vous partagerez :</v-col>
						<v-col class="col-4"><v-spacer></v-spacer><v-switch label="Vos événements" class="centered-switch" v-model="partage_courant.sharingEvents"></v-switch></v-col>
						<v-col class="col-4"><v-spacer></v-spacer><v-switch label="Votre profil" class="centered-switch" v-model="partage_courant.sharingProfile"></v-switch></v-col>
						<v-col class="col-4"><v-spacer></v-spacer><v-switch label="Votre vue" class="centered-switch" v-model="partage_courant.sharingView"></v-switch></v-col>
						<!-- COTERIE SHARES STATE -->
						<v-col class="col-12">
							<v-card flat tile>
								<v-card-actions>
									<v-spacer></v-spacer>
									<v-tooltip top>
										<template v-slot:activator="{ on, attrs }">
											<v-btn icon @click="show_shares = !show_shares" v-bind="attrs" v-on="on">
												<v-icon size="16px">{{ show_shares ? 'fas fa-chevron-down' : 'fas fa-chevron-up' }}</v-icon>
											</v-btn>
										</template>
										<span>Partages de la coterie</span>
									</v-tooltip>
									<v-spacer></v-spacer>
								</v-card-actions>
								<v-slide-y-transition>
									<v-card-text v-show="show_shares" class="text-center">
										<v-data-table :headers="headers" :items="partages.admins.concat(partages.users)" class="elevation-1" hide-default-footer :items-per-page="-1">
											<template v-slot:item.nom="{ item }">
												{{ item.nom }} ({{item.partage.user_id}})
											</template>
											<template v-slot:item.partage.sharingEvents="{ item }">
												<v-icon size="16px" :color="item.partage.sharingEvents ? 'green' : 'red'">{{ item.partage.sharingEvents ? 'fas fa-check-circle' : 'fas fa-times-circle'}}</v-icon>
											</template>
											<template v-slot:item.partage.sharingProfile="{ item }">
												<v-icon size="16px" :color="item.partage.sharingProfile ? 'green' : 'red'">{{ item.partage.sharingProfile ? 'fas fa-check-circle' : 'fas fa-times-circle'}}</v-icon>
											</template>
											<template v-slot:item.partage.sharingView="{ item }">
												<v-icon size="16px" :color="item.partage.sharingView ? 'green' : 'red'">{{ item.partage.sharingView ? 'fas fa-check-circle' : 'fas fa-times-circle'}}</v-icon>
											</template>
											<template v-slot:item.partage.hookPropagation="{ item }">
												<v-switch class="centered-switch" :disabled="item.partage.user_id !== userData().id && !partage_courant.admin " v-model="item.partage.hookPropagation"></v-switch>
											</template>
										</v-data-table>
									</v-card-text>
								</v-slide-y-transition>
							</v-card>
						</v-col>
					</v-row>
					<!-- HOOKS -->
					<v-divider v-if="loaded && coterie_courante.hooks && !partage_courant.pending" class="mb-5 mt-5"></v-divider>
					<v-row v-if="loaded && coterie_courante.hooks && !partage_courant.pending" wrap align="center" justify="center" class="fill-height">
						<v-col class="col-11">
							<span>Hooks</span>
							<v-row wrap align="center" justify="center" class="fill-height mt-5">
								<v-menu v-for="(hook, index) in coterie_courante.hooks" :key="index" offset-y>
									<template v-slot:activator="{ on, attrs }">
										<v-chip v-bind="attrs" v-on="on" class="ma-3">
											<v-avatar><v-img :src="Image('logo-' + hook.type.toLowerCase())" contain></v-img></v-avatar>
											{{ hook.type }}
										</v-chip>
									</template>
									<v-list>
										<v-list-item v-if="hook.type === 'Discord'" :href="'https://discordapp.com/oauth2/authorize?client_id=531898253210550281&scope=bot&permissions=2048'">Inviter le bot sur mon serveur</v-list-item>
										<v-list-item v-if="hook.type === 'Hangouts'" @click="info_msg = 'Adresse copiée dans le presse-papier'; info = true;" v-clipboard:copy="'botsciz@gmail.com'">Copier l'adresse du bot à inviter</v-list-item>
										<v-list-item v-if="hook.type === 'Miaou' && hook.jwt" @click="info_msg = 'Commande copiée dans le presse-papier'; info = true;" v-clipboard:copy="'!!sciz register ' + hook.jwt">Copier la commande d'enregistrement</v-list-item>
										<v-list-item v-if="hook.type === 'Discord' && hook.jwt" @click="info_msg = 'Commande copiée dans le presse-papier'; info = true;" v-clipboard:copy="'!sciz register ' + hook.jwt">Copier la commande d'enregistrement</v-list-item>
										<v-list-item v-if="hook.type === 'Hangouts' && hook.jwt" @click="info_msg = 'Commande copiée dans le presse-papier'; info = true;" v-clipboard:copy="'/sciz register '+ hook.jwt">Copier la commande d'enregistrement</v-list-item>
										<v-list-item v-if="hook.type === 'Mountyzilla' && hook.jwt" @click="info_msg = 'Commande copiée dans le presse-papier'; info = true;" v-clipboard:copy="hook.jwt">Copier le JWT</v-list-item>
										<v-list-item v-if="hook.jwt && partage_courant.admin" @click="selectedHook = hook; hook_dialog = true;">Configurer</v-list-item>
										<v-list-item v-if="hook.jwt && partage_courant.admin" @click="regenerateHook(hook.id)"><span class="red--text text-darken1">Régénérer</span></v-list-item>
										<v-list-item v-if="!hook.jwt" @click="regenerateHook(hook.id)"><span class="red--text text-darken1">Générer</span></v-list-item>
									</v-list>
								</v-menu>
							</v-row>
						</v-col>
					</v-row>
					<!-- SHARES -->
					<v-divider v-if="loaded && coterie_courante.grouped && !partage_courant.pending" class="mb-5 mt-5"></v-divider>
					<v-row v-if="loaded && coterie_courante.grouped && !partage_courant.pending" wrap align="center" justify="center" class="fill-height">
						<v-col class="col-11">
							<span>Administrateur(s)</span>
							<v-row wrap align="center" justify="center" class="fill-height mt-3">
								<v-list v-for="(item, index) in partages.admins" :key="index">
									<v-menu offset-y :disabled="partages.admins.length <= 1 || !partage_courant.admin">
										<template v-slot:activator="{ on, attrs }">
											<v-chip v-bind="attrs" v-on="on" class="red--text ma-3">	
												<v-avatar>
													<v-img :src="item.blason_uri" v-if="item.blason_uri" @error="item.blason_uri=Image('unknown')" alt="" contain></v-img>
													<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
												</v-avatar>
												{{ item.nom }}
											</v-chip>
										</template>
										<v-list v-if="partages.admins.length > 1 && partage_courant.admin">
											<v-list-item @click="retrograde(item)"> Rétrograder simple utilisateur </v-list-item>
											<v-list-item @click="exclude(item)"> Exclure de la coterie </v-list-item>
										</v-list>
									</v-menu>
								</v-list>
							</v-row>
						</v-col>
						<v-col class="col-11" v-if="partages.users.length > 0">
							<span>Utilisateur(s)</span>
							<v-row wrap align="center" justify="center" class="fill-height mt-3">
								<v-list v-for="(item, index) in partages.users" :key="index">
									<v-menu offset-y :disabled="!partage_courant.admin && item.partage.user_id !== userData().id">
										<template v-slot:activator="{ on, attrs }">
											<v-chip v-bind="attrs" v-on="on" class="blue--text ma-3">	
												<v-avatar>
													<v-img :src="item.blason_uri" v-if="item.blason_uri" @error="item.blason_uri=Image('unknown')" alt="" contain></v-img>
													<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
												</v-avatar>
												{{ item.nom }}
											</v-chip>
										</template>
										<v-list v-if="partage_courant.admin || item.partage.user_id === userData().id">
											<v-list-item v-if="partage_courant.admin" @click="upgrade(item)"> Promouvoir administrateur </v-list-item>
											<v-list-item v-if="partage_courant.admin" @click="exclude(item)"> Exclure de la coterie </v-list-item>
											<v-list-item v-else @click="deleteOwnShare(item)"> Quitter la coterie </v-list-item>
										</v-list>
									</v-menu>
								</v-list>
							</v-row>
						</v-col>
						<v-col class="col-11">
							<span>Invitation(s)</span>
							<v-row wrap align="center" justify="center" class="fill-height mt-3">
								<v-autocomplete :disabled="!partage_courant.admin" v-model="pending" :items="usersList" item-text="nom" item-value="id" multiple chips hide-no-data hide-selected cache-items :menu-props="{'closeOnContentClick': true}" no-data-text="Aucun trõll à inviter" :filter="trollFilter">
									<template slot="selection" slot-scope="data">
										<v-chip close close-icon="far fa-times-circle" @click:close="removePending(data.item)">
											<v-avatar>
												<v-img :src="data.item.blason_uri" v-if="data.item.blason_uri" @error="data.item.blason_uri=Image('unknown')" alt="" contain></v-img>
												<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
											</v-avatar>
											{{ data.item.nom }}
										</v-chip>
									</template>
									<template slot="item" slot-scope="data">
										<v-list-tile-avatar>
											<v-img :src="data.item.blason_uri" v-if="data.item.blason_uri" @error="data.item.blason_uri=Image('unknown')" alt="" contain max-width="30px"></v-img>
											<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
										</v-list-tile-avatar>
										<v-list-tile-content>
											<v-list-tile-title> {{ data.item.nom }} ({{ data.item.id }}) </v-list-tile-title>
										</v-list-tile-content>
									</template>
								</v-autocomplete>
							</v-row>
						</v-col>
					</v-row>
				</v-card>
				<!-- BOTTOM BUTTONS -->
				<v-row align="center" justify="center" class="ma-5">
					<v-col align="center" justify="center">
						<v-btn v-if="!partage_courant.pending" class="info" @click="saveCoterie()" @keyup.native.enter="saveCoterie()">Sauvegarder</v-btn>
						<v-dialog v-if="coterie_courante.grouped && partage_courant.admin" v-model="delete_dialog" max-width="50%">
							<template v-slot:activator="{ on, attrs }">
								<v-btn v-bind="attrs" v-on="on" class="error">Supprimer la coterie</v-btn>
							</template>
							<v-card>
								<v-card-title class="headline">Supprimer cette coterie ?</v-card-title>
								<v-card-text>Cette action est définitive et irréversible.<br/>Les informations déjà partagées avec d'autres utilisateurs leurs seront toujours accessibles.</v-card-text>
								<v-card-actions>
									<v-spacer></v-spacer>
									<v-btn @click="delete_dialog = false">Annuler</v-btn>
									<v-btn class="error" @click="deleteCoterie()">Supprimer</v-btn>
								</v-card-actions>
							</v-card>
						</v-dialog>
						<v-btn v-if="partage_courant.pending" class="info" @click="acceptInvitation()">Accepter l'invitation</v-btn>
						<v-btn v-if="partage_courant.pending" class="error" @click="declineInvitation()">Décliner l'invitation</v-btn>
					</v-col>
				</v-row>
			</v-col>
		</v-row>
		<!-- HOOK DIALOG -->
		<v-dialog v-if="selectedHook" v-model="hook_dialog">
			<Format :h="selectedHook" :c="coterie_courante"></Format>
		</v-dialog>
	</v-container>
</template>

<!-- SCRIPT -->
<script>
import { renewHook, deleteGroup, deleteShare, acceptInvite, declineInvite, createGroup, getUsersList, setGroup, getPartages, getGroups } from '~/src/api.js';
import Format from '~/src/components/format.vue';

export default {
	name: 'ShareView',
	components: { Format },
	data() {
		return {
			loaded: false,
			error: false,
			success: false,
			info: false,
			error_msg: '',
			success_msg: '',
			info_msg: '',
			hook_dialog: false,
			selectedHook: null,
			group_dialog: false,
			delete_dialog: false,
			valid_group: false,
			error_group: false,
			error_group_msg: '',
			partages: {admins: [], users: [], pending: [], toExpire: []},
			pending: [], // Because v-autocomplete can't take a complex object as an input right now
			usersList: [],
			coterie_perso: {},
			coterie_nouvelle: {nom: null, blason_uri: null, desc: null},
			coterie_courante: {},
			partage_courant: {},
			coteries: [],
			invitations: [],
			show_shares: false,
			headers: [
				{ text: 'Nom', align: 'center', value: 'nom' },
				{ text: 'Evénéments', align: 'center', value: 'partage.sharingEvents' },
				{ text: 'Profil', align: 'center', value: 'partage.sharingProfile' },
				{ text: 'Vue', align: 'center', value: 'partage.sharingView' },
				{ text: 'Propagation', align: 'center', value: 'partage.hookPropagation' }
			],
		}
	},
	beforeMount() {
		this.refreshGroups();
	},
	methods: {
		switchCoterie(coterie) {
			this.coterie_courante = coterie;
			this.$store.commit('setCoterieID', coterie.id);
			this.$store.commit('setCoterieName', coterie.nom);
		},
		trollFilter (item, queryText, itemText) {
			const textOne = item.nom.toLowerCase();
			const textTwo = item.id.toString().toLowerCase();
			const searchText = queryText.toLowerCase();
			return textOne.indexOf(searchText) > -1 || textTwo.indexOf(searchText) > -1;
		},
		refreshGroups() {
			var coterie_courante = this.coterie_courante;
			getGroups(false, true, true)
				.then(res => {
					if (res.status === 200) {
						this.coterie_perso = res.data['coterie_perso'];
						this.coteries = res.data['coteries'];
						this.invitations = res.data['invitations'];
						this.coterie_courante = this.coterie_perso;
						// Try to set the current coterie to the last one stored in local storage
						var lastCoterieID = this.$store.getters.coterieID;
						this.coteries.forEach(coterie => {
							if (coterie.id === lastCoterieID) {
								this.coterie_courante = coterie;
							}
						}); 
						this.refreshPartages();
					}
				});
		},
		refreshPartages() {
			this.loaded = false;
			this.pending = [];
			getPartages(this.coterie_courante.id)
				.then(res => {
					if (res.status === 200) {
						this.partages = res.data;
						this.partages.toExpire = [];
						this.partages.pending.forEach((item) => {
							this.pending.push(item.partage.user_id);
						});
						this.partages.admins.concat(this.partages.users).concat(this.partages.pending).forEach(item => {
							if (item.partage.user_id === this.userData().id) {
								this.partage_courant = item.partage;
							}
						});
						this.loaded = true;
					}
				});
			getUsersList(this.coterie_courante.id)
				.then(res => {
					if (res.status === 200) {
						this.usersList = res.data;
					}
				});
		},
		createCoterie() {
			this.group_dialog = false;
			createGroup(this.coterie_nouvelle)
				.then(res => {
					this.refreshGroups();
				});
		},
		acceptInvitation() {
			acceptInvite(this.coterie_courante.id, this.partage_courant)
				.then(res => {
					this.refreshGroups();
				});
		},
		declineInvitation() {
			declineInvite(this.coterie_courante.id)
				.then(res => {
					this.refreshGroups();
				});
		},
		deleteCoterie() {
			deleteGroup(this.coterie_courante.id)
				.then(res => {
					this.refreshGroups();
					this.delete_dialog = false;
				});
		},
		deleteOwnShare() {
			deleteShare(this.coterie_courante.id)
				.then(res => {
					this.refreshGroups();
				})
				.catch(err => {
					this.error = true;
					this.error_msg = err.message;
				});
		},
		saveCoterie() {
			this.partages.pendingToAdd = this.pending;
			this.coterie_courante.partages = this.partages;
			setGroup(this.coterie_courante.id, this.coterie_courante)
				.then(res => {
					this.success = true;
					this.success_msg = res.data.message;
					this.refreshPartages();
				})
				.catch(err => {
					this.error = true;
					this.error_msg = err.message;
				});
		},
		removePending(item) {
			this.pending = this._.reject(this.pending, function(i) { return i === item.id; });
			this.partages.toExpire.push(item.id)
		},
		exclude(item) {
			if (item.partage.admin && this.partages.admins.length > 1) {
				this.partages.admins = this._.reject(this.partages.admins, function(i) { return i.partage.user_id === item.partage.user_id; });
			} else {
				this.partages.users = this._.reject(this.partages.users, function(i) { return i.partage.user_id === item.partage.user_id; });
			}
			this.partages.toExpire.push(item.partage.user_id);
		},
		upgrade(item) {
			item.partage.admin = true;
			this.partages.users = this._.reject(this.partages.users, function(i) { return i.partage.user_id === item.partage.user_id; });
			this.partages.admins.push(item);
		},
		retrograde(item) {
			if (item.partage.admin && this.partages.admins.length > 1) {
				item.partage.admin = false;
				this.partages.admins = this._.reject(this.partages.admins, function(i) { return i.partage.user_id === item.partage.user_id; });
				this.partages.users.push(item);
			}
		},
		regenerateHook(hook_id) {
			renewHook(hook_id)
				.then(res => {
					this.refreshGroups();
				});
		}
	}
}
</script>

<!-- STYLE -->
<style>
/* For v-switch centering */
.centered-switch > .v-input__control > .v-input__slot > .v-label {
	flex-grow: 0 !important;
	flex-shrink: 1 !important;
}
.centered-switch > .v-input__control > .v-input__slot {
	justify-content: center !important;
}
</style>
