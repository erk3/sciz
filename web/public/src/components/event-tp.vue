<!-- TEMPLATE -->
<template>
	<v-row justify="center" align="center" class="fill-height ma-4">
		<!-- HEADER -->
		<v-col class="col-12 mb-5 text-center">
			<h4 class="display-1">Portail de Téléportation</h4>
			<span>de</span>
			<v-avatar>
				<v-img v-if="tp.owner_blason_uri" :src="tp.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{tp.owner_nom}} ({{tp.owner_id}})</span><br/>
		</v-col>
		<!-- MOB -->
		<v-col class="col-12 text-center">
			<v-row justify="center" align="center" class="fill-height">
				<v-col class="col-4">
					<v-img :src="Image('portal')" alt="" contain max-height="100px"></v-img>
					<br/>({{tp.portail_id}})
				</v-col>
				<v-col class="col-4 offset-1">
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
				</v-col>
			</v-row>
		</v-col>
	</v-row>
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
