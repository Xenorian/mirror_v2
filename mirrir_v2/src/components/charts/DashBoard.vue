<template>
    <div class="left">
        <Title class="title" />
        <Overview class="overview" />
    </div>

    <div class="right">
        <div id="chart" />
    </div>
</template>


<script setup lang="ts">
    import * as echarts from 'echarts';
    import Title from './DashBoard/Title.vue'
    import Overview from './DashBoard/Overview.vue'
    import { ref ,onMounted  } from 'vue'
    import { repoDataStore } from '@/stores/repoData'

    const data = repoDataStore();
    console.log(data.val[0].basicData.language_detail)

    onMounted(() => {
        var myChart = echarts.init(document.getElementById('chart')!);
        myChart.setOption({
            title: {
                text: 'Languages'
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
                data: data.val[0].basicData.language_detail
                }
            ]
        });
    })
</script>

<style scoped>
    .left{
        margin-left: 50px;
        float: left;
        width: 800px;
        height: 100%;
    }
    .title{
        margin-top: 10px;
    }

    .overview{
        max-width: 600px;
    }

    .right{
        margin-top: 50px;
        margin-left: 900px;
    }

    #chart{
        height: 700px;
        width: 400px;
    }
</style>