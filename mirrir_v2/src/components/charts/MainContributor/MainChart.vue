<template>
    <div id="mainchart"></div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue'
import * as echarts from 'echarts';
import { repoDataStore } from '@/stores/repoData'


const data = repoDataStore();

let type_to_int = new Map();
type_to_int.set('pulls',0)
type_to_int.set('issue',1)
type_to_int.set('commit',2)
type_to_int.set('review',3)
let type_activate = [1,1,1,1];

let totaldata = [];
let userdata = data.val[0].userData
console.log(userdata)
let i = 0;
for (i = 0; i < userdata.length; i++) {
    totaldata.push([userdata[i].login, userdata[i].pulls, userdata[i].issues, userdata[i].commit, userdata[i].reviews])
}
console.log(totaldata)

totaldata.sort(function(a,b){
    let a_sum = 0;
    let b_sum = 0;
    for(let i=1;i<=4;i++){
        a_sum+=a[i] * type_activate[i-1];
        b_sum+=b[i] * type_activate[i-1];
    }
    
    if(a_sum>b_sum){
        return 1;
    }else if(a_sum<b_sum){
        return -1;
    }else {
        return 0;
    }
})

onMounted(() => {
    var chartDom = document.getElementById('mainchart')!;
    var myChart = echarts.init(chartDom);
    var option;
    option = {
        dataset: [{
            dimensions:['name', 'pulls', 'issue', 'commit','review'],
            source: totaldata,
        },
        {
            transform: {
                type: 'sort',
                config: { dimension: 'commit', order: 'asc' }
            }
        }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                // Use axis to trigger tooltip
                type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
            }
        },
        legend: {},
        grid: {
            left: '3%',
            right: '8%',
            bottom: '8%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
        },
        yAxis: {
            type: 'category',
        },
        dataZoom: [
            {
                type: 'inside',
                show: true,
                yAxisIndex: 0,
                filterMode: 'empty',
                width: 30,
                height: '85%',
                showDataShadow: false,
                left: '95%',
                endValue: totaldata.length,
                startValue: totaldata.length - 15,
                moveOnMouseWheel: true,
                zoomOnMouseWheel: false,
            },
            {
                type: 'slider',
                show: true,
                yAxisIndex: 0,
                filterMode: 'empty',
                width: 30,
                height: '85%',
                showDataShadow: false,
                left: '95%',
            }
        ],
        series: [{
            type: 'bar',
            stack: 'total',
            emphasis: {
                focus: 'series'
            },
        }, {
            type: 'bar',
            stack: 'total',
            emphasis: {
                focus: 'series'
            },
        }, {
            type: 'bar',
            stack: 'total',
            emphasis: {
                focus: 'series'
            },
        },{
            type: 'bar',
            stack: 'total',
            emphasis: {
                focus: 'series'
            },
        }]
    };
    myChart.on('legendselectchanged', (e) => {
        console.log(type_activate)
        if(type_activate[type_to_int.get(e.name)] === 1){
            type_activate[type_to_int.get(e.name)] = 0
        } else {
            type_activate[type_to_int.get(e.name)] = 1
        }

        totaldata.sort(function(a,b){
            let a_sum = 0;
            let b_sum = 0;

            for(let i=1;i<=4;i++){
                a_sum+=a[i] * type_activate[i-1];
                b_sum+=b[i] * type_activate[i-1];
            }
            
            if(a_sum>b_sum){
                return 1;
            }else if(a_sum<b_sum){
                return -1;
            }else {
                return 0;
            }

        })
        
        var chartDom = document.getElementById('mainchart')!;
        var myChart = echarts.init(chartDom);
        option && myChart.setOption(option);
    })
    option && myChart.setOption(option);
})
</script>

<style>

</style>