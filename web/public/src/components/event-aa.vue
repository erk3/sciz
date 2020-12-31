<!-- TEMPLATE -->
<template>
	<v-row justify="center" align="center" class="fill-height ma-4">
		<!-- HEADER -->
		<v-col class="col-12 mb-5 text-center">
			<h4 class="display-1">Analyse Anatomique</h4>
			<span>de</span>
			<v-avatar>
				<v-img v-if="aa.owner_blason_uri" :src="aa.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{aa.owner_nom}} ({{aa.owner_id}})</span><br/>
		</v-col>
		<!-- MOB -->
		<v-col class="col-12 text-center">
			<v-row wrap justify="center" align="end" class="fill-height pa-4">
				<v-col class="col-4">
					<v-img v-if="aa.troll_blason_uri" :src="aa.troll_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="100px"></v-img>
					<v-img v-else :src="Image('unknown')" alt="" contain max-height="100px"></v-img>
					<br/>{{aa.troll_nom}} ({{aa.troll_id}})
					<v-btn v-bind:href="aa.troll_link" v-bind:class="{'ma-0': true}" icon target="_blank">
						<v-icon size="14px">fas fa-link</v-icon>
					</v-btn>
				</v-col>
				<v-col class="col-4 offset-1">
					<h3 class="display-2">{{aa.blessure}} %</h3>
					<span>
						Reste entre
						<v-tooltip bottom>
							<template v-slot:activator="{ on, attrs }">
								<u v-bind="attrs" v-on="on">{{pdv_min}}</u>
							</template>
							<span>~{{(100 - Math.min(100, aa.blessure + 5))}}% de {{aa.base_pdv_min}}</span>
						</v-tooltip>
						et
						<v-tooltip bottom>
							<template v-slot:activator="{ on, attrs }">
								<u v-bind="attrs" v-on="on">{{pdv_max}}</u>
							</template>
							<span>~{{(100 - Math.max(1, aa.blessure - 4))}}% de {{aa.base_pdv_max}}</span>
						</v-tooltip>
						points de vie
					</span><br/><br/>
					<v-progress-linear class="mb-2" :color="aa.blessure > 75 ? 'error' : (aa.blessure > 25 ? 'warning' : 'success')" height="15" :value="100 - aa.blessure" buffer-value="100"></v-progress-linear>
				</v-col>
			</v-row>
		</v-col>
		<!-- DATA -->
		<v-col class="col-12 text-center">
			<v-row wrap justify="center" align="start" class="fill-height">
				<v-col class="col-4 text-center">
					<v-card flat>
		      		<v-divider></v-divider>
						<v-list v-for="(carac, index) in cnum" dense class="pa-0" :key="index">
							<v-list-item>
								<v-list-item-content>{{carac.k}}</v-list-item-content>
								<v-list-item-content class="align-end">
									<v-tooltip v-if="carac.t" right>
										<template v-slot:activator="{ on, attrs }">
											<u v-bind="attrs" v-on="on">{{carac.v}}</u>
										</template>
										<span>{{carac.t}}</span>
									</v-tooltip>
									<span v-else>{{carac.v}}</span>
								</v-list-item-content>
							</v-list-item>
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
		name: 'EventAA',
		props: {
			aa: {
				type: Object,
				default: null
			}
		},
		data() {
			return {
				cnum: [],
			}
		},
		computed: {
			pdv_min: function () {
				if (this.aa.blessure === 0) {
					return this.aa.base_pdv_min;
				}
				return Math.floor(this.aa.base_pdv_min * (100 - Math.min(100, this.aa.blessure + 5)) / 100);
			},
			pdv_max: function () {
				if (this.aa.blessure === 0) {
					return this.aa.base_pdv_max;
				}
				return Math.ceil(this.aa.base_pdv_max * (100 - Math.max(1, this.aa.blessure - 4)) / 100);
			},
		},
		beforeMount() {
			// Caractéristiques numériques
			this.cnum.push({k: 'Niveau', v: this.aa.niv})
			this.cnum.push({k: 'Points de vie', v: this.displayMinMax(this.aa.base_pdv_min, this.aa.base_pdv_max, true)})
			this.cnum.push({k: 'Attaque (D6)', v: this.displayMinMax(this.aa.base_att_min, this.aa.base_att_max, true)})
			this.cnum.push({k: 'Esquive (D6)', v: this.displayMinMax(this.aa.base_esq_min, this.aa.base_esq_max, true)})
			this.cnum.push({k: 'Dégâts (D3)', v: this.displayMinMax(this.aa.base_deg_min, this.aa.base_deg_max, true)})
			this.cnum.push({k: 'Régénération (D3)', v: this.displayMinMax(this.aa.base_reg_min, this.aa.base_reg_max, true)})
			this.cnum.push({k: 'Vue', v: this.displayMinMax(this.aa.base_vue_min, this.aa.base_vue_max, true)})
			this.cnum.push({k: 'Armure (D3)', v: this.displayMinMax(this.aa.base_arm_min, this.aa.base_arm_max, true)})
		}
	}
</script>
