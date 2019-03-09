<!-- TEMPLATE -->
<template>
	<v-layout justify-center align-start fill-height id="bestiary-view" class='mt-5'>
		<v-snackbar v-model="info" color="info" :timeout="6000" top>
	  	{{ info_msg }}
	    <v-btn dark flat @click="info = false">Fermer</v-btn>
	  </v-snackbar>
<v-flex xs6 text-xs-center>
			<v-autocomplete v-model="search" :items="mobsList" item-text="nom" item-value="nom" chips hide-no-data cache-items :menu-props="{'closeOnContentClick': true}" no-data-text="Aucun monstre dans le bestiaire..." v-on:change="makeRequest" :filter="mobFilter" :hint="'Le bestiaire compte actuellement ' + nbCDM + ' connaissances des monstres partagées par la communauté !'" persistent-hint placeholder="Rechercher un monstre..." label="Recherchez un monstre !">
				<template slot="selection" slot-scope="data">
					<v-chip close @input="search=''; result=''">
						<v-avatar>
							<v-img :src="data.item.blason_uri" v-if="data.item.blason_uri" @error="data.item.blason_uri=Image('unknown')" alt="" contain></v-img>
							<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
						</v-avatar>
						{{ data.item.nom }}
					</v-chip>
				</template>
				<template slot="item" slot-scope="data">
					<v-list-tile-avatar>
						<v-img :src="data.item.blason_uri" v-if="data.item.blason_uri" @error="data.item.blason_uri=Image('unknown')" alt="" contain></v-img>
						<v-img v-else :src="Image('unknown')" alt="" contain></v-img>
					</v-list-tile-avatar>
					<v-list-tile-content>
						<v-list-tile-title> {{ data.item.nom }} </v-list-tile-title>
					</v-list-tile-content>
				</template>
			</v-autocomplete>
      <v-card tile class="ma-5 pa-3" v-if="result">
				<pre>{{ result }}</pre>
				<br/>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn v-clipboard:copy="result" @click="info_msg = 'CdM copiée dans le presse-papier'; info = true;">Copier</v-btn>
					<v-spacer></v-spacer>
				</v-card-actions>
			</v-card>
    </v-flex>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	
	import { getMobs, getnbCDM, request } from '~/src/api.js';

	export default {
    name: 'BestiaryView',
 		data: () => ({
			search: '',
			result: '',
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
								if (i < l - 1) {
									this.result += "\n-\n"
								}
							}
						}
					})
			},
		}
	}
</script>
