<template>
    <div :id="graph_id" style="height: 700px;
        width: 400px;" />
</template>


<script setup lang="ts">
    import * as echarts from 'echarts';
    import { ref ,onMounted  } from 'vue'
    import { repoDataStore } from '@/stores/repoData'

    const data = repoDataStore();
    const props = defineProps(['index'])
    const graph_id = data.val[props.index].basicData.repo

    onMounted(() => {
        var myChart = echarts.init(document.getElementById(graph_id)!);
        myChart.setOption({
            title: {
                text: 'Languages',
                top: '5%',
            },
            tooltip: {
                trigger: 'item',
                formatter: function(params){
                    return (params.value*100).toFixed(2)+'%'
                }
            },
            legend: {
                top: '15%',
                left: 'center'
                },
            series: [
                {
                name: 'Language',
                type: 'pie',
                radius: ['60%', '80%'],
                center: ['50%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center',
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 30,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: data.val[props.index].basicData.language_detail
                }
            ]
        });
    })
</script>