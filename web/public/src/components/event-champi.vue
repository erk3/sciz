<!-- TEMPLATE -->
<template>
	<v-row justify="center" align="center" class="fill-height ma-4">
		<!-- HEADER -->
		<v-col class="col-12 mb-5 text-center">
			<h4 class="display-1">{{ce.type}}</h4>
			<span>de</span>
			<v-avatar>
				<v-img v-if="ce.owner_blason_uri" :src="ce.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{ce.owner_nom}} ({{ce.owner_id}})</span><br/>
		</v-col>
		<!-- MOB -->
		<v-col class="col-12 text-center">
			<v-row justify="center" align="center" class="fill-height">
				<v-col class="col-4">
					<v-img :src="Image('mushroom')" alt="" contain max-height="100px"></v-img>
					<br/>{{ce.nom}} ({{ce.champi_id}})
					<v-btn v-bind:href="ce.champi_link" v-bind:class="{'ma-0': true}" icon target="_blank">
						<v-icon size="14px">fas fa-link</v-icon>
					</v-btn>
				</v-col>
				<v-col class="col-4 offset-1" v-if="ce.qualite || ce.pos_x">
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
				</v-col>
			</v-row>
		</v-col>
	</v-row>
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
	}
}
</script>
