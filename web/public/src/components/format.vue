<!-- TEMPLATE -->
<template>
	<v-card class="pa-5 text-xs-center">
		<!-- SNACKBAR -->
		<v-snackbar v-model="error" color="error" :timeout="6000" top>
			{{ error_msg }}
	    <v-btn dark flat @click="error = false">Fermer</v-btn>
	  </v-snackbar>
		<v-snackbar v-model="success" color="success" :timeout="6000" top>
	    {{ success_msg }}
	    <v-btn dark flat @click="success = false">Fermer</v-btn>
	  </v-snackbar>
		<!-- HEADER & BUTTONS -->
		<span class="display-1">{{c.nom}}</span><br/><br/>
		<span class="title">Configuration du hook {{h.type}}</span><br/><br/>
		<v-btn class="info" @click="saveConfig()" :disabled="!loaded">Sauvegarder la configuration</v-btn>
		<v-btn class="error" @click="resetConfig()" :disabled="!loaded">Réinitialiser la configuration</v-btn>
		<br/><br/>
		<v-divider></v-divider>
		<!-- LOADING -->
		<v-flex v-if="!loaded" class="text-xs-center">
			<v-progress-circular :size="150" :width="15" indeterminate></v-progress-circular>
		</v-flex>
		<!-- TAB BAR -->
		<v-tabs fixed-tabs v-if="loaded">
			<v-tab>FILTRES</v-tab>
			<v-tab>ABRÉVIATIONS</v-tab>
    	<v-tab v-for="(item, key, index) in format" v-if="key !== consts.ABREVIATIONS && key !== consts.FILTRES">
				<span v-html="consts[key]"></span>
    	</v-tab>
			<!-- FILTRES -->
    	<v-tab-item class="mt-4">
				<v-layout row wrap align-center justify-center fill-height>
					<v-flex xs12>
						<v-layout row wrap align-center justify-center fill-height>
							<v-flex xs8>
								<v-alert :value="true" type="warning" class="mb-4" outline> Les événements filtrés ne seront pas transmis. Les filtres sont appliqués APRÈS les abréviations.</v-alert>
							</v-flex>
						</v-layout>
					</v-flex>
					<v-flex xs4>
						<v-text-field v-model="new_filter" placeholder="Suite de mots à filtrer" label="Ajouter un filtre sur :" hint="Sensible à la casse" prepend-icon="fas fa-plus fa-md" @click:prepend="addFilter()"><v-text-field>
					</v-flex>
					<v-flex offset-xs1 xs4>
						<v-layout v-for="(subitem, subindex) in format[consts.FILTRES]" row wrap align-center justify-center fill-height>
							<v-flex xs12>
								<v-text-field :value="subitem" v-model="format[consts.FILTRES][subindex]" append-outer-icon="fas fa-trash-alt fa-xs" @click:append-outer="delFilter(subindex, false)" v-on:blur="delFilter(subindex, true)"><v-text-field>
							</v-flex>
						</v-layout>
					</v-flex>
				</v-layout>
			</v-tab-item>
			<!-- ABREVIATIONS -->
    	<v-tab-item class="mt-4">
				<v-layout row wrap align-center justify-center fill-height>
					<v-flex xs12>
						<v-layout row wrap align-center justify-center fill-height>
							<v-flex xs8>
								<v-alert :value="true" type="warning" class="mb-4" outline> Les abréviations sont appliquées AVANT les filtres.</v-alert>
							</v-flex>
						</v-layout>
					</v-flex>
					<v-flex xs4>
						<v-text-field v-model="new_abr" placeholder="Suite de mots à remplacer" label="Ajouter une abréviation pour :" hint="Sensible à la casse" prepend-icon="fas fa-plus fa-md" @click:prepend="addAbr()"><v-text-field>
					</v-flex>
					<v-flex offset-xs1 xs4>
						<v-layout v-for="(item, subkey, subindex) in format[consts.ABREVIATIONS]" row wrap align-center justify-center fill-height>
							<v-flex xs12>
								<v-text-field :placeholder="subkey" :label="subkey" :value="item" v-model="format[consts.ABREVIATIONS][subkey]" append-outer-icon="fas fa-trash-alt fa-xs" @click:append-outer="delAbr(subkey, false)" v-on:blur="delAbr(subkey, true)"><v-text-field>
							</v-flex>
						</v-layout>
					</v-flex>
				</v-layout>
			</v-tab-item>
			<!-- FORMATS -->
    	<v-tab-item v-for="(item, key, index) in format" v-if="key !== consts.ABREVIATIONS && key !== consts.FILTRES" class="mt-4" :key="key">
				<v-layout row wrap align-center justify-center fill-height>
					<!-- NOTIFICATION -->
					<v-flex xs8 class="mt-4" v-if="consts.NOTIF in format[key]"> 
						<v-card>
							<v-card-title>{{consts.NOTIF}}</v-card-title>
							<v-combobox v-model="format[key][consts.NOTIF]" :items="getSubKeys(format[key], [consts.ATTR_C, consts.ATTR])" multiple small-chips deletable-chips hide-selected class="ml-5 mr-5" :menu-props="{'closeOnClick': true, 'closeOnContentClick': true, 'maxHeight': '200px'}" :key="key + consts.NOTIF">
								<template slot="selection" slot-scope="{ item, parent, selected }">
	      					<v-chip :color="getChipColor(key, item)" label small closable v-if="getSubKeys(format[key], [consts.ATTR_C, consts.ATTR]).includes(item)">
										<span class="pr-2">{{ item.substring(1, item.length - 1) }}</span>
	        					<v-icon small @click="parent.selectItem(item)">close</v-icon>
	      					</v-chip>
	      					<v-chip label small closable outline v-else>
										<span class="pr-1 pl-1">{{ item }}</span>
	        					<v-icon small @click="parent.selectItem(item)">close</v-icon>
	      					</v-chip>
	    					</template>
								<template slot="item" slot-scope="{ item, parent, selected }">
	      					<v-chip :color="getChipColor(key, item)" label small closable>
										<span>{{ item.substring(1, item.length - 1) }}</span>
	      					</v-chip>
	    					</template>
							</v-combobox>
						</v-card>
					</v-flex>
					<!-- ATTRIBUTS CONSTRUITS -->
					<v-flex xs8 class="mt-4" v-if="consts.ATTR_C in format[key]"> 
						<v-card>
							<v-card-title>{{consts.ATTR_C}}</v-card-title>
							<v-layout row wrap align-center justify-center fill-height>
								<v-flex xs12 v-for="(subitem, subkey, subindex) in format[key][consts.ATTR_C]" :key="key+subkey+consts.ATTR_C">
									<v-layout row wrap align-center justify-end fill-height ma-2>
										<v-flex xs3> 
	      							<v-chip color="teal" label small closable> {{subkey}} </v-chip>
										</v-flex>
										<v-flex xs9>
											<v-combobox v-model="format[key][consts.ATTR_C][subkey]" :items="getSubKeys(format[key], [consts.ATTR_C, consts.ATTR], [subkey])" :label="subkey" multiple small-chips deletable-chips hide-selected class="ml-5 mr-5" :menu-props="{'closeOnClick': true, 'closeOnContentClick': true, 'maxHeight': '200px'}">
												<template slot="selection" slot-scope="{ item, parent, selected }">
					      					<v-chip :color="getChipColor(key, item)" label small closable v-if="getSubKeys(format[key], [consts.ATTR_C, consts.ATTR]).includes(item)">
														<span class="pr-2">{{ item.substring(1, item.length - 1) }}</span>
					        					<v-icon small @click="parent.selectItem(item)">close</v-icon>
					      					</v-chip>
					      					<v-chip label small closable outline v-else>
														<span class="pr-1 pl-1">{{ item }}</span>
					        					<v-icon small @click="parent.selectItem(item)">close</v-icon>
					      					</v-chip>
					    					</template>
												<template slot="item" slot-scope="{ item, parent, selected }">
					      					<v-chip :color="getChipColor(key, item)" label small closable>
														<span>{{ item.substring(1, item.length - 1) }}</span>
					      					</v-chip>
												</template>
											</v-combobox>
										</v-flex>
									</v-layout>
								</v-flex>
							</v-layout>
						</v-card>
					</v-flex>
					<!-- ATTRIBUTS -->
					<v-flex xs8 class="mt-4" v-if="consts.ATTR in format[key]"> 
						<v-card>
							<v-card-title>{{consts.ATTR}}</v-card-title>
							<v-layout row wrap align-center justify-center fill-height>
								<v-flex xs12 v-for="(subitem, subkey, subindex) in format[key][consts.ATTR]" :key="key+subkey+consts.ATTR">
									<v-layout row wrap align-center justify-end fill-height ma-2>
										<v-flex xs3> 
	      							<v-chip :color="key !== 'Event' ? 'brown' : 'blue-grey'" label small closable> {{subkey}} </v-chip>
										</v-flex>
										<v-flex xs9>
											<v-layout row wrap align-center justify-start fill-height>
												<v-flex xs4 v-for="(subsubitem, subsubkey, subsubindex) in format[key][consts.ATTR][subkey]" v-if="subsubkey !== 'Attribut'">
													<v-text-field v-model="format[key][consts.ATTR][subkey][subsubkey]" :label="subsubkey" class="ml-5 mr-5" :key="key+subkey+consts.ATTR+subsubkey" hide-details placeholder=' '>
													</v-text-field>
												</v-flex>
											</v-layout>
										</v-flex>
									</v-layout>
								</v-flex>
							</v-layout>
						</v-card>
					</v-flex>
				</v-layout>
    	</v-tab>
  	</v-tabs>
	</v-card>
</template>

<!-- SCRIPT -->
<script>
	import { getFormat, saveFormat, resetFormat } from '~/src/api.js';

	export default {
		name: 'Format',
		props: {
			h: { type: Object, default: null },
			c: { type: Object, default: null },
		},
		watch: {
      h: function(newHook, oldHook) {
				this.loadHook(newHook);
    	}
		},
		beforeMount() {
			this.loadHook(this.h);
		},
		data() {
			return {
				loaded: false,
				format: {},
				error: false,
				success: false,
				error_msg: '',
				success_msg: '',
				new_abr: '',
				new_filter: '',
				consts: {
					ABREVIATIONS: 'Abréviations',
					FILTRES: 'Filtres',
					Event: 'Événement<br/>Commun',
					battleEvent: 'Événements<br/>Combat',
					tresorEvent: 'Événements<br/>Trésor',
					champiEvent: 'Événements<br/>Champignon',
					tpEvent: 'Événements<br/>TP',
					cpEvent: 'Événements<br/>Piège',
					aaEvent: 'Événements<br/>AA',
					cdmEvent: 'Événements<br/>CdM',
					TrollPrivate: 'Trõll',
					TrollPrivateCapa: 'Compétence<br/>Sort',
					MobPrivate: 'Monstre',
					TresorPrivate: 'Trésor',
					ChampiPrivate: 'Champignon',
					Lieu: 'Lieu<br/>Commun',
					Portail: 'Portail',
					Piege: 'Piège',
					NOTIF: 'Notification',
					ATTR_C: 'Attributs construits',
					ATTR: 'Attributs',
				}	
			}
		},
		methods: {
			loadHook(hook) {
				this.new_abr = '';
				this.new_filter = '';
				this.loaded = false;
				getFormat(hook.id).then(res => {
					if (res.status === 200) {
						this.format = JSON.parse(res.data.format);
						if (!(this.consts.FILTRES in this.format)) {
							this.format[this.consts.FILTRES] = []
						}
						if (!(this.consts.ABREVIATIONS in this.format)) {
							this.format[this.consts.ABREVIATIONS] = {}
						}
						this.loaded = true;
					}
				});
			},
			getSubKeys(f, subkeys, excludes) {
				var arr = [];
				subkeys.forEach(subkey => {
					if (subkey in f) {
						arr = arr.concat(Object.keys(f[subkey]).map(x => '{' + x + '}'))
					}
					if (subkey in this.format['Event']) {
						arr = arr.concat(Object.keys(this.format['Event'][subkey]).map(x => '{' + x + '}'))
					}
					else if (subkey in this.format['Lieu']) {
						arr = arr.concat(Object.keys(this.format['Lieu'][subkey]).map(x => '{' + x + '}'))
					}
				});
				if (excludes !== undefined) {
					excludes.forEach(exclude => {
						if (arr.indexOf('{' + exclude + '}') > -1) {
							arr.splice(arr.indexOf('{' + exclude + '}'), 1);
						}
					})
				}
				return arr;
			},
			getChipColor(k, i) {
				if (this.consts.ATTR_C in this.format[k] && i.substring(1, i.length - 1)  in this.format[k][this.consts.ATTR_C]) {
					return 'teal';
				} else if (this.consts.ATTR in this.format[k] && i.substring(1, i.length - 1) in this.format[k][this.consts.ATTR]) {
					if (k === 'Event' || k === 'Lieu') {
						return 'blue-grey';
					}
					return 'brown';
				}
				return 'blue-grey';
			},
			addFilter() {
				if (this.new_filter && this.new_filter !== '') {
					this.format[this.consts.FILTRES].push(this.new_filter);
					this.new_filter = '';
				}
			},
			delFilter(index, checkEmptinessBefore) {
				if (!checkEmptinessBefore || this.format[this.consts.FILTRES][index] === '') {
					this.$delete(this.format[this.consts.FILTRES], index);
				}
			},
			addAbr() {
				if (this.new_abr && this.new_abr !== '') {
					this.$set(this.format[this.consts.ABREVIATIONS], this.new_abr, this.new_abr);
					this.new_abr = '';
				}
			},
			delAbr(abr) {
				this.$delete(this.format[this.consts.ABREVIATIONS], abr);
			},
			delAbr(abr, checkEmptinessBefore) {
				if (!checkEmptinessBefore || this.format[this.consts.ABREVIATIONS][abr] === '') {
					this.$delete(this.format[this.consts.ABREVIATIONS], abr);
				}
			},
			saveConfig() {
				saveFormat(this.h.id, this.format)
					.then(res => {
						if (res.status === 200) {
							this.success = true;
							this.success_msg = res.data.message;
						}
					})
					.catch(err => {
						this.error = true;
						this.error_msg = err.message;
					});
			},
			resetConfig() {
				resetFormat(this.h.id)
					.then(res => {
						if (res.status === 200) {
							this.success = true;
							this.success_msg = res.data.message;
							this.loadHook(this.h);
						}
					})
					.catch(err => {
						this.error = true;
						this.error_msg = err.message;
					});
			},
		},
	}
</script>
