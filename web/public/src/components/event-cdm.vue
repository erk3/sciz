<!-- TEMPLATE -->
<template>
	<v-layout row wrap justify-center align-center fill-height pa-4>
		<!-- HEADER -->
		<v-flex xs12 mb-5>
			<h4 class="display-1">Connaissance des Monstres</h4>
			<h6 class="title">(Niveau {{cdm.cdm_niv}})</h6><br/>
			<span>de</span>
			<v-avatar>
				<v-img v-if="cdm.owner_blason_uri" :src="cdm.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{cdm.owner_nom}} ({{cdm.owner_id}})</span><br/>
		</v-flex>
		<!-- MOB -->
		<v-flex xs12 text-xs-center mb-5>
			<v-layout row align-end justify-center fill-height>
				<v-flex xs4>
					<v-img v-if="cdm.mob_blason_uri" :src="cdm.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="100px"></v-img>
					<v-img v-else :src="Image('unknown')" alt="" contain max-height="100px"></v-img>
					<br/>{{cdm.mob_nom}} [{{cdm.mob_age}}] ({{cdm.mob_id}})
					<v-btn v-bind:href="cdm.mob_link" v-bind:class="{'ma-0': true}" icon target="_blank">
						<v-icon size="14px">fas fa-link</v-icon>
					</v-btn>
				</v-flex>
				<v-flex offset-xs1 xs4>
					<h3 class="display-2">{{cdm.blessure}} %</h3>
					<span>
						Reste entre
						<v-tooltip bottom>
							<span slot="activator"><u>{{pdv_min}}</u></span>
							<span>~{{(100 - Math.min(100, cdm.blessure + 5))}}% de {{cdm.pdv_min}}</span>
						</v-tooltip>
						et 
						<v-tooltip bottom>
							<span slot="activator"><u>{{pdv_max}}</u></span>
							<span>~{{(100 - Math.max(1, cdm.blessure - 4))}}% de {{cdm.pdv_max}}</span>
						</v-tooltip>
						points de vie
					</span>
					<v-progress-linear class="mb-2" :color="cdm.blessure > 75 ? 'error' : (cdm.blessure > 25 ? 'warning' : 'success')" height="15" :value="100 - cdm.blessure" buffer-value="100"></v-progress-linear>
				</v-flex>
			</v-layout>
		</v-flex>
		<!-- DATA -->
		<v-flex xs12 text-xs-center>
			<v-layout row align-start justify-center fill-height>
				<v-flex xs4 text-xs-center>
					<v-card flat>
		      	<v-divider></v-divider>
						<v-list v-for="carac in ctxt" dense class="pa-0">
							<v-list-tile>
								<v-list-tile-content>{{carac.k}}</v-list-tile-content>
								<v-list-tile-content class="align-end">
									<v-tooltip v-if="carac.t" right>
										<span slot="activator"><u>{{carac.v}}</u></span>
										<span>{{carac.t}}</span>
									</v-tooltip>
									<span v-else>{{carac.v}}</span>
								</v-list-tile-content>
							</v-list-tile>
						</v-list>
		    	</v-card>
				</v-flex>
				<v-flex offset-xs1 xs4 text-xs-center>
					<v-card flat>
		      	<v-divider></v-divider>
						<v-list v-for="carac in cnum" dense class="pa-0">
							<v-list-tile>
								<v-list-tile-content>{{carac.k}}</v-list-tile-content>
								<v-list-tile-content class="align-end">
									<v-tooltip v-if="carac.t" right>
										<div slot="activator"><u>{{carac.v}}</u></div>
										<span>{{carac.t}}</span>
									</v-tooltip>
									<span v-else>{{carac.v}}</span>
								</v-list-tile-content>
							</v-list-tile>
						</v-list>
		    	</v-card>
				</v-flex>
			</v-layout>
		</v-flex>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	export default {
		name: 'EventCDM',
		props: {
			cdm: {
				type: Object,
				default: null
			}
		},
		data() {
			return {
				ctxt: [],
				cnum: [],
			}
		},
		computed: {
			pdv_min: function () {
				if (this.cdm.blessure === 0) {
					return this.cdm.pdv_min;
				}
				return Math.floor(this.cdm.pdv_min * (100 - Math.min(100, this.cdm.blessure + 5)) / 100);
			},
			pdv_max: function () {
				if (this.cdm.blessure === 0) {
					return this.cdm.pdv_max;
				}
				return Math.ceil(this.cdm.pdv_max * (100 - Math.max(1, this.cdm.blessure - 4)) / 100);
			},
		},
		beforeMount() {
			// Caractéristiques textuelles
			var capa_tooltip = '';
    	capa_tooltip += (this.cdm.capa_effet) ? 'Affecte : ' + this.cdm.capa_effet : '';
    	capa_tooltip += (this.cdm.capa_tour) ? ' pour ' + this.cdm.capa_tour + 'T' : '';
    	capa_tooltip += (this.cdm.capa_portee) ? ' (' + this.cdm.capa_portee + ')' : '';
			capa_tooltip = (capa_tooltip === '') ? null : capa_tooltip;
			this.ctxt.push({k: 'Race', v: this.cdm.mob_race})
			this.ctxt.push({k: 'Capacité spéciale', v: this.cdm.capa_desc ? this.cdm.capa_desc : '-', t: capa_tooltip})
			this.ctxt.push({k: 'Portée de la capacité spéciale', v: this.cdm.capa_portee ? this.cdm.capa_portee : '-'})
			this.ctxt.push({k: 'Nombre d\'attaque par tour', v: this.cdm.nb_att_tour ? this.cdm.nb_att_tour : '-'})
			this.ctxt.push({k: 'Vitesse de déplacement', v: this.cdm.vit_dep ? this.cdm.vit_dep : '-'})
			this.ctxt.push({k: 'Attaque à distance ?', v: this.boolean2french(this.cdm.att_dist)})
			this.ctxt.push({k: 'Attaque magique ?', v: this.boolean2french(this.cdm.att_mag)})
			this.ctxt.push({k: 'Voir le caché ?', v: this.boolean2french(this.cdm.vlc)})
			this.ctxt.push({k: 'Voleur ?', v: this.boolean2french(this.cdm.voleur)})
			this.ctxt.push({k: 'Sang froid', v: this.cdm.sang_froid ? this.cdm.sang_froid : '-'})
			this.ctxt.push({k: 'DLA', v: this.cdm.dla ? this.cdm.dla : '-'})
			this.ctxt.push({k: 'Chargement', v: this.cdm.chargement ? this.cdm.chargement : '-'})
			// Caractéristiques numériques
			this.cnum.push({k: 'Niveau', v: this.displayMinMax(this.cdm.niv_min, this.cdm.niv_max, true)})
			this.cnum.push({k: 'Points de vie', v: this.displayMinMax(this.cdm.pdv_min, this.cdm.pdv_max, true)})
			this.cnum.push({k: 'Attaque (D6)', v: this.displayMinMax(this.cdm.att_min, this.cdm.att_max, true)})
			this.cnum.push({k: 'Esquive (D6)', v: this.displayMinMax(this.cdm.esq_min, this.cdm.esq_max, true)})
			this.cnum.push({k: 'Dégâts (D3)', v: this.displayMinMax(this.cdm.deg_min, this.cdm.deg_max, true)})
			this.cnum.push({k: 'Régénération (D3)', v: this.displayMinMax(this.cdm.reg_min, this.cdm.reg_max, true)})
			this.cnum.push({k: 'Vue', v: this.displayMinMax(this.cdm.vue_min, this.cdm.vue_max, true)})
			this.cnum.push({k: 'Armure physique', v: this.displayMinMax(this.cdm.arm_phy_min, this.cdm.arm_phy_max, true)})
			this.cnum.push({k: 'Armure magique', v: this.displayMinMax(this.cdm.arm_mag_min, this.cdm.arm_mag_max, true)})
			this.cnum.push({k: 'Maitrise magique', v: this.displayMinMax(this.cdm.mm_min, this.cdm.mm_max, true)})
			this.cnum.push({k: 'Résistance magique', v: this.displayMinMax(this.cdm.rm_min, this.cdm.rm_max, true)})
			this.cnum.push({k: 'Durée du tour (h)', v: this.displayMinMax(this.cdm.tour_min, this.cdm.tour_max, true)})
		}
	}
</script>
