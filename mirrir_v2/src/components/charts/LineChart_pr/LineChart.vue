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
        name: 'Commit'
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

  for(let i=0;i<data.val.length;i++){
    series.push(data.val[i].basicData.repo)
    let sum=0;
    for(let j=1;j<data.val[i].prActivity.length;j++){
      _rawData[_rawData.length]= JSON.parse(JSON.stringify(data.val[i].prActivity[j]))
      sum += _rawData[_rawData.length-1][0];
      _rawData[_rawData.length-1][0] = sum;
    }
  }

  run(_rawData,series)

  option && myChart.setOption(option);
})

</script>