<!-- TEMPLATE -->
<template>
	<v-row justify="center" align="center" class="fill-height ma-4">
		<!-- HEADER -->
		<v-col class="col-12 mb-5 text-center">
			<h4 class="display-1">{{ba.type}}</h4>
			<p v-if="ba.subtype !== ''">{{ba.subtype}}</p>
		</v-col>
		<!-- BEINGS-->
		<v-col class="col-12 text-center pa-0">
			<v-row wrap justify="center" align="end" class="fill-height pa-4">
				<v-col class="col-5">
					<div v-if="!def_event">
						<v-img v-if="ba.att_blason_uri" :src="ba.att_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="100px"></v-img>
						<v-img v-else :src="Image('unknown')" alt="" contain max-height="100px"></v-img>
						<br/><span v-if="ba.att_id < 300000">de </span><span v-else>d'</span>{{ba.att_nom}} ({{ba.att_id}})
						<v-btn v-bind:href="ba.att_link" v-bind:class="{'ma-0': true}" icon target="_blank">
							<v-icon size="14px">fas fa-link</v-icon>
						</v-btn>
					</div>
				</v-col>
				<v-col class="col-2">
					<span v-if="!att_event" class="display-1">VS <br/></span>
					<span v-if="ba.pdv" class="title text--"><br/>-{{ba.pdv}} PV<br/></span>
					<span v-else-if="ba.deg" class="title">-{{ba.deg}} PV<br/></span>
					<span v-if="ba.vie">(reste {{ba.vie}})<br/></span><br/>
					<v-img v-if="ba.vie !== null && ba.vie === 0" :src="Image('deadflag')" alt="" contain max-height="70px"></v-img>
				</v-col>
				<v-col class="col-5">
					<div v-if="!att_event">
						<div class="container-overlay">
							<v-img v-if="ba.def_blason_uri" :src="ba.def_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="100px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="100px"></v-img>
							<div class="overlay">
								<v-img v-if="ba.vie !== null && ba.vie === 0" :src="Image('deadstamp')" alt="" contain max-height="100px"></v-img>
							</div>
						</div>
						<br/>sur {{ba.def_nom}} ({{ba.def_id}})
						<v-btn v-bind:href="ba.def_link" v-bind:class="{'ma-0': true}" icon target="_blank">
							<v-icon size="14px">fas fa-link</v-icon>
						</v-btn>
					</div>
				</v-col>
				<v-col class="col-5">
					<div v-if="follower_event && ba.att_id !== ba.owner_id && ba.att_id >= 300000">
						<span>appartenant à </span>
						<v-avatar>
							<v-img v-if="ba.owner_blason_uri" :src="ba.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						</v-avatar>
						<span>{{ba.owner_nom}} ({{ba.owner_id}})</span>
						<v-btn v-bind:href="ba.owner_link" v-bind:class="{'ma-0': true}" icon target="_blank">
							<v-icon size="14px">fas fa-link</v-icon>
						</v-btn>
					</div>
				</v-col>
				<v-col class="col-2">
				</v-col>
				<v-col class="col-5">
					<div v-if="ba.autre_id">
						<span>s'interposant pour </span>
						<v-avatar>
							<v-img v-if="ba.autre_blason_uri" :src="ba.autre_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						</v-avatar>
						<span>{{ba.autre_nom}} ({{ba.autre_id}})</span>
						<v-btn v-bind:href="ba.autre_link" v-bind:class="{'ma-0': true}" icon target="_blank">
							<v-icon size="14px">fas fa-link</v-icon>
						</v-btn>
					</div>
					<div v-if="follower_event && ba.def_id !== ba.owner_id && ba.def_id >= 300000">
						<span>appartenant à </span>
						<v-avatar>
							<v-img v-if="ba.owner_blason_uri" :src="ba.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
						</v-avatar>
						<span>{{ba.owner_nom}} ({{ba.owner_id}})</span>
						<v-btn v-bind:href="ba.owner_link" v-bind:class="{'ma-0': true}" icon target="_blank">
							<v-icon size="14px">fas fa-link</v-icon>
						</v-btn>
					</div>
				</v-col>
			</v-row>
		</v-col>
		<!-- CAPA -->
		<v-col class="col-12 text-center pt-0" v-if="ba.capa_desc || ba.capa_effet">
			<h5 class="title" v-if="ba.type !== ba.capa_desc && ba.capa_desc">{{ba.capa_desc}}</h5>
			<h5 class="title" v-else>Effet</h5>
			<span>{{ba.capa_effet}}</span><span v-if="ba.capa_tour"> pour {{ba.capa_tour}}T</span>
		</v-col>
		<!-- DATA -->
		<v-col class="col-12 text-center" v-if="catt.some((e) => { return e.v}) || cdef.some((e) => { return e.v})">
			<v-row wrap justify="center" align="start" class="fill-height">
				<v-col class="col-5">
					<v-card flat v-if="catt.some((e) => { return e.v})">
		      			<v-divider></v-divider>
						<v-list v-for="(carac, index) in catt" dense class="pa-0" :key="index">
							<v-list-item v-if="carac.v">
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
				</v-col>
				<v-col class="col-5 offset-2 text-center">
					<v-card flat v-if="cdef.some((e) => { return e.v})">
		      			<v-divider></v-divider>
						<v-list v-for="(carac, index) in cdef" dense class="pa-0" :key="index">
							<v-list-item v-if="carac.v">
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
				</v-col>
			</v-row>
		</v-col>
	</v-row>
</template>

<!-- SCRIPT -->
<script>
	export default {
		name: 'EventBattle',
		props: {
			ba: {
				type: Object,
				default: null
			}
		},
		data() {
			return {
				catt: [],
				cdef: [],
			}
		},
		computed: {
			att_event: function () {
				return this.ba.att_id && !this.ba.def_id && !this.ba.autre_id;
			},
			def_event: function () {
				return this.ba.def_id && !this.ba.att_id && !this.ba.autre_id;
			},
			follower_event: function () {
				return this.ba.owner_id !== this.ba.att_id && this.ba.owner_id !== this.ba.def_id && this.ba.owner_id !== this.ba.autre_id;
			},
			pos: function () {
				var pos = '';
				pos += (this.ba.pos_x !== null) ? 'X = ' + this.ba.pos_x : '';
				pos += (this.ba.pos_y !== null) ? ((pos !== '') ? ' | Y = ' + this.ba.pos_y : 'Y = ' + this.ba.pos_y) : '';
				pos += (this.ba.pos_n !== null) ? ((pos !== '') ? ' | N = ' + this.ba.pos_n : 'N = ' + this.ba.pos_n) : '';
				return (pos === '') ? null : pos;
			},
			dir: function () {
				var dir = '';
				dir += (this.ba.dir_x !== null) ? this.ba.dir_x : '';
				dir += (this.ba.dir_y !== null) ? ((dir !== '') ? ' ' + this.ba.dir_y : this.ba.dir_y) : '';
				dir += (this.ba.dir_n !== null) ? ((dir !== '') ? ' ' + this.ba.dir_n : this.ba.dir_n) : '';
				return (dir === '') ? null : dir;
			}
		},
		beforeMount() {
			// Caractéristiques ATT
			this.catt.push({k: 'Jet d\'attaque', v: this.ba.att});
			this.catt.push({k: 'Jet de déstabilisation', v: this.ba.destab});
			this.catt.push({k: 'Jet de résistance', v: this.ba.resi});
			this.catt.push({k: 'Blessure', v: this.ba.blessure});
			this.catt.push({k: 'Jet de dégâts', v: this.ba.deg});
			this.cdef.push({k: 'Soin', v: (this.ba.type.includes('Régénération') || this.ba.type.includes('Vampirisme')) ? this.ba.soin : null});
			this.catt.push({k: 'Position', v: this.pos});
			this.catt.push({k: 'Gain de MM', v: this.ba.mm});
			this.catt.push({k: 'Gain de fatigue', v: this.ba.fatigue});
			this.catt.push({k: 'Gain de PX', v: this.ba.px});
			// Caractéristiques DEF
			this.cdef.push({k: 'Jet d\'esquive', v: this.ba.esq});
			this.cdef.push({k: 'Jet de parade', v: this.ba.par});
			this.cdef.push({k: 'Jet de réflexe', v: this.ba.ref});
			this.cdef.push({k: 'Jet de stabilisation', v: this.ba.stab});
			this.cdef.push({k: 'Seuil de résistance', v: this.ba.sr});
			this.cdef.push({k: 'Soin', v: (!this.ba.type.includes('Régénération') && !this.ba.type.includes('Vampirisme')) ? this.ba.soin : null});
			this.cdef.push({k: 'Armure', v: this.ba.arm});
			this.cdef.push({k: 'Direction', v: this.dir});
			this.cdef.push({k: 'Gain de RM', v: this.ba.rm});
		}
	}
</script>

<!-- STYLE -->
<style>
	.container-overlay {
	  	position: relative;  
	}

	.overlay {
	  	background: none repeat scroll 0 0;
	  	opacity: 0.8;
		top:0;
	  	left:0;
	  	position: absolute;
		width: 100%;
	}
</style>
