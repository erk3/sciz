<!-- TEMPLATE -->
<template>
	<v-layout row wrap justify-center align-center fill-height pa-4>
		<!-- HEADER -->
		<v-flex xs12 mb-5>
			<h4 class="display-1">Construire un Piège</h4>
			<span>de</span>
			<v-avatar>
				<v-img v-if="cp.owner_blason_uri" :src="cp.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{cp.owner_nom}} ({{cp.owner_id}})</span><br/>
		</v-flex>
		<!-- MOB -->
		<v-flex xs12 text-xs-center mb-5>
			<v-layout row align-center justify-center fill-height>
				<v-flex xs4>
					<v-img :src="Image('trap')" alt="" contain max-height="100px"></v-img>
					<br/>({{cp.piege_id}})
				</v-flex>
				<v-flex offset-xs1 xs4>
					<div>
						<h5 class="title">Type</h5>
						<span> {{cp.piege_type}}</span>
						<br/><br/>
					</div>
					<div>
						<h5 class="title">Position</h5>
						<span> X = {{cp.pos_x}} | Y = {{cp.pos_y}} | N = {{cp.pos_n}}</span>
						<br/><br/>
					</div>
				</v-flex>
			</v-layout>
		</v-flex>
		<!-- DATA -->
		<v-flex xs12 text-xs-center>
			<v-layout row align-start justify-center fill-height>
				<v-flex xs4 text-xs-center>
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
		name: 'EventCP',
		props: {
			cp: {
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
			this.cnum.push({k: 'Maitrise Magique', v: this.cp.piege_mm})
		}
	}
</script>
