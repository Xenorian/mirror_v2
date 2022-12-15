<template>
  <div id="columnchart"></div>
</template>

<script lang="ts" setup>
import * as echarts from 'echarts';
import { ref, onMounted } from 'vue'
import { repoDataStore } from '@/stores/repoData'

const data = repoDataStore();

const xdata = []

let date_now = "0000-00-00 00:00:00"
let date_this_turn = "0000-00-00 00:00:00"
let counter = [];
let choosen_val = 0;
let legend_item = [];
let chartdata = [{}]

// get x axis
// init counter and legend
for(let i=0;i<data.val.length;i++){
  counter[i] = 1;
  legend_item[i] = data.val[i].basicData.repo;
  chartdata[i].name = data.val[i].basicData.repo;
  chartdata[i].type = 'bar';
  chartdata[i].data = [];
}

// compare the top
while(1){
  date_this_turn = data.val[0].commitActivity[counter[0]][2];
  choosen_val = 0;
  for(let i=1;i<data.val.length;i++){
    if(data.val[i].commitActivity[counter[i]][2]<date_this_turn &&
      data.val[i].commitActivity[counter[i]][2]>date_now){
        choosen_val = i;
        date_this_turn = data.val[i].commitActivity[counter[i]][2]
    }
  }
  date_now = date_this_turn;
  
  // add data into chart
  for(let i=0;i<data.val.length;i++){
    if(data.val[i].commitActivity[counter[i]][2] === date_now){
      chartdata[i].data.push(data.val[i].commitActivity[counter[i]][0])
      counter[i]++;
    }
  }

  xdata[xdata.length] = date_now;

  let i=0;
  for(i=0;i<data.val.length;i++){
    if(counter[i]!==data.val[i].commitActivity.length - 1){
      break;
    }
  }

  if(i===data.val.length){
    console.log("success");
    break;
  }
}





onMounted(()=>{
  var chartDom = document.getElementById('columnchart')!;

  var myChart = echarts.init(chartDom);

  var option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
        label: {
          show: true
        }
      }
    },
    toolbox: {
      show: true,
      feature: {
        mark: { show: true },
        dataView: { show: true, readOnly: false },
        magicType: { show: true, type: ['line', 'bar'] },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    calculable: true,
    title: {
      text: 'Commit Per Day',
    },
    legend: {
      data: legend_item,
      itemGap: 5
    },
    grid: {
      top: '12%',
      left: '1%',
      right: '10%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: xdata
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: 'value',
      }
    ],
    dataZoom: [
      {
        show: true,
        start: 0,
        end: 100
      },
      {
        type: 'inside',
        start: 94,
        end: 100
      },
      {
        show: true,
        yAxisIndex: 0,
        filterMode: 'empty',
        width: 30,
        height: '75%',
        showDataShadow: false,
        left: '93%'
      }
    ],
    series: chartdata
  };
  myChart.setOption(option);
  option && myChart.setOption(option);
})


</script>
