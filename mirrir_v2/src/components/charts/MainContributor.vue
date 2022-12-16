<template>
    <div v-for="(project , index) in data.val" class="pro">
        <MainChart :index="index"/>
    </div>
</template>

<script lang="ts" setup>
    import MainChart from './MainContributor/MainChart.vue'
    import { repoDataStore } from '@/stores/repoData'

    const data = repoDataStore();
</script>

<style>

</style>