<template>
    <div v-for="(project , index) in data.val" class="pro">
        <div class="left">
            <Title :index="index" class="title" />
            <Overview :index="index" class="overview" />
        </div>

        <div class="right">
            <Language :index="index"/>
        </div>
    </div>
</template>


<script setup lang="ts">
    import * as echarts from 'echarts';
    import Title from './DashBoard/Title.vue'
    import Overview from './DashBoard/Overview.vue'
    import Language from './DashBoard/Language.vue'
    import { ref ,onMounted  } from 'vue'
    import { repoDataStore } from '@/stores/repoData'

    const data = repoDataStore();
</script>

<style scoped>
    .left{
        float: left;
        width: 800px;
        height: 100%;
        margin-left: 50px;
    }

    .overview{
        max-width: 600px;
    }

    .right{
        margin-left: 900px;
    }

    .pro{
        height: 700px;
        width: 1600px;
    }
</style>