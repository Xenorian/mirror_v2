<template>
  <div id="linechart"></div>
</template>


<script setup>
import * as echarts from 'echarts';
import { ref, onMounted } from 'vue'
import { repoDataStore } from '@/stores/repoData'

const data = repoDataStore();

onMounted(() => {
  var chartDom = document.getElementById('linechart');
  var myChart = echarts.init(chartDom);
  var option;

  function run(_rawData,series) {
    // var countries = ['Australia', 'Canada', 'China', 'Cuba', 'Finland', 'France', 'Germany', 'Iceland', 'India', 'Japan', 'North Korea', 'South Korea', 'New Zealand', 'Norway', 'Poland', 'Russia', 'Turkey', 'United Kingdom', 'United States'];
    const countries = series;
    const datasetWithFilters = [];
    const seriesList = [];
    echarts.util.each(countries, function (country) {
      var datasetId = 'dataset_' + country;
      datasetWithFilters.push({
        id: datasetId,
        fromDatasetId: 'dataset_raw',
        transform: {
          type: 'filter',
          config: {
            and: [
              { dimension: 'Country', '=': country }
            ]
          }
        }
      });
      seriesList.push({
        type: 'line',
        datasetId: datasetId,
        showSymbol: false,
        name: country,
        endLabel: {
          show: true,
          formatter: function (params) {
            return params.value[1];
          }
        },
        labelLayout: {
          moveOverlap: 'shiftY'
        },
        emphasis: {
          focus: 'series'
        },
        encode: {
          x: 'Year',
          y: 'Commit',
          label: ['Country', 'Commit'],
          itemName: 'Year',
          tooltip: ['Commit']
        }
      });
    });
    option = {
      animationDuration: 500,
      dataset: [
        {
          id: 'dataset_raw',
          source: _rawData
        },
        ...datasetWithFilters
      ],
      title: {
        text: 'Total Pull Request',
        left: '300'
      },
      tooltip: {
        order: 'valueDesc',
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        nameLocation: 'middle'
      },
      yAxis: {
        name: 'Pull Request'
      },
      grid: {
        right: 140
      },
      dataZoom: [
        {
          type: 'inside',
          start: 50,
          end: 100
        },
        {
          show: true,
          type: 'slider',
          top: '93%',
          start: 50,
          end: 100
        }
      ],
      series: seriesList
    };
    myChart.setOption(option);
  }

  let series = []

  let _rawData = [];
  _rawData[0]=data.val[0].prActivity[0];

  let counter = [];
  let sum_counter = 0;
  let choosen_val = 0;
  let sum = [];
  let date_now = "0000-00-00 00:00:00"
  let date_this_turn = "0000-00-00 00:00:00"

  for(let i=0;i<data.val.length;i++){
    counter[i]= 1 ;
    sum[i] = 0;
    series.push(data.val[i].basicData.repo)
  }

  // compare the top
  while(1){
    let exit=false;
    for(let i=0;i<data.val.length;i++){
      if(data.val[i].prActivity.length == counter[i]){
        console.log("finish one!")
        if(i==data.val.length - 1){
          exit = true;
        }

        continue;
      }else{
        date_this_turn = data.val[i].prActivity[counter[i]][2];
        choosen_val = i;
      }
    }

    // if(exit==true || sum_counter >= sum_all - 4)

    if(exit==true){
      break;
    }

    for(let i=0;i<data.val.length;i++){
      if(data.val[i].prActivity.length == counter[i] ){
        continue;
      }

      if(data.val[i].prActivity[counter[i]][2]<date_this_turn &&
        data.val[i].prActivity[counter[i]][2]>date_now){
          choosen_val = i;
          date_this_turn = data.val[i].prActivity[counter[i]][2]
      }
    }
    if(date_now == date_this_turn){
      console.log("error")
    } else {
      
    }
    date_now = date_this_turn;
    
    // add data into chart
    for(let i=0;i<data.val.length;i++){
      if(data.val[i].prActivity.length == counter[i] ){
        continue;
      }

      if(data.val[i].prActivity[counter[i]][2] === date_now){
        _rawData[_rawData.length]= JSON.parse(JSON.stringify(data.val[i].prActivity[counter[i]]))
        sum[i] += _rawData[_rawData.length-1][0];
        _rawData[_rawData.length-1][0] = sum[i];

        sum_counter++;
        counter[i]++;
      } else {
        _rawData[_rawData.length] = JSON.parse(JSON.stringify(data.val[i].prActivity[counter[i]]))
        _rawData[_rawData.length-1][0] = sum[i];
        _rawData[_rawData.length-1][2] = date_now;
      }
    }
  }

  // for(let i=0;i<data.val.length;i++){

  //   for(let j=1;j<data.val[i].prActivity.length;j++){
  //     _rawData[_rawData.length]= JSON.parse(JSON.stringify(data.val[i].prActivity[j]))
  //     sum[i] += Number(_rawData[_rawData.length-1][0]);
  //     _rawData[_rawData.length-1][0] = sum[i];
  //   }
  // }


  console.log(_rawData,series)
  run(_rawData,series)

  option && myChart.setOption(option);
})

</script>