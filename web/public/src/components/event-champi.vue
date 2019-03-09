<!-- TEMPLATE -->
<template>
	<v-layout row wrap justify-center align-center fill-height pa-4>
		<!-- HEADER -->
		<v-flex xs12 mb-5>
			<h4 class="display-1">{{ce.type}}</h4>
			<span>de</span>
			<v-avatar>
				<v-img v-if="ce.owner_blason_uri" :src="ce.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{ce.owner_nom}} ({{ce.owner_id}})</span><br/>
		</v-flex>
		<!-- MOB -->
		<v-flex xs12 text-xs-center mb-5>
			<v-layout row align-center justify-center fill-height>
				<v-flex xs4>
					<v-img :src="Image('mushroom')" alt="" contain max-height="100px"></v-img>
					<br/>{{ce.nom}} ({{ce.champi_id}})
					<v-btn v-bind:href="ce.champi_link" v-bind:class="{'ma-0': true}" icon target="_blank">
						<v-icon size="14px">fas fa-link</v-icon>
					</v-btn>
				</v-flex>
				<v-flex offset-xs1 xs4 v-if="ce.qualite || ce.pos_x">
					<div v-if="ce.qualite">
						<h5 class="title">Qualité</h5>
						<span>{{ce.qualite}}</span>
						<br/><br/>
					</div>
					<div v-if="ce.pos_x">
						<h5 class="title">Position</h5>
						<span v-if="ce.pos_n"> X = {{ce.pos_x}} | Y = {{ce.pos_y}} | N = {{ce.pos_n}}</span>
						<span v-else> X = {{ce.pos_x}} | Y = {{ce.pos_y}}</span>
					</div>
				</v-flex>
			</v-layout>
		</v-flex>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	export default {
		name: 'EventChampi',
		props: {
			ce: {
				type: Object,
				default: null
			}
		},
	}
</script>
