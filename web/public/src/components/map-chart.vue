<script>
	import { Scatter, mixins } from 'vue-chartjs'
	import ChartZoomPlugin from 'chartjs-plugin-zoom'
	import ChartDatalabelsPlugin from 'chartjs-plugin-datalabels'

	export default {
		extends: Scatter,
		mixins: [mixins.reactiveProp],
		props: {
			chartData: {
				type: Object,
				default: null
			},
			options: {
				type: Object,
				default: null
			}
		},
		mounted () {
			this.addPlugin(ChartZoomPlugin);
			this.addPlugin(ChartDatalabelsPlugin);
			this.renderChart(this.chartData, this.options);
			this.$parent.$data.chart = this.$data._chart;
		}
	}
</script>
