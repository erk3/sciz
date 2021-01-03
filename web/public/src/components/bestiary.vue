<!-- TEMPLATE -->
<template>
	<v-container class="mt-5 fill-height" id="bestiary-view">
		<!-- NOTIFICATIONS -->
		<v-snackbar v-model="info" color="info" :timeout="6000" top>
			{{ info_msg }}
			<template v-slot:action="{ attrs }">
				<v-btn dark text @click="info = false" v-bind="attrs">Fermer</v-btn>
			</template>
		</v-snackbar>
		<!-- BESTIARY -->
		<v-row wrap justify="center" align="start">
			<v-col class="col-6 text-center">
				<v-autocomplete v-model="search" :items="mobsList" item-text="nom" item-value="nom" chips hide-no-data cache-items :menu-props="{'closeOnContentClick': true}" no-data-text="Aucun monstre dans le bestiaire..." v-on:change="makeRequest" :filter="mobFilter" :hint="'Le bestiaire compte actuellement ' + nbCDM + ' connaissances des monstres partagées par la communauté !'" persistent-hint placeholder="Rechercher un monstre..." label="Recherchez un monstre !">
					<template slot="selection" slot-scope="data">
						<v-chip close close-icon="far fa-times-circle" @click:close="search=''; result=''; blason=''">
							<v-avatar>
								<v-img :src="data.item.blason_uri" v-if="data.item.blason_uri" @error="data.item.blason_uri=Image('unknown')" alt="" contain></v-img>
								<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
							</v-avatar>
							{{ data.item.nom }}
						</v-chip>
					</template>
					<template slot="item" slot-scope="data">
						<v-list-tile-avatar>
							<v-img :src="data.item.blason_uri" v-if="data.item.blason_uri" @error="data.item.blason_uri=Image('unknown')" alt="" contain max-width="30px"></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
						</v-list-tile-avatar>
						<v-list-tile-content>
							<v-list-tile-title> {{ data.item.nom }} </v-list-tile-title>
						</v-list-tile-content>
					</template>
				</v-autocomplete>
			</v-col>
		</v-row>
		<v-row wrap justify="center" align="center" class="fill-height">
			<v-col class="col-4 text-center d-none d-md-flex" v-if="blason">
				<v-img :src="blason" v-if="blason" @error="blason=Image('unknown')" alt="" contain max-height="300px"></v-img>
				<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
			</v-col>
			<v-col class="col-6 text-center">
				<v-card tile class="ma-5 pa-3" v-if="result">
					<pre>{{ result }}</pre>
					<br/>
					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn color="primary" v-clipboard:copy="result" @click="info_msg = 'CdM copiée dans le presse-papier'; info = true;">Copier</v-btn>
						<v-spacer></v-spacer>
					</v-card-actions>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<!-- SCRIPT -->
<script>
import { getMobs, getnbCDM, request } from '~/src/api.js';
export default {
	name: 'BestiaryView',
	data: () => ({
		search: '',
		result: '',
		blason: '',
		mobsList: [],
		nbCDM: 0,
		info: false,
		info_msg: '',
	}),
	beforeMount() {
		getMobs()
			.then(res => {
				if (res.status === 200) {
					this.mobsList = res.data;
				}
			});
		getnbCDM()
			.then(res => {
				if (res.status === 200) {
					this.nbCDM = res.data;
				}
			});
	},
	methods: {
		mobFilter (item, queryText, itemText) {
			const text = item.nom.normalize('NFD').replace(/[\u0300-\u036f]/g, "").toLowerCase();
			const searchText = queryText.normalize('NFD').replace(/[\u0300-\u036f]/g, "").toLowerCase();
			var keywords = searchText.split(' ');
			return keywords.every((search) => {return text.indexOf(search) > -1});
		},	
		makeRequest() {
			request({'req': '%bestiaire:' + this.search.replace(/[\[\]]+/g, '').normalize('NFD').replace(/[\u0300-\u036f]/g, "").replace(/(\s|\W)+/g, ',')})
				.then(res => {
					if (res.status === 200 && res.data) {
						this.result = '';
						var l = res.data['message'].length;
						for (var i = 0; i < l; i++) {
							this.result += res.data['message'][i];
						}
						this.blason = "" + this.result.match(/Blason\s*:\s*(.*)/)[1];
						this.result = this.result.replace(/Blason.*|,$/gi, "");
					}
				})
		},
	}
}
</script>
