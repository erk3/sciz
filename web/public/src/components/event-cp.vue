<!-- TEMPLATE -->
<template>
	<v-row justify="center" align="center" class="fill-height ma-4">
		<!-- HEADER -->
		<v-col class="col-12 mb-5 text-center">
			<h4 class="display-1">Construire un Piège</h4>
			<span>de</span>
			<v-avatar>
				<v-img v-if="cp.owner_blason_uri" :src="cp.owner_blason_uri" :lazy-src="Image('unknown')" alt="" contain max-height="30px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain max-height="30px"></v-img>
			</v-avatar>
			<span>{{cp.owner_nom}} ({{cp.owner_id}})</span><br/>
		</v-col>
		<!-- MOB -->
		<v-col class="col-12 text-center">
			<v-row justify="center" align="center" class="fill-height">
				<v-col class="col-4">
					<v-img :src="Image('trap')" alt="" contain max-height="100px"></v-img>
					<br/>({{cp.piege_id}})
				</v-col>
				<v-col class="col-4 offset-1">
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
				</v-col>
			</v-row>
		</v-col>
		<!-- DATA -->
		<v-col class="col-12 text-center">
			<v-row justify="center" align="center" class="fill-height">
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
				</v-col>
			</v-row>
		</v-col>
	</v-row>
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
