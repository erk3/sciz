<!-- TEMPLATE -->
<template>
	<v-layout justify-center align-start fill-height id="aviary-view" class='mt-5'>
		<v-flex xs6 text-xs-center>
      <v-card flat tile class="transparent">
				<v-alert :value="true" type="warning" class="mb-4" outline> La guichet est en cours d'aménagement !</v-alert>
				<v-text-field label="Effectuer une requête auprès du guichet..." v-model="search" prepend-icon="fas fa-filter" @click:prepend="sheet = true;" append-outer-icon="fas fa-arrow-circle-right" @click:append-outer="makeRequest" @blur="reverseGenerateSearch" @keyup.native.enter="makeRequest" hint="<a href='http://mountypedia.mountyhall.com/Outils/SCIZ'>Comment ça marche ?</a>" persistent-hint></v-text-field>
				<pre class="ma-5">{{result}}</pre>
      </v-card>
    </v-flex>
		<!-- BOTTOM BAR -->
		<v-bottom-sheet v-model="sheet">
			<v-card class="pa-5">
				<v-layout row justify-space-around fill-height>
					<!-- POS_X -->
					<v-flex xs2>
						<v-layout row wrap justify-center fill-height>
							<v-flex xs2>
								<v-layout row wrap justify-end fill-height>
									<v-checkbox v-model="b_pos_x" hide-details @change="generateSearch"></v-checkbox>
								</v-layout>
							</v-flex>
							<v-flex xs10>
								<v-range-slider label="X" single-line always-dirty thumb-label="always" :min="-150" :max="150" v-model="pos_x" :disabled="!b_pos_x" @change="generateSearch"></v-range-slider>
							</v-flex>
						</v-layout>
					</v-flex>
					<!-- POS_Y -->
					<v-flex xs2>
						<v-layout row wrap justify-center fill-height>
							<v-flex xs2>
								<v-layout row wrap justify-end fill-height>
									<v-checkbox v-model="b_pos_y" hide-details @change="generateSearch"></v-checkbox>
								</v-layout>
							</v-flex>
							<v-flex xs10>
								<v-range-slider label="Y" single-line always-dirty thumb-label="always" :min="-150" :max="150" v-model="pos_y" :disabled="!b_pos_y" @change="generateSearch"></v-range-slider>
							</v-flex>
						</v-layout>
					</v-flex>
					<!-- POS_N -->
					<v-flex xs2>
						<v-layout row wrap justify-center fill-height>
							<v-flex xs2>
								<v-layout row wrap justify-end fill-height>
									<v-checkbox v-model="b_pos_n" hide-details @change="generateSearch"></v-checkbox>
								</v-layout>
							</v-flex>
							<v-flex xs10>
								<v-range-slider label="N" single-line always-dirty thumb-label="always" :min="-150" :max="0" v-model="pos_n" :disabled="!b_pos_n" @change="generateSearch"></v-range-slider>
							</v-flex>
						</v-layout>
					</v-flex>
					<!-- Niveau -->
					<v-flex xs2>
						<v-layout row wrap justify-center fill-height>
							<v-flex xs2>
								<v-layout row wrap justify-end fill-height>
									<v-checkbox v-model="b_niveau" hide-details @change="generateSearch"></v-checkbox>
								</v-layout>
							</v-flex>
							<v-flex xs10>
								<v-range-slider label="Niveau" single-line always-dirty thumb-label="always" :min="1" :max="60" v-model="niveau" :disabled="!b_niveau" @change="generateSearch"></v-range-slider>
							</v-flex>
						</v-layout>
					</v-flex>
				</v-layout>
				<v-layout row justify-space-around fill-height>
					<!-- ID -->
					<v-flex xs3>
						<v-layout row wrap justify-center fill-height>
							<v-flex xs2>
								<v-layout row wrap justify-end fill-height>
									<v-checkbox v-model="b_id" hide-details @change="generateSearch"></v-checkbox>
								</v-layout>
							</v-flex>
							<v-flex xs10>
								<v-text-field label="Identifiants" placeholder="104126,54367821..." v-model="id" :disabled="!b_id" @change="generateSearch"></v-text-field>
							</v-flex>
						</v-layout>
					</v-flex>
					<!-- Select -->
					<v-flex xs3>
						<v-layout row wrap justify-center fill-height>
							<v-flex xs2>
								<v-layout row justify-end fill-height>
									<v-checkbox v-model="b_res" hide-details @change="generateSearch"></v-checkbox>
								</v-layout>
							</v-flex>
							<v-flex xs10>
								<v-slider label="Nombre de résultats" single-line always-dirty thumb-label="always" :min="1" :max="10" v-model="res" :disabled="!b_res" @change="generateSearch"></v-slider>
							</v-flex>
						</v-layout>
					</v-flex>
					<!-- Coterie -->
					<v-flex xs3>
						<v-layout row wrap justify-center fill-height>
							<v-flex xs12>
								<v-checkbox v-model="b_coterie" label="Filtrer sur les trolls de la coterie" @change="generateSearch"></v-checkbox>
							</v-flex>
						</v-layout>
					</v-flex>
				</v-layout>
				<v-layout row wrap justify-space-around align-center fill-height>
					<v-flex xs4>
						<v-layout column align-space-around justify-space-around fill-height>
							<!-- Troll -->
							<v-layout row wrap justify-center fill-height>
								<v-flex xs2>
									<v-layout row wrap justify-end fill-height>
										<v-checkbox v-model="b_troll" hide-details @change="generateSearch"></v-checkbox>
									</v-layout>
								</v-flex>
								<v-flex xs10>
									<v-text-field label="Troll" placeholder="Nom, race..." v-model="troll" :disabled="!b_troll" @change="generateSearch"></v-text-field>
								</v-flex>
							</v-layout>
							<!-- Monstre -->
							<v-layout row wrap justify-center fill-height>
								<v-flex xs2>
									<v-layout row wrap justify-end fill-height>
										<v-checkbox v-model="b_mob" hide-details @change="generateSearch"></v-checkbox>
									</v-layout>
								</v-flex>
								<v-flex xs10>
									<v-text-field label="Monstre" placeholder="Nom, race, templates, age, tag..." v-model="mob" :disabled="!b_mob" @change="generateSearch"></v-text-field>
								</v-flex>
							</v-layout>
							<!-- Tresor -->
							<v-layout row wrap justify-center fill-height>
								<v-flex xs2>
									<v-layout row wrap justify-end fill-height>
										<v-checkbox v-model="b_tresor" hide-details @change="generateSearch"></v-checkbox>
									</v-layout>
								</v-flex>
								<v-flex xs10>
									<v-text-field label="Trésor" placeholder="Nom, type, templates, effet..." v-model="tresor" :disabled="!b_tresor" @change="generateSearch"></v-text-field>
								</v-flex>
							</v-layout>
							<!-- Champi -->
							<v-layout row wrap fill-height>
								<v-flex xs2>
									<v-layout row wrap justify-end fill-height>
										<v-checkbox v-model="b_champi" hide-details @change="generateSearch"></v-checkbox>
									</v-layout>
								</v-flex>
								<v-flex xs10>
									<v-text-field label="Champignon" placeholder="Nom, qualité..." v-model="champi" :disabled="!b_champi" @change="generateSearch"></v-text-field>
								</v-flex>
							</v-layout>
						</v-layout>
					</v-flex>
					<v-flex xs4>
						<v-layout column align-space-around justify-space-around fill-height>
							<!-- Recap -->
							<v-layout row wrap justify-center fill-height>
								<v-flex xs2>
									<v-layout row wrap justify-end fill-height>
										<v-checkbox v-model="b_recap" hide-details @change="generateSearch"></v-checkbox>
									</v-layout>
								</v-flex>
								<v-flex xs10>
									<v-text-field label="Récapitulatif de bataille" placeholder="Nom, race, templates, age, tag..." v-model="recap" :disabled="!b_recap" @change="generateSearch"></v-text-field>
								</v-flex>
							</v-layout>
							<!-- Bestiaire -->
							<v-layout row wrap justify-center fill-height>
								<v-flex xs2>
									<v-layout row wrap justify-end fill-height>
										<v-checkbox v-model="b_bestiaire" hide-details @change="generateSearch"></v-checkbox>
									</v-layout>
								</v-flex>
								<v-flex xs10>
									<v-text-field label="Bestiaire" placeholder="Nom, race, templates, age, tag..." v-model="bestiaire" :disabled="!b_bestiaire" @change="generateSearch"></v-text-field>
								</v-flex>
							</v-layout>
							<!-- Recherche -->
							<v-layout row wrap justify-center fill-height>
								<v-flex xs2>
									<v-layout row wrap justify-end fill-height>
										<v-checkbox v-model="b_recherche" hide-details @change="generateSearch"></v-checkbox>
									</v-layout>
								</v-flex>
								<v-flex xs10>
									<v-text-field label="Localiser un monstre" placeholder="Nom, race, templates, age, tag..." v-model="recherche" :disabled="!b_recherche" @change="generateSearch"></v-text-field>
								</v-flex>
							</v-layout>
							<!-- Lieu -->
							<v-layout row wrap justify-center fill-height>
								<v-flex xs2>
									<v-layout row wrap justify-end fill-height>
										<v-checkbox v-model="b_lieu" hide-details @change="generateSearch"></v-checkbox>
									</v-layout>
								</v-flex>
								<v-flex xs10>
									<v-text-field label="Lieu" placeholder="Nom..." v-model="lieu" :disabled="!b_lieu" @change="generateSearch"></v-text-field>
								</v-flex>
							</v-layout>
						</v-layout>
					</v-flex>
				</v-layout>
				<!-- Filtres -->
				<v-layout row wrap justify-center fill-height>
					<v-flex xs8>
						<v-layout row justify-center fill-height>
							<v-flex xs2>
								<v-layout row wrap justify-end fill-height>
									<v-checkbox v-model="b_filtre" hide-details @change="generateSearch"></v-checkbox>
								</v-layout>
							</v-flex>
							<v-flex xs10>
								<v-text-field label="Filtres sur le résultat" placeholder="att,esq,pos,dla..." v-model="filtre" :disabled="!b_filtre" @change="generateSearch"></v-text-field>
							</v-flex>
						</v-layout>
					</v-flex>
				</v-layout>
			</v-card>
		</v-bottom-sheet>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>
	
	import { request } from '~/src/api.js';

	export default {
    name: 'AviaryView',
 		data: () => ({
			search: '',
			result:'',
			sheet: false,
			b_troll: false,
			troll: '',
			b_mob: false,
			mob: '',
			b_tresor: false,
			tresor: '',
			b_champi: false,
			champi: '',
			b_lieu: false,
			lieu: '',
			b_recap: false,
			recap: '',
			b_bestiaire: false,
			bestiaire: '',
			b_recherche: false,
			recherche: '',
			b_pos_x: false,
			pos_x: [-10, 10],
			b_pos_y: false,
			pos_y: [-10, 10],
			b_pos_n: false,
			pos_n: [-10, 0],
			b_niveau: false,
			niveau: [1, 60],
			b_coterie: false,
			b_id: false,
			id: '',
			b_res: false,
			res: 1,
			b_filtre: false,
			filtre: '',
		}),
		methods: {
			makeRequest() {
				request({'req': this.search})
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
			reverseGenerateSearch() {
				// FIXME
			},
			generateSearch() {
				this.search = '';
				if (this.b_troll) {
					this.search += ' %troll'
					if (this.troll != '') {
						this.search += ':' + this.troll
					}
				}
				if (this.b_mob) {
					this.search += ' %mob'
					if (this.mob != '') {
						this.search += ':' + this.mob
					}
				}
				if (this.b_tresor) {
					this.search += ' %tresor'
					if (this.tresor != '') {
						this.search += ':' + this.tresor
					}
				}
				if (this.b_champi) {
					this.search += ' %champi'
					if (this.champi != '') {
						this.search += ':' + this.champi
					}
				}
				if (this.b_lieu) {
					this.search += ' %lieu'
					if (this.lieu != '') {
						this.search += ':' + this.lieu
					}
				}
				if (this.b_recap) {
					this.search += ' %recap'
					if (this.recap != '') {
						this.search += ':' + this.recap
					}
				}
				if (this.b_recherche) {
					this.search += ' %recherche'
					if (this.recherche != '') {
						this.search += ':' + this.recherche
					}
				}
				if (this.b_filtre) {
					this.search += ' %filtre'
					if (this.filtre != '') {
						this.search += ':' + this.filtre
					}
				}
				if (this.b_coterie) {
					this.search += ' %coterie'
				}
				if (this.b_id) {
					this.search += ' %id'
					if (this.id != '') {
						this.search += ':' + this.id
					}
				}
				if (this.b_res && this.res > 1) {
					this.search += ' %select:' + this.res
				}
				if (this.b_niv) {
					if (this.niv[0] != this.niv[1]) {
						this.search += ' %niv:' + this.niv.join('_')
					} else {
						this.search += ' %niv:' + this.niv[0]
					}
				}
				if (this.b_pos_x) {
					if (this.pos_x[0] != this.pos_x[1]) {
						this.search += ' %pos_x:' + this.pos_x.join('_')
					} else {
						this.search += ' %pos_x:' + this.pos_x[0]
					}
				}
				if (this.b_pos_y) {
					if (this.pos_y[0] != this.pos_y[1]) {
						this.search += ' %pos_y:' + this.pos_y.join('_')
					} else {
						this.search += ' %pos_y:' + this.pos_y[0]
					}
				}
				if (this.b_pos_n) {
					if (this.pos_n[0] != this.pos_n[1]) {
						this.search += ' %pos_n:' + this.pos_n.join('_')
					} else {
						this.search += ' %pos_n:' + this.pos_n[0]
					}
				}
			},
		}
	}
</script>
