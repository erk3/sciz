<!-- TEMPLATE -->
<template>
	<v-layout row wrap justify-center align-center fill-height pa-4>
		<!-- HEADER -->
		<v-flex xs12 mb-5>
			<h4 class="display-1">{{te.type}}</h4>
			<span>de</span>
			<v-avatar>
				<v-img v-if="te.owner_blason_uri" :src="te.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{te.owner_nom}} ({{te.owner_id}})</span><br/>
		</v-flex>
		<!-- MOB -->
		<v-flex xs12 text-xs-center mb-5>
			<v-layout row align-center justify-center fill-height>
				<v-flex xs4>
					<v-img :src="Image('treasure')" alt="" contain max-height="100px"></v-img>
					<br/>{{te.tresor_nom}} ({{te.tresor_id}})
					<v-btn v-bind:href="te.tresor_link" v-bind:class="{'ma-0': true}" icon target="_blank">
						<v-icon size="14px">fas fa-link</v-icon>
					</v-btn>
				</v-flex>
				<v-flex offset-xs1 xs4 v-if="te.effet || te.pos_x">
					<div v-if="te.effet">
						<h5 class="title" v-if="te.tresor_nom === 'Mission'">Numéro</h5>
						<h5 class="title" v-else-if="te.tresor_nom === 'Tête Réduite'">Monstre</h5>
						<h5 class="title" v-else-if="te.tresor_nom === 'Potion de Pàïntûré'">Niveau</h5>
						<h5 class="title" v-else-if="te.tresor_type === 'Coquillage'">Sonorité</h5>
						<h5 class="title" v-else-if="te.tresor_type === 'Carte'">Lieu</h5>
						<h5 class="title" v-else>Effet</h5>
						<span>{{te.effet}}</span>
						<br/><br/>
					</div>
					<div v-if="te.pos_x">
						<h5 class="title">Position</h5>
						<span v-if="te.pos_n"> X = {{te.pos_x}} | Y = {{te.pos_y}} | N = {{te.pos_n}}</span>
						<span v-else> X = {{te.pos_x}} | Y = {{te.pos_y}}</span>
					</div>
				</v-flex>
			</v-layout>
		</v-flex>
		<!-- DATA -->
		<v-flex xs12 text-xs-center v-if="!te.type.startsWith('Télékinésie')">
			<v-layout row align-start justify-center fill-height>
				<v-flex xs4 text-xs-center>
					<v-card flat>
		      	<v-divider></v-divider>
						<v-list v-for="carac in cnum" dense class="pa-0">
							<v-list-tile>
								<v-list-tile-content>{{carac.k}}</v-list-tile-content>
								<v-list-tile-content class="align-end">
									<v-tooltip v-if="carac.t" right>
										<div slot="activator" class="text-capitalize">{{carac.v}}</div>
										<span>{{carac.t}}</span>
									</v-tooltip>
									<span v-else class="text-capitalize">{{carac.v}}</span>
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
		name: 'EventTresor',
		props: {
			te: {
				type: Object,
				default: null
			}
		},
		data() {
			return {
				cnum: [],
			}
		},
		beforeMount() {
			// Caractéristiques numériques
			this.cnum.push({k: 'Type', v: this.te.tresor_type ? this.te.tresor_type : '-'})
		}
	}
</script>
