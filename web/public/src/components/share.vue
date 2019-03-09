<!-- TEMPLATE -->
<template>
	<v-layout app row>
		<!-- DRAWER -->
		<v-navigation-drawer permanent app clipped value="true">
			<v-toolbar flat pa-0 ma-0>
				<v-layout row wrap align-center justify-center fill-height>
					<v-flex xs11> Mes coteries </v-flex>
					<v-flex xs1>
          	<!-- CREATE GROUP DIALOG -->
						<v-dialog v-model="group_dialog" max-width="50%">
							<v-btn slot="activator" small fab right class="primary"><v-icon size="16px">fas fa-plus</v-icon></v-btn>
							<v-card>
								<v-card-title class="headline">Créer une nouvelle coterie</v-card-title>
								<v-snackbar v-model="error_group" color="error" :timeout="6000" top>
					      	{{ error_group }}
					      	<v-btn dark flat @click="success = false">Fermer</v-btn>
					    	</v-snackbar>
								<v-layout row wrap align-center justify-center fill-height>
									<v-flex xs5>
										<v-img v-if="coterie_nouvelle.blason_uri" :src="coterie_nouvelle.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="200px"></v-img>
										<v-img v-else :src="Image('unknown')" alt="" contain max-height="200px"></v-img>
									</v-flex>
									<v-flex xs7>
										<v-card-title primary-title>
											<v-layout column wrap align-center justify-center fill-height>
												<v-text-field label="Nom de la coterie" v-model="coterie_nouvelle.nom"></v-text-field>
												<v-text-field label="URI du blason" v-model="coterie_nouvelle.blason_uri"></v-text-field>
												<v-text-field label="Description" v-model="coterie_nouvelle.desc"></v-text-field>
											</v-layout>
										</v-card-title>
									</v-flex>
								</v-layout>
								<v-card-actions>
									<v-spacer></v-spacer>
									<v-btn @click="group_dialog = false">Annuler</v-btn>
									<v-btn class="primary" @click="createCoterie()" :disabled="!coterie_nouvelle.nom">Créer</v-btn>
								</v-card-actions>
							</v-card>
						</v-dialog>
        	</v-flex>
				</v-layout>
			</v-toolbar>
      <!-- GROUPS LIST -->
    	<v-divider></v-divider>
			<v-subheader>Coterie personnelle</v-subheader>
      <v-list v-for="(coterie, index) in [coterie_perso]">
				<v-list-tile :key="index" @click="switchCoterie(coterie); refreshPartages();" v-model="coterie_courante.id === coterie.id">
					<v-layout row wrap align-center justify-start fill-height>
						<v-img v-if="coterie.blason_uri" :src="coterie.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						<v-flex xs10 ml-1>{{ coterie.nom }}</v-flex>
					</v-layout>
				</v-list-tile>
      </v-list>
      <v-divider></v-divider>
			<v-subheader v-if="invitations.length > 0">Invitation(s)</v-subheader>
			<v-list v-for="(coterie, index) in invitations">
				<v-list-tile :key="index" @click="switchCoterie(coterie); refreshPartages()" v-model="coterie_courante.id === coterie.id">
					<v-layout row wrap align-center justify-start fill-height>
						<v-img v-if="coterie.blason_uri" :src="coterie.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						<v-flex xs10 ml-1>{{ coterie.nom }}</v-flex>
					</v-layout>
				</v-list-tile>
      </v-list>
			<v-divider></v-divider>
			<v-subheader v-if="coteries.length > 0">Coterie(s) de groupe</v-subheader>
			<v-list v-for="(coterie, index) in coteries">
				<v-list-tile :key="index" @click="switchCoterie(coterie); refreshPartages();" v-model="coterie_courante.id === coterie.id">
					<v-layout row wrap align-center justify-start fill-height>
						<v-img v-if="coterie.blason_uri" :src="coterie.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						<v-flex xs10 ml-1>{{ coterie.nom }}</v-flex>
					</v-layout>
				</v-list-tile>
      </v-list>
    </v-navigation-drawer>
		<!-- COTERIE -->
		<v-layout row wrap align-start justify-center fill-height ma-5>
			<v-flex xs8 text-xs-center>
				<v-snackbar v-model="error" color="error" :timeout="6000" top>
      		{{ error_msg }}
	      	<v-btn dark flat @click="error = false">Fermer</v-btn>
	    	</v-snackbar>
				<v-snackbar v-model="success" color="success" :timeout="6000" top>
	      	{{ success_msg }}
	      	<v-btn dark flat @click="success = false">Fermer</v-btn>
	    	</v-snackbar>
        <v-card class="pa-3 ma-3">
          <v-layout row wrap align-center justify-center fill-height>
            <v-flex xs5>
							<v-img v-if="coterie_courante.blason_uri" :src="coterie_courante.blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="200px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="200px"></v-img>
            </v-flex>
            <v-flex xs7>
            	<v-card-title primary-title>
								<v-layout column wrap align-center justify-center fill-height>
									<v-text-field label="Nom de la coterie" v-model="coterie_courante.nom" :disabled="!partage_courant.admin"></v-text-field>
									<v-text-field label="URI du blason" v-model="coterie_courante.blason_uri" :disabled="!partage_courant.admin"></v-text-field>
									<v-text-field label="Description" v-model="coterie_courante.desc" :disabled="!partage_courant.admin"></v-text-field>
  							</v-layout>
							</v-card-title>
            </v-flex>
            <v-flex v-if="coterie_courante.grouped" xs12>
							<v-tooltip left>
								<v-btn v-bind:href="coterie_courante.mp_link" fab small slot="activator" target="_blank">MP</v-btn>
								<span>Envoyer un MP à la coterie</span>
							</v-tooltip>
							<v-tooltip right>
								<v-btn v-bind:href="coterie_courante.px_link" fab small slot="activator" target="_blank">PX</v-btn>
								<span>Envoyer des PX à la coterie</span>
							</v-tooltip>
							<br/><br/>
            </v-flex>
          </v-layout>
					<!-- USER SHARE STATE -->
					<v-divider v-if="loaded && coterie_courante.grouped" class="mb-3"></v-divider>
					<v-layout v-if="loaded && coterie_courante.grouped" row wrap align-center justify-center fill-height>
						<v-flex v-if="!partage_courant.pending"xs12>Vous partagez</v-flex>
						<v-flex v-else xs12>Vous avez été invité dans cette coterie, si vous acceptez vous partagerez :</v-flex>
						<v-flex xs4 d-flex><v-spacer></v-spacer><v-switch label="Vos événements" v-model="partage_courant.sharingEvents"></v-switch></v-flex>
      			<v-flex xs4 d-flex><v-spacer></v-spacer><v-switch label="Votre profil" v-model="partage_courant.sharingProfile"></v-switch></v-flex>
      			<v-flex xs4 d-flex><v-spacer></v-spacer><v-switch label="Votre vue" v-model="partage_courant.sharingView"></v-switch></v-flex>
						<!-- GROUP SHARES STATE -->
						<v-flex xs12>
							<v-card flat tile>
								<v-card-actions>
									<v-spacer></v-spacer>
									<v-tooltip top>
										<v-btn slot="activator" icon @click="show_shares = !show_shares">
            					<v-icon>{{ show_shares ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
          					</v-btn>
										<span>Partages de la coterie</span>
									</v-tooltip>
									<v-spacer></v-spacer>
        				</v-card-actions>
								<v-slide-y-transition>
          				<v-card-text v-show="show_shares" class="text-xs-center">
										<v-data-table :headers="headers" :items="partages.admins.concat(partages.users)" class="elevation-1" hide-actions>
    									<template slot="items" slot-scope="props">
												<td>{{ props.item.nom }} ({{props.item.partage.user_id}})</td>
												<td><v-icon size="16px" :color="props.item.partage.sharingEvents ? 'green' : 'red'">{{ props.item.partage.sharingEvents ? 'fas fa-check-circle' : 'fas fa-times-circle'}}</v-icon></td>
												<td><v-icon size="16px" :color="props.item.partage.sharingProfile ? 'green' : 'red'">{{ props.item.partage.sharingProfile ? 'fas fa-check-circle' : 'fas fa-times-circle'}}</v-icon></td>
												<td><v-icon size="16px" :color="props.item.partage.sharingView ? 'green' : 'red'">{{ props.item.partage.sharingView ? 'fas fa-check-circle' : 'fas fa-times-circle'}}</v-icon></td>
								    	</template>
								  	</v-data-table>
          				</v-card-text>
        				</v-slide-y-transition>
							</v-card>
						</v-flex>
					</v-layout>
					<!-- HOOKS -->
					<v-divider v-if="loaded && partage_courant.admin && coterie_courante.hooks" class="mb-3"></v-divider>
					<v-layout v-if="loaded && partage_courant.admin && coterie_courante.hooks" row wrap align-center justify-center fill-height>
						<v-flex xs11>
						Hooks
          		<v-layout row wrap align-center justify-center fill-height>
								<v-menu v-for="hook in coterie_courante.hooks" offset-y>
									<v-chip slot="activator" >
										<v-avatar><v-img :src="Image('logo-' + hook.type.toLowerCase())" contain></v-img></v-avatar>
										{{ hook.type }}
									</v-chip>
									<v-list>
										<v-list-tile v-if="hook.type === 'Discord'" :href="'https://discordapp.com/oauth2/authorize?client_id=531898253210550281&scope=bot&permissions=2048'">Inviter le bot sur mon serveur</v-list-tile>
										<v-list-tile v-if="hook.type === 'Hangouts'" @click="" v-clipboard:copy="'botsciz@gmail.com'">Copier l'adresse du bot à inviter</v-list-tile>
										<v-list-tile v-if="hook.type === 'Miaou' && hook.jwt" @click="" v-clipboard:copy="'!!sciz register ' + hook.jwt">Copier la commande d'enregistrement</v-list-tile>
										<v-list-tile v-if="hook.type === 'Discord' && hook.jwt" @click="" v-clipboard:copy="'!sciz register ' + hook.jwt">Copier la commande d'enregistrement</v-list-tile>
										<v-list-tile v-if="hook.type === 'Hangouts' && hook.jwt" @click="" v-clipboard:copy="'/sciz register '+ hook.jwt">Copier la commande d'enregistrement</v-list-tile>
										<v-list-tile v-if="hook.jwt" @click="selectedHook = hook; hook_dialog = true;">Configurer</v-list-tile>
										<v-list-tile v-if="hook.jwt" @click="regenerateHook(hook.id)" class="red--text text-darken1">Régénérer</v-list-tile>
										<v-list-tile v-else @click="regenerateHook(hook.id)" class="red--text text-darken1">Générer</v-list-tile>
									</v-list>
								</v-menu>
      				</v-layout>
							<br/>
						</v-flex>
      		</v-layout>
					<!-- SHARES -->
					<v-divider v-if="loaded && coterie_courante.grouped && !partage_courant.pending" class="mb-3"></v-divider>
					<v-layout v-if="loaded && coterie_courante.grouped && !partage_courant.pending" row wrap align-center justify-center fill-height>
						<v-flex xs11>
							Administrateur(s)
          		<v-layout row wrap align-center justify-center fill-height>
								<v-list v-for="item in partages.admins">
									<v-menu offset-y :disabled="partages.admins.length <= 1 || !partage_courant.admin">
										<v-chip slot="activator" class="red--text" :disabled="partages.admins.length <= 1 || !partage_courant.admin">	
											<v-avatar>
												<v-img :src="item.blason_uri" v-if="item.blason_uri" @error="item.blason_uri=Image('unknown')" alt="" contain></v-img>
												<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
											</v-avatar>
											{{ item.nom }}
										</v-chip>
										<v-list v-if="partages.admins.length > 1">
											<v-list-tile @click="retrograde(item)"> Rétrograder simple utilisateur </v-list-tile>
											<v-list-tile @click="exclude(item)"> Exclure de la coterie </v-list-tile>
										</v-list>
									</v-menu>
								</v-list>
      				</v-layout>
						</v-flex>
						<v-flex xs11 v-if="partages.users.length > 0">
							<br/>Utilisateur(s)
          		<v-layout row wrap align-center justify-center fill-height>
								<v-list v-for="item in partages.users">
									<v-menu offset-y :disabled="!partage_courant.admin && item.partage.user_id !== userData().id">
										<v-chip slot="activator" class="blue--text" :disabled="!partage_courant.admin && item.partage.user_id !== userData().id">	
											<v-avatar>
												<v-img :src="item.blason_uri" v-if="item.blason_uri" @error="item.blason_uri=Image('unknown')" alt="" contain></v-img>
												<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
											</v-avatar>
											{{ item.nom }}
										</v-chip>	
										<v-list>
											<v-list-tile v-if="partage_courant.admin" @click="upgrade(item)"> Promouvoir administrateur </v-list-tile>
											<v-list-tile v-if="partage_courant.admin" @click="exclude(item)"> Exclure de la coterie </v-list-tile>
											<v-list-tile v-else @click="deleteOwnShare(item)"> Quitter la coterie </v-list-tile>
										</v-list>
									</v-menu>
								</v-list>
      				</v-layout>
      			</v-flex>
						<v-flex xs11>
							<br/>Invitation(s)
          		<v-layout row wrap align-center justify-center fill-height>
									<v-autocomplete v-model="pending" :items="usersList" item-text="nom" item-value="id" multiple chips hide-no-data hide-selected cache-items :menu-props="{'closeOnContentClick': true}" no-data-text="Aucun trõll à inviter" :filter="trollFilter" :disabled="!partage_courant.admin">
		              <template slot="selection" slot-scope="data">
		                <v-chip close @input="removePending(data.item)">
											<v-avatar>
												<v-img :src="data.item.blason_uri" v-if="data.item.blason_uri" @error="data.item.blason_uri=Image('unknown')" alt="" contain></v-img>
												<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
											</v-avatar>
		                  {{ data.item.nom }}
                		</v-chip>
              		</template>
              		<template slot="item" slot-scope="data">
                  	<v-list-tile-avatar>
											<v-img :src="data.item.blason_uri" v-if="data.item.blason_uri" @error="data.item.blason_uri=Image('unknown')" alt="" contain></v-img>
											<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
                  	</v-list-tile-avatar>
                  	<v-list-tile-content>
											<v-list-tile-title> {{ data.item.nom }} ({{ data.item.id }}) </v-list-tile-title>
                  	</v-list-tile-content>
              		</template>
            		</v-autocomplete>
      				</v-layout>
						</v-flex>
					</v-layout>
        </v-card>
				<!-- SAVE BUTTON -->
				<v-btn v-if="!partage_courant.pending" class="info" @click="saveCoterie()" @keyup.native.enter="saveCoterie()">Sauvegarder</v-btn>
				<v-dialog v-if="coterie_courante.grouped && partage_courant.admin" v-model="delete_dialog" max-width="50%">
					<v-btn slot="activator" class="error">Supprimer la coterie</v-btn>
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
				<!-- INVITE  BUTTONS -->
				<v-btn v-if="partage_courant.pending" class="info" @click="acceptInvitation()">Accepter l'invitation</v-btn>
				<v-btn v-if="partage_courant.pending" class="error" @click="declineInvitation()">Décliner l'invitation</v-btn>
      </v-flex>
		</v-layout>
		<!-- HOOK DIALOG -->
		<v-dialog v-if="selectedHook" v-model="hook_dialog" full-width>
			<Format :h="selectedHook" :c="coterie_courante"></Format>
		</v-dialog>
	</v-layout>
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
				error_msg: '',
				success_msg: '',
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
          { text: 'Vue', align: 'center', value: 'partage.sharingView' }
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

