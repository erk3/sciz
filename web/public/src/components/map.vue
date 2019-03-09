<!-- TEMPLATE -->
<template>
	<v-layout row justify-center align-center fill-height id="map-view" pa-3>
		<v-navigation-drawer app permanent floating :width="45" v-if="loaded && !error_map">
			<v-layout align-center justify-center fill-height>
				<v-flex>
					<v-layout column align-center justify-center fill-height>
						<!-- BOTTOM FILTERS -->
						<v-tooltip right>
							<v-bottom-sheet slot="activator" v-model="filters">
								<v-btn slot="activator" icon @click=''><v-icon :size="16">fas fa-filter</v-icon></v-btn>
								<v-card class="pa-5">
									<v-layout row wrap justify-center align-center fill-height>
      							<v-flex xs12 md4 text-xs-center pr-3 pl-3>
							        <v-layout row align-center justify-center fill-height wrap>
							          <v-flex xs12>
													<span class="title">Afficher les éléments :</span><br/><br/>
							      			<v-slider :label="'A une portée de ' + portee + ' case(s)'" single-line always-dirty thumb-label="always":min="1" :max="user.portee" v-model="portee"></v-slider>
												</v-flex>
							          <v-flex xs12>
							      			<v-slider :label="'Vu il y a moins de ' + days + ' jour(s)'" single-line always-dirty thumb-label="always":min="1" :max="10" v-model="days"></v-slider>
							        	</v-flex>
  							      </v-layout>
							      </v-flex>
										<v-flex xs12 offset-md1 md4 text-xs-center pa-3>
											<v-layout row align-center justify-center fill-height wrap>
							          <v-flex xs12>
													<span class="title">Centrer sur :</span><br/><br/>
													<v-select :items="trolls" item-value="id" item-text="nom" item-avatar="blason_uri" v-model="selectedTrollID" v-on:input="centerOnTroll(selectedTrollID)">
							  						<template slot="selection" slot-scope="data">
						    							<v-list-tile-avatar>
																<v-img v-if="data.item.blason_uri" :lazy-src="Image('unknown')" :src="data.item.blason_uri" contain></v-img>
																<v-img v-else :src="Image('unknown')" contain></v-img>
							    						</v-list-tile-avatar>
							    						<v-list-tile-content>
																<v-list-tile-title>{{data.item.nom}} ({{data.item.id}})</v-list-tile-title>
							    						</v-list-tile-content>
													  </template>
						  							<template slot="item" slot-scope="data">
						    							<v-list-tile-avatar>
																<v-img v-if="data.item.blason_uri" :lazy-src="Image('unknown')" :src="data.item.blason_uri" contain></v-img>
																<v-img v-else :src="Image('unknown')" contain></v-img>
							    						</v-list-tile-avatar>
							    						<v-list-tile-content>
																<v-list-tile-title>{{data.item.nom}} ({{data.item.id}})</v-list-tile-title>
						    							</v-list-tile-content>
							  						</template>
													</v-select>
												</v-flex>
												<v-flex xs12>
							      			<v-layout row align-center justify-center fill-height wrap>
							          		<v-flex xs3><v-text-field class="mb-2" type="number" label="X = " v-model="pos_x"></v-text-field></v-flex>
							          		<v-flex offset-xs1 xs3><v-text-field class="mb-2" type="number" label="Y = " v-model="pos_y"></v-text-field></v-flex>
							          		<v-flex offset-xs1 xs3><v-text-field class="mb-2" type="number" label="N = " v-model="pos_n"></v-text-field></v-flex>
													</v-layout>
							        	</v-flex>
											</v-layout>
							      </v-flex>
							      <v-flex xs12 text-xs-center>
											<v-btn color="primary" @click="reloadChart()" @keyup.native.enter="reloadChart()">Rafraichir</v-btn>
										</v-flex>
							    </v-layout>
								</v-card>
    					</v-bottom-sheet>
			     		<span>Filtres</span>
			  		</v-tooltip>
						<!-- LEGENDS -->
						<v-tooltip right>
							<v-btn slot="activator" icon @click='centerMap()'><v-img :src="Image('user-map-icon')" class="ma-2" contain aspect-ratio="1"></v-img></v-btn>
							<span>Re-centrer sur X = {{pos_x}} | Y = {{pos_y}} | N = {{pos_n}}</span>
						</v-tooltip>
						<v-tooltip right>
							<v-btn slot="activator" icon @click='toggleDataset(1)' :class="{pressed: loaded && !$data.datasets[1].hidden}">
								<v-img :src="Image('troll-map-icon')" class="ma-2" contain aspect-ratio="1"></v-img>
							</v-btn>
			      	<span>Trolls</span>
			    	</v-tooltip>
						<v-tooltip right>
							<v-btn slot="activator" icon @click='toggleDataset(2)' :class="{pressed: loaded && !$data.datasets[2].hidden}">
								<v-img :src="Image('follower-map-icon')" class="ma-2" contain aspect-ratio="1"></v-img>
							</v-btn>
		      		<span>Suivants</span>
		    		</v-tooltip>
						<v-tooltip right>
							<v-btn slot="activator" icon @click='toggleDataset(3)' :class="{pressed: loaded && !$data.datasets[3].hidden}">
								<v-img :src="Image('monster-map-icon')" class="ma-2" contain aspect-ratio="1"></v-img>
							</v-btn>
			    		<span>Monstres</span>
			  		</v-tooltip>
						<v-tooltip right>
							<v-btn slot="activator" icon @click='toggleDataset(4)' :class="{pressed: loaded && !$data.datasets[4].hidden}">
								<v-img :src="Image('treasure-map-icon')" class="ma-2" contain aspect-ratio="1"></v-img>
							</v-btn>
		      		<span>Trésors</span>
		    		</v-tooltip>
						<v-tooltip right>
							<v-btn slot="activator" icon @click='toggleDataset(5)' :class="{pressed: loaded && !$data.datasets[5].hidden}">
								<v-img :src="Image('mushroom-map-icon')" class="ma-2" contain aspect-ratio="1"></v-img>
							</v-btn>
			    		<span>Champignons</span>
		    		</v-tooltip>
						<v-tooltip right>
							<v-btn slot="activator" icon @click='toggleDataset(6)' :class="{pressed: loaded && !$data.datasets[6].hidden}">
								<v-img :src="Image('place-map-icon')" class="ma-2" contain aspect-ratio="1"></v-img>
							</v-btn>
			     		<span>Lieux</span>
			  		</v-tooltip>
					</v-layout>
				</v-flex>
			</v-layout>
		</v-navigation-drawer>
		<!-- LOADING -->
		<v-flex v-if="!loaded && !error_map" class="text-xs-center">
			<v-progress-circular :size="150" :width="15" indeterminate></v-progress-circular>
		</v-flex>
		<!-- NO MAP -->
     <v-flex xs6 text-xs-center v-if="error_map">
      <v-card flat tile class="transparent">
        <v-img :src="Image('confused')" contain max-height="300px"></v-img>
				<h1 class="display-2 text-uppercase"> Oups ! </h1><br/>
				<h2 class="title"> Aucune carte à afficher pour le moment. </h2><br/>
      </v-card>
    </v-flex>
		<!-- MAP -->
		<v-flex v-if="loaded" d-flex>
			<map-chart
				:chartData="{datasets: datasets}"
				:options="options"
				@hook:mounted="centerMap"
				style="width:100vw"
				aspect-ratio="1"
			>
			</map-chart>
		</v-flex>
	</v-layout>
</template>

<!-- SCRIPT -->
<script>

	import { getMapUser, getMapData, getMapCount } from '~/src/api.js';
	import MapChart from '~/src/components/map-chart.vue'
	
	let activeTooltip = null;

	export default {
    name: 'MapView',
		components: { MapChart },
		data() {
			return {
				loaded: false,
				error_map: false,
				filters: false,
				days: 1,
				pos_x: 0,
				pos_y: 0,
				pos_n: 0,
				portee: 5,
				user: {},
				trolls: [],
				selectedTrollID: this.userData().id,
				datasets: [],
				icons: { user: new Image(), troll: new Image(), follower: new Image(), monster: new Image(), treasure: new Image(), mushroom: new Image(), place: new Image() },
				options: {
					responsive: true,
					aspectRatio: 1,
					maintainAspectRatio: true,
					//animation: false,
					hover: {
						// Fetch data for rendering the tooltips
						onHover: this._.throttle(function(event, elements) {
							if (elements[0]) {
								var d = elements[0].$datalabels.$context.dataset;
								var e = d.data[elements[0]._index];
								if (e.tooltip === undefined || e.tooltip === null) {
									var type = ''
									switch(d.label) {
  									case 'Trõlls': type = 'trolls'; break;
  									case 'Suivants': type = 'followers'; break;
  									case 'Monstres': type = 'monsters'; break;
  									case 'Trésors': type = 'treasures'; break;
  									case 'Champignons': type = 'mushrooms'; break;
  									case 'Lieux': type = 'places'; break;
									  default: type = 'user';
									};
									getMapData(type, d.days, 0, Math.floor(e.x), Math.floor(e.y), this.pos_n).then(res => {
		    						e.tooltip = []
										var n = null;
										var l = null;
										for (var i = 0; i < res.data.length; i++) {
											if (n !== res.data[i].pos_n) {
												l = null;
												n = res.data[i].pos_n;
												e.tooltip.push('');
												e.tooltip.push('N = ' + n);
											}
											if (l !== res.data[i].last_seen_at) {
												l = res.data[i].last_seen_at;
												e.tooltip.push(l);
											}
											e.tooltip.push('   ' + res.data[i].tooltip);
										}
										e.tooltip.push('');
		    						elements[0].$datalabels.$context.chart.tooltip.update(0);
									})
  							}
							}
						}, 100)
					},
					tooltips: {
						mode: 'point',
						displayColors: false,
						// Render a tooltip
						callbacks: {
							title: (items, data) => 'X = ' + Math.floor(items[0].xLabel) + ' | Y = ' + Math.floor(items[0].yLabel),
							label: (item, data) => {
								activeTooltip = item;
								return data.datasets[item.datasetIndex].data[item.index].tooltip;
							},
							footer: () => 'Cliquez sur l\'icône pour copier',
						}
					},
					scales: {
        		xAxes: [{
							position: 'top',
							gridLines: { drawOnChartArea: true },
							ticks: { type: 'linear', min: -100, max: 100, autoSkip: false, stepSize: 1},
						}],
        		yAxes: [{
							gridLines: { drawOnChartArea: true },
							ticks: { type: 'linear', min: -100, max: 100, autoSkip: false, stepSize: 1},
						}],
					},
					legend: {
						display: false,
						labels: { usePointStyle: true }
					},
					plugins: {
						// Scale datalabels on zoom
						datalabels: {
							align: 'bottom',
							offset: function (context) {
								var xl = context.chart.scales['x-axis-1'].max - context.chart.scales['x-axis-1'].min;
								var yl = context.chart.scales['y-axis-1'].max - context.chart.scales['y-axis-1'].min;
								var scaleFactor = Math.min(Math.abs(xl), Math.abs(yl));
								return 100 / scaleFactor;
							},
							font: function(context) {
								var xl = context.chart.scales['x-axis-1'].max - context.chart.scales['x-axis-1'].min;
								var yl = context.chart.scales['y-axis-1'].max - context.chart.scales['y-axis-1'].min;
								var scaleFactor = Math.min(Math.abs(xl), Math.abs(yl));
								var windowRatio = context.chart.width / context.chart.height;
								return { size: (150 / scaleFactor) * windowRatio };
							}
						}
					},
					pan: { enabled: true, mode: 'xy'},
					zoom: { enabled: true, mode: 'xy',
						onZoom: () => {
							var xl = this.$data.chart.scales['x-axis-1'].max - this.$data.chart.scales['x-axis-1'].min;
							var yl = this.$data.chart.scales['y-axis-1'].max - this.$data.chart.scales['y-axis-1'].min;
							var scaleFactor = Math.min(Math.abs(xl), Math.abs(yl));
							// Scale icons on the map
							for (var key in this.icons) {
								var windowRatio = window.innerWidth / (window.innerHeight * 1);
  							this.icons[key].width = (125 / scaleFactor) * windowRatio;
  							this.icons[key].height = (125 / scaleFactor) * windowRatio;
							}
							// Prevent infinite forward zooming
							var scaleFactor_min = 5;
							var scaleFactor_max = 20;
							if (scaleFactor < scaleFactor_min) {
								this.options.scales.xAxes[0].ticks.max = Math.ceil(this.$data.chart.scales['x-axis-1'].max);
								this.options.scales.yAxes[0].ticks.max = Math.ceil(this.$data.chart.scales['y-axis-1'].max);
								this.options.scales.xAxes[0].ticks.min = Math.floor(this.$data.chart.scales['x-axis-1'].min);
								this.options.scales.yAxes[0].ticks.min = Math.floor(this.$data.chart.scales['y-axis-1'].min);
							}
						}
					},
					onResize: (chart, size) => {
						this.centerMap();
					},
					onClick: (evt) => {
						this.$copyText('X = ' + Math.floor(activeTooltip.xLabel) + ' | Y = ' + Math.floor(activeTooltip.yLabel) + '\n' + this.$data.datasets[activeTooltip.datasetIndex].data[activeTooltip.index].tooltip.join('\n'));
					},
				}
			}
		},
		mounted() {
			// Change grid colors depending on user mode
			var gridColor = (this.$store.getters.mode === ('light')) ? 'rgba(0, 0, 0, 0.25)' : 'rgba(255, 255, 255, 0.25)';
			this.options.scales.xAxes[0].gridLines.color = gridColor;
			this.options.scales.yAxes[0].gridLines.color = gridColor;
			var gridColor = (this.$store.getters.mode === ('light')) ? 'rgba(0, 0, 0, 0.5)' : 'rgba(255, 255, 255, 0.5)';
			this.options.scales.xAxes[0].gridLines.zeroLineColor = gridColor;
			this.options.scales.yAxes[0].gridLines.zeroLineColor = gridColor;
			this.options.plugins.datalabels.color = gridColor;
			// Load the icons
			this.icons.user.src = this.Image('user-map-icon');
			this.icons.troll.src = this.Image('troll-map-icon');
			this.icons.follower.src = this.Image('follower-map-icon');
			this.icons.monster.src = this.Image('monster-map-icon');
			this.icons.mushroom.src = this.Image('mushroom-map-icon');
			this.icons.treasure.src = this.Image('treasure-map-icon');
			this.icons.place.src = this.Image('place-map-icon');
			// Load the map data
			this.getAllData(true)
				.then(() => {
					// Scale everything around the user
					if (this.user) {
						this.setCenter(this.pos_x, this.pos_y);
					}
				}).catch(() => {
					this.error_map = true;
				});
		},
		methods: {
			// Reloard chart
			reloadChart() {
				this.filters = false;
				this.loaded = false;
				this.datasets = [];
				this.getAllData(false).then(() => {
					this.setCenter(this.pos_x, this.pos_y);
				});
			},
			// Set a point as center
			setCenter(x, y) {
				var xl = (this.options.scales.xAxes[0].ticks.max - this.options.scales.xAxes[0].ticks.min) / 2;
				var yl = (this.options.scales.yAxes[0].ticks.max - this.options.scales.yAxes[0].ticks.min) / 2;
				var xl = 7;
				var yl = 7;
				var height = window.innerHeight * 0.7; // Because of navbars and legends
				var width = window.innerWidth;
				var yOffset = width > height ? Math.ceil(width / height) : 0;
				var xOffset = height > width ? Math.ceil(height / width) : 0;
				this.options.scales.xAxes[0].ticks.min = parseFloat(x) - xl + xOffset;
				this.options.scales.xAxes[0].ticks.max = parseFloat(x) + xl + xOffset;
				this.options.scales.yAxes[0].ticks.min = parseFloat(y) - yl - yOffset;
				this.options.scales.yAxes[0].ticks.max = parseFloat(y) + yl - yOffset;
			},
			// Select a troll position for future refresh
			centerOnTroll(troll_id) {
				this.trolls.forEach(troll => {
					if (troll.id === troll_id) {
						this.pos_x = troll.pos_x;
						this.pos_y = troll.pos_y;
						this.pos_n = troll.pos_n;
					}
				});
			},
			// Center the map
			centerMap() {
				this.$data.chart.resetZoom();
				this.options.zoom.onZoom();
			},
			// Toggle dataset visibility
			toggleDataset(i) {
				this.datasets[i].hidden = !this.datasets[i].hidden;
			},
			// Generic function for putting items in the datasets (and so on the map)
			createDataSet(res, icon, xOffset, yOffset, label, hidden) {
				var data = []
				for (var i = 0; i < res.data.length; i++) {
					var obj = res.data[i];
					data[i] = { x: obj.pos_x + xOffset, y: obj.pos_y + yOffset, label: obj.count > 1 ? obj.count : ''};
				}
				var dataset = { days: this.days, portee: this.portee, label: label, data: data, pointStyle: icon, pointHitRadius: 5, hidden: hidden };
				this.datasets.push(dataset);
			},
			getAllData(firstload) {
				return getMapUser().then(res => {
					this.trolls = res.data;
					var new_res = [];
					res.data.forEach(troll => {
						if (troll.id === this.userData().id) {
							this.user = troll;
							if (firstload) {
								this.pos_x = this.user.pos_x;
								this.pos_y = this.user.pos_y;
								this.pos_n = this.user.pos_n;
								this.portee = Math.min(this.user.portee, 10);
							}
							new_res.push(troll);
						}
					});
					this.createDataSet({data: new_res}, this.icons.user, 0.5, 0.5, this.userData().nom, false);
					getMapCount('trolls', this.days, this.portee, this.pos_x, this.pos_y, this.pos_n).then(res => {
						this.createDataSet(res, this.icons.troll, 0.25, 0.75, 'Trõlls', false);
						getMapCount('followers', this.days, this.portee, this.pos_x, this.pos_y, this.pos_n).then(res => {
							this.createDataSet(res, this.icons.follower, 0.5, 0.75, 'Suivants', false);
							getMapCount('monsters', this.days, this.portee, this.pos_x, this.pos_y, this.pos_n).then(res => {
								this.createDataSet(res, this.icons.monster, 0.75, 0.75, 'Monstres', false);
								getMapCount('treasures', this.days, this.portee, this.pos_x, this.pos_y, this.pos_n).then(res => {
									this.createDataSet(res, this.icons.treasure, 0.25, 0.25, 'Trésors', false);
										getMapCount('mushrooms', this.days, this.portee, this.pos_x, this.pos_y, this.pos_n).then(res => {
										this.createDataSet(res, this.icons.mushroom, 0.5, 0.25, 'Champignons',false);
											getMapCount('places', this.days, this.portee, this.pos_x, this.pos_y, this.pos_n).then(res => {
												this.createDataSet(res, this.icons.place, 0.75, 0.25, 'Lieux', false);
												this.loaded = true;
											}).catch(()=>{this.error_map = true;})
										}).catch(()=>{this.error_map = true;})
									}).catch(()=>{this.error_map = true;})
								}).catch(()=>{this.error_map = true;})
							}).catch(()=>{this.error_map = true;})
						}).catch(()=>{this.error_map = true;})
					}).catch(()=>{this.error_map = true;});
			}
		}
	}
</script>

<style scoped>
.pressed {
	background-color: rgba(0, 0, 0, 0.2);
}
</style>
