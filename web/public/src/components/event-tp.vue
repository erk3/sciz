<!-- TEMPLATE -->
<template>
	<v-layout row wrap justify-center align-center fill-height pa-4>
		<!-- HEADER -->
		<v-flex xs12 mb-5>
			<h4 class="display-1">Portail de Téléportation</h4>
			<span>de</span>
			<v-avatar>
				<v-img v-if="tp.owner_blason_uri" :src="tp.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{tp.owner_nom}} ({{tp.owner_id}})</span><br/>
		</v-flex>
		<!-- MOB -->
		<v-flex xs12 text-xs-center mb-5>
			<v-layout row align-center justify-center fill-height>
				<v-flex xs4>
					<v-img :src="Image('portal')" alt="" contain max-height="100px"></v-img>
					<br/>({{tp.portail_id}})
				</v-flex>
				<v-flex offset-xs1 xs4>
					<div>
						<h5 class="title">Position</h5>
						<span> X = {{tp.pos_x}} | Y = {{tp.pos_y}} | N = {{tp.pos_n}}</span>
						<br/><br/>
					</div>
					<div>
						<h5 class="title">Destination</h5>
						<span> X = {{tp.pos_x_dst}} | Y = {{tp.pos_y_dst}} | N = {{tp.pos_n_dst}}</span>
						<br/><br/>
					</div>
					<div>
						<h5 class="title">Dispersion</h5>
						<span> X = {{tp.pos_x_disp}} | Y = {{tp.pos_y_disp}} | N = {{tp.pos_n_disp}}</span>
					</div>
				</v-flex>
			</v-layout>
		</v-flex>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	export default {
		name: 'EventTP',
		props: {
			tp: {
				type: Object,
				default: null
			}
		},
	}
</script>
