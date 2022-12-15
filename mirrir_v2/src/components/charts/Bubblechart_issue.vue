<template>
	<div class="left">
        <div id="bubble" style="height: 650px; width: 800px;"> </div>
    </div>

    <div class="right">
        <CompanyList id="bubblelist"/>
    </div>
	
</template>


<script setup>
	import CompanyList from './BubbleChart/CompanyList.vue'
</script>

<script>
import {ref} from 'vue'
import Highcharts from 'highcharts/highstock';
import HighchartsMore from 'highcharts/highcharts-more';
import { repoDataStore } from '@/stores/repoData'

const data = repoDataStore();

HighchartsMore(Highcharts)

export default {
	data() {
		return {
			chart: null,
			bubbledata: [],
		}
	},

	mounted() {
		for(let i=0;i<data.val.length;i++){
			this.bubbledata.push({});
			this.bubbledata[i].data = data.val[i].bubbledata
			this.bubbledata[i].name = data.val[i].basicData.repo
		}
		
		this.initchart()
	},


	methods: {
		initchart() {
			Highcharts.chart('bubble', {
				chart: {
					type: 'packedbubble',
					// height: '50%'
				},
				title: {
					text: "Commit Contributors' Companies",
					margin: 0
				},
				tooltip: {
					useHTML: true,
					pointFormat: '<b>{point.name}:</b> {point.y}'
				},
				plotOptions: {
					packedbubble: {
						useSimulation: false,
						Draggable: false,
						minSize: '20%',
						maxSize: '700%',
						zMin: 0,
						zMax: 1000,
						layoutAlgorithm: {
							splitSeries: true,
							gravitationalConstant: 0.01
						},
						dataLabels: {
							enabled: true,
							format: '{point.name}',
							filter: {
								property: 'y',
								operator: '>',
								value: 1
							},
							style: {
								color: 'black',
								textOutline: 'none',
								fontWeight: 'normal'
							}
						}
					}
				},
				series: this.bubbledata
			})
		}

	}

}



</script>

<style scoped>
#bubble {
	margin-top: 50px;
	float: left;
}

#bubblelist{
	width: 500px;
	float: left;
}

.left{
	margin-left: 100px;
	float: left;
	width: 800px;
	height: 100%;
}

.right{
	margin-top: 50px;
	margin-left: 1000px;
	height: 600px;
}
</style>