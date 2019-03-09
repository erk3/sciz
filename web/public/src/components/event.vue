<!-- TEMPLATE -->
<template>
	<v-layout row wrap justify-center align-start fill-height id="event-view" pa-3>
		<!-- SNACKBAR -->
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
		<!-- DIALOGS -->
		<v-dialog v-model="show_mail" max-width="50%" scrollable hide-overlay>
			<v-card>
				<v-card-title class="title elevation-3">{{ selectedEvent.mail_subject }}</v-card-title>
				<v-card-text><pre>{{selectedEvent.mail_body}}</pre></v-card-text>
			</v-card>
		</v-dialog>
		<v-dialog v-model="delete_dialog" max-width="50%">
      <v-card>
        <v-card-title class="headline">Supprimer cette chauve-souris ?</v-card-title>
				<v-card-text>Cette action est définitive et irréversible.<br/>L'événement ne sera plus visible de vous-même et des membres de vos coteries.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="delete_dialog = !delete_dialog">Annuler</v-btn>
          <v-btn class="error" @click="delete_dialog = !delete_dialog; deleteOneEvent(selectedEvent.id, selectedIndex)">Supprimer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
		<!-- SIDE BUTTONS -->
		<v-speed-dial v-model="fab" v-if="events.length > 0" top left direction="bottom" transition="slide-y-transition" fixed class="pt-3 mt-5">
			<v-tooltip right slot="activator">
      	<v-btn slot="activator" fab small v-model="fab">
          <v-icon size="16px">keyboard_arrow_down</v-icon>
          <v-icon size="16px">keyboard_arrow_up</v-icon>
      	</v-btn>
				<span>{{this.coterie_courante.nom}}</span>
			</v-tooltip>
			<v-tooltip right>
      	<v-btn fab small slot="activator" @click="sheet = true;">
        	<v-icon size="16px">fas fa-filter</v-icon>
      	</v-btn>
				<span>Filtrer</span>
			</v-tooltip>
			<v-tooltip right>
     		<v-btn fab small slot="activator" @click="loadEvents(limit, offset, true, false);">
        	<v-icon size="17px">fas fa-search-plus</v-icon>
      	</v-btn> 
				<span>Charger plus de chauve-souris</span>
			</v-tooltip>
			<v-tooltip right>
     		<v-btn fab small slot="activator" @click="filters=''; date = null; time = null; loadEvents(limit, 0, true, true);">
        	<v-icon size="17px">fas fa-search-minus</v-icon>
      	</v-btn> 
				<span>Supprimer les filtres et recharger</span>
			</v-tooltip>
    </v-speed-dial>
		<!-- TIMELINE -->
		<v-flex xs6 text-xs-center>
				<v-text-field label="Mots clés" v-model="filters" prepend-icon="fas fa-filter" v-on:blur="apply_search" @keyup.native.enter="apply_search"></v-text-field>
		</v-flex>
		<v-flex xs11 text-xs-center>
			<v-timeline v-scroll="onScroll" v-for="(item, index) in events" v-if="!item.hidden" :key="item.event.id" dense>
				<!-- DAY -->
				<v-timeline-item hide-dot v-if="index === 0">
					<v-layout row justify-space-between align-center fill-height>
						<b v-if="new Date().setHours(0,0,0,0) === new Date(item.event.time).setHours(0,0,0,0)">Aujourd'hui</b>
						<b v-else class="mr-3">{{ item.event.time | moment('utc', 'DD/MM/YY')}}</b>
					</v-layout>
				</v-timeline-item>
				<v-timeline-item hide-dot v-if="index > 0 && (new Date(item.event.time).setHours(0,0,0,0) !== new Date(events[index-1].event.time).setHours(0,0,0,0))">
					<v-layout row wrap justify-space-between align-center fill-height>
						<b class="mr-3">{{ item.event.time | moment('utc', 'DD/MM/YY')}}</b>
						<v-divider></v-divider>
					</v-layout>
				</v-timeline-item>
				<!-- EVENT -->
				<div v-click-outside="onClickOutside">
      	<v-timeline-item right fill-dot color="transparent" class="pa-0">
					<v-avatar size="30px" slot="icon">
        		<v-img :src="item.img">
      		</v-avatar>
					<v-layout row justify-start align-center fill-height>
						<v-layout row justify-start align-center fill-height shrink>
							<v-flex xs12>
								<span>{{ item.event.time | moment('utc', 'HH:mm:ss') }}</span><br/>
								<v-layout row justify-start align-center fill-height shrink>
									<v-flex xs6>
										<v-btn class="ma-0" icon @click="info_msg = 'Événement copié dans le presse-papier'; info = true;" v-clipboard:copy="item.repr"><v-icon size="12px">fas fa-copy</v-icon></v-btn>
									</v-flex>
									<v-flex xs6>
										<v-btn class="ma-0" icon @click="show_mail = !show_mail; selectedEvent = item.event"><v-icon size="12px">fas fa-envelope</v-icon></v-btn>
									</v-flex>
								</v-layout>
							</v-flex>
						</v-layout>
						<v-card v-bind:class="{clickable: item.type && item.event !== eventToDisplay}" class="ml-4" @click.native="onClickInside(item, $event)">
							<v-card-text v-if="eventToDisplay.id !== item.event.id || !item.type" class="body-1 pb-2 pt-2">
								{{ item.repr.slice(15) }}
							</v-card-text>
							<v-layout v-else row justify-start align-center fill-height>
								<EventCDM :cdm="item.event" v-if="item.type === 'CDM'"></EventCDM>
								<EventAA :aa="item.event" v-if="item.type === 'AA'"></EventAA>
								<EventTresor :te="item.event" v-if="item.type === 'TRESOR'"></EventTresor>
								<EventChampi :ce="item.event" v-if="item.type === 'CHAMPIGNON'"></EventChampi>
								<EventTP :tp="item.event" v-if="item.type === 'TP'"></EventTP>
								<EventCP :cp="item.event" v-if="item.type === 'CP'"></EventCP>
								<EventBattle :ba="item.event" v-if="item.type === 'BATTLE'"></EventBattle>
							</v-layout>
      			</v-card>
						<v-btn class="ma-0" icon @click="delete_dialog = !delete_dialog; selectedEvent = item.event; selectedIndex = index" v-if="item.event.owner_id === userData().id"><v-icon size="12px">fas fa-trash-alt</v-icon></v-btn>
					</v-layout>
	      </v-timeline-item>
				</div>
			</v-timeline>
		</v-flex>
		<!-- LOADING -->
		<v-flex xs6 v-if="!loaded" v-on:remove="sheet = True;" class="text-xs-center">
			<v-progress-circular :size="150" :width="15" indeterminate></v-progress-circular>
		</v-flex>
		<!-- NO EVENT -->
     <v-flex xs6 text-xs-center v-if="loaded && events.length < 1">
      <v-card flat tile class="transparent">
        <v-img :src="Image('confused')" contain max-height="300px"></v-img>
				<h1 class="display-2 text-uppercase"> Oups ! </h1><br/>
				<h2 class="title"> Aucune chauve-souris pour le moment. </h2><br/>
      </v-card>
    </v-flex>
		<!-- BOTOM BAR -->
		<v-bottom-sheet v-model="sheet" persistent>
			<v-card>
				<v-layout row justify-center align-center fill-height wrap pa-5>
					<v-flex xs4 text-xs-center>
						<v-card tile flat class="pa-5">
							<span class="title">Filtrer sur la coterie :</span><br/><br/>
							<v-select :items="[coterie_perso].concat(coteries)" item-value="id" item-text="nom" item-avatar="blason_uri" v-model="selectedCoterieID" v-on:input="should_refresh = true">
							  <template slot="selection" slot-scope="data">
    							<v-list-tile-avatar>
										<v-img v-if="data.item.blason_uri" :lazy-src="Image('unknown')" :src="data.item.blason_uri" contain></v-img>
										<v-img v-else :src="Image('unknown')" contain></v-img>
	    						</v-list-tile-avatar>
	    						<v-list-tile-content>
	      						<v-list-tile-title v-html="data.item.nom"></v-list-tile-title>
	    						</v-list-tile-content>
							  </template>
  							<template slot="item" slot-scope="data">
    							<v-list-tile-avatar>
										<v-img v-if="data.item.blason_uri" :lazy-src="Image('unknown')" :src="data.item.blason_uri" contain></v-img>
										<v-img v-else :src="Image('unknown')" contain></v-img>
	    						</v-list-tile-avatar>
	    						<v-list-tile-content>
	      						<v-list-tile-title v-html="data.item.nom"></v-list-tile-title>
	    						</v-list-tile-content>
	  						</template>
							</v-select>
						</v-card>
					</v-flex>
					<v-flex xs4 text-xs-center>
						<v-card tile flat class="pa-5">
							<span class="title">Evénéments antérieurs au :</span><br/><br/>
							<v-menu :close-on-content-click="false" v-model="date_menu" :nudge-right="40" lazy transition="scale-transition" offset-y full-width min-width="290px">
        			<v-text-field slot="activator" v-model="date" label="Date" prepend-icon="event" readonly></v-text-field>
        				<v-date-picker v-model="date" @input="date_menu = false; should_refresh = true;" :max="max_date" locale="fr"></v-date-picker>
      				</v-menu>
							<v-menu ref="time_menu" :close-on-content-click="false" v-model="time_menu" :nudge-right="40" :return-value.sync="time" lazy transition="scale-transition" offset-y full-width min-width="290px">
        			<v-text-field slot="activator" v-model="time" label="Horaire" prepend-icon="access_time" readonly></v-text-field>
        				<v-time-picker v-model="time" full-width format="24hr" locale="fr" @change="$refs.time_menu.save(time); should_refresh = true;"></v-time-picker>	
      				</v-menu>
						</v-card>
					</v-flex>
					<v-flex xs4 text-xs-center>
						<v-card tile flat class="pa-5">
							<span class="title">Rechercher les mots :</span><br/><br/>
        			<v-text-field v-model="filters" label="Mots clés" v-on:blur="apply_search"></v-text-field>
						</v-card>
					</v-flex>
					<v-flex xs6 text-xs-center>
						<v-slider label="Nombre de résultats maximum" single-line always-dirty thumb-label="always" :min="1" :max="100" v-model="limit" @change="should_refresh = true"></v-slider>
					</v-flex>
					<v-flex xs12 text-xs-center>
						<v-btn @click="sheet = !sheet; apply_filter();" @keyup.native.enter="sheet = !sheet; apply_filter();">Fermer</v-btn>
					</v-flex>
				</v-layout>
			</v-card>
		</v-bottom-sheet>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	import { deleteEvent, getEvents, getGroups } from '~/src/api.js';
	import EventCDM from '~/src/components/event-cdm.vue';
	import EventAA from '~/src/components/event-aa.vue';
	import EventTresor from '~/src/components/event-tresor.vue';
	import EventChampi from '~/src/components/event-champi.vue';
	import EventTP from '~/src/components/event-tp.vue';
	import EventCP from '~/src/components/event-cp.vue';
	import EventBattle from '~/src/components/event-battle.vue';
	
	export default {
    name: 'EventView',
		components: { EventCDM, EventAA, EventTresor, EventChampi, EventTP, EventCP, EventBattle },
		data() {
			return {
				tick: null,
				loaded: false,
				error: false,
				success: false,
				info: false,
				error_msg: '',
				success_msg: '',
				info_msg: '',
				sheet: false,
				fab: true,
				show_mail: false,
				last_time: 0,
				delete_dialog: false,
				selectedIndex: -1,
				selectedEvent: {},
				eventToDisplay: {},
				selectedCoterieID: -1,
				events: [],
				offset: 0,
				coterie_perso: {},
				coterie_courante: {},
				coteries: [],
				date_menu: false,
				time_menu: false,
				max_date: new Date().toISOString().substr(0, 10),
				date: null,
				time: null,
				filters: '',
				limit: 25,
				should_refresh: false,
			}
		},
		beforeMount() {
			this.refreshGroups();
		},
		beforeDestroy() {
			window.clearInterval(this.tick);
	  },
		methods: {
			onClickInside(item, event) {
				event.stopPropagation();
				if (this.eventToDisplay !== item.event) {
					this.eventToDisplay = item.event;
					this.$nextTick(() => {
						this.$vuetify.goTo(event.target);
					});
					this.$forceUpdate();
				}
			},
			onClickOutside(event, el) {
				this.eventToDisplay = {};
			},
			onScroll(e) {
				if (typeof window === 'undefined') return;
				const fromTop = window.pageYOffset || e.target.scrollTop || 0;
				const pageHeight = window.innerHeight;
				const bottomOfPage = document.documentElement.scrollHeight;
				if ((bottomOfPage <= fromTop + pageHeight) && this.loaded) {
					this.loadEvents(this.limit, this.offset, true, false);
				}
			},
			refreshGroups() {
				var coterie_courante = this.coterie_courante;
				getGroups(false, false, false)
					.then(res => {
						if (res.status === 200) {
							this.coterie_perso = res.data['coterie_perso'];
							this.coteries = res.data['coteries'];
							this.coterie_courante = this.coterie_perso;
							// Try to set the current coterie to the last one stored in local storage
							var lastCoterieID = this.$store.getters.coterieID;
							this.coteries.forEach(coterie => {
								if (coterie.id === lastCoterieID) {
									this.coterie_courante = coterie;
								}
							}); 	
							this.selectedCoterieID = this.coterie_courante.id;
							this.loadEvents(this.limit, 0, true, true);
							if (this.tick === null || this.tick === undefined) {
								this.tick = window.setInterval(this.loadEvents, 10000, this.limit, 0, false, false);
							}
						}
					});
			},
			deleteOneEvent(event_id, index) {
				deleteEvent(event_id)
					.then(res => {
						if (res.status === 200) {
							this.success = true;
							this.success_msg = res.data.message;
							this.$delete(this.events, index);
						}
					})
					.catch(err => {
						this.error = true;
						this.error_msg = err.message;
					});
			},
			apply_search() {
				if (this.filters) {
					var filters = this.filters.toLowerCase().split(' ');
					this.events.forEach(item => {
						item.hidden = !filters.some(filter => {
							return item.repr.toLowerCase().includes(filter);
						});
					});
				} else {
					this.events.forEach(item => {
						item.hidden = false;
					});
				}
			},
			apply_filter() {
				if (this.should_refresh) {
					this.should_refresh = false;
					this.switchCoterie();
				}
			},
			switchCoterie() {
				if (this.coterie_perso.id === this.selectedCoterieID) {
					this.coterie_courante = this.coterie_perso;
				} else {
					this.coteries.forEach(coterie => {
						if (coterie.id === this.selectedCoterieID) {
							this.coterie_courante = coterie;
						}
					}); 
				}
				this.$store.commit('setCoterieID', this.coterie_courante.id);
				this.$store.commit('setCoterieName', this.coterie_courante.nom);
				this.loadEvents(this.limit, 0, true, true);
			},
			loadEvents(limit, offset, old, force) {
				if (!force && !this.loaded) { return; }
				if (force) {
					this.offset = 0;
					this.events = [];
				}
				var lastPos = window.pageYOffset;
				this.loaded = !old;
				if (old && !force) {
					this.$vuetify.goTo(document.documentElement.scrollHeight);
				}
				var last_time = (old) ? 0 : this.last_time;
				var revert = false;
				if (this.date) {
					revert = true;
					if (this.time) {
						last_time = this.$moment.utc(this.date + ' ' + this.time, 'YYYY-MM-DD hh:mm').toDate().getTime();
					} else {
						last_time = this.$moment.utc(this.date, 'YYYY-MM-DD').toDate().getTime();
					}
				}
				if (!old && this.date) {
					return; // No call if there is a date limit and it's not an 'old' call
				}
				getEvents(this.coterie_courante.id, limit, offset, last_time, revert)
					.then(res => {
						if (res.status === 200) {
							var events = res.data['events'];
							events.forEach(item => {
								if (item.event.sciz_type === 'Connaissance des Monstres') {
									//item.color = 'orange';
									item.type = 'CDM';
									item.img = this.Image('monster-map-icon');
								} else if (item.event.sciz_type === 'Analyse Anatomique') {
									//item.color = 'pink';
									item.type = 'AA';
									item.img = this.Image('troll-map-icon');
								} else if (item.event.sciz_type === 'Trésor') {
									//item.color = 'brown';
									item.type = 'TRESOR';
									item.img = this.Image('treasure-map-icon');
								} else if (item.event.sciz_type === 'Champignon') {
									//item.color = 'lime';
									item.type = 'CHAMPIGNON';
									item.img = this.Image('mushroom-map-icon');
								} else if (item.event.sciz_type === 'Téléportation') {
									//item.color = 'grey';
									item.type = 'TP';
									item.img = this.Image('portal');
								} else if (item.event.sciz_type === 'Construire un Piège') {
									//item.color = 'grey';
									item.type = 'CP';
									item.img = this.Image('trap');
								} else if (item.event.sciz_type === 'Combat') {
									if (item.repr.includes('MORT')) {
										//item.color = 'red';
										item.img = this.Image('deadflag');
									} else if (item.event.def_id === null) {
										//item.color = 'purple';
										item.img = this.Image('pickaxe-wand-icon');
									} else {
										item.img = this.Image('fight-icon');
									}
									item.type = 'BATTLE'
								}
								var last = item.repr.indexOf('\n');
								if (last > 0) {
									item.repr = item.repr.substring(0, last - 1); // First line break
								}
								// Search
								if (this.filters) {
									var filters = this.filters.toLowerCase().split(' ');
									item.hidden = !filters.some(filter => {
										return item.repr.toLowerCase().includes(filter);
									});
								}
								// Notification
								if (!old) {
									this.$notification.show('SCIZ', {body: item.repr}, {});
								}
								// Insert ordered
								if (this.events.length < 1) {
						      this.events.splice(0, 0, item);
									this.last_time = new Date(item.event.time).getTime();
								} else {
									var l = this.events.length;
									for (var i = 0; i < this.events.length; i++) {
										if (new Date(item.event.time).getTime() - new Date(this.events[i].event.time).getTime() >= 0) {
						        	this.events.splice(i, 0, item);
											if (i === 0) {
												this.last_time = new Date(item.event.time).getTime();
											}
						        	break;
							    	}
									}
									if (l === this.events.length) {
										this.events.push(item);
									}
								}
							});
							this.offset += events.length;
						}
						if (old && !force) {
							this.$vuetify.goTo(lastPos);
						}
						this.$nextTick(() => {
							this.loaded = true;
						});
					});
			}
		}
	}
</script>

<style>
.clickable {
	cursor:pointer;
}
pre {
    white-space: pre-wrap;
}
.v-timeline-item__dot, .v-timeline-item__inner-dot, .v-image, .v-avatar {
	background: unset !important;
	box-shadow: unset !important;
	border-radius: unset !important;
}

</style>
