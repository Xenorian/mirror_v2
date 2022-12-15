<template>
    <SumChart class="sumchart"/>
    <Columnchart  class="columnchart"/>
</template>

<script lang="ts" setup>
import SumChart from './LineChart_issue/LineChart.vue'
import Columnchart from './LineChart_issue/ColumnChart.vue'
</script>

<style scoped>
.sumchart{
    margin-top: 50px;
    height: 600px;
    width: 800px;
    float: left;
}

.columnchart{
    margin-top: 50px;
    margin-left: 820px;
    height: 600px;
    width: 800px;
}
</style>