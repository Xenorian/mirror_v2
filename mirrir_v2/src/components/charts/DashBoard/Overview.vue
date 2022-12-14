<template>
    <div>
        <div class="container">
            <div class="a">
                Overview
            </div>

            <div class="content">
                {{list[0]}}
            </div>

            <div class="data">
                {{data.val[0].basicData.stars}}
            </div>

            <div class="content">
                {{list[1]}}
            </div>

            <div class="data">
                {{data.val[0].basicData.pulls}}
            </div>

            <div class="content">
                {{list[2]}}
            </div>

            <div class="data">
                {{data.val[0].basicData.issues}}
            </div>

            <div class="content">
                {{list[3]}}
            </div>

            <div class="data">
                {{data.val[0].basicData.forks}}
            </div>

            <div class="content">
                {{list[4]}}
            </div>

            <div class="data">
                ****
            </div>

            <div class="content">
                {{list[5]}}
            </div>

            <div class="data">
                ****
            </div>

            <div class="tag">
                Tag
            </div>
        </div>

        <div class="tag_data">
            <div v-for="(item,i) in tag_content" class="tag_content">
                {{item}}
            </div>
        </div>    
    </div>
</template>


<script setup lang="ts">
    import * as echarts from 'echarts';
    import { ref,onMounted  } from 'vue'
    import { repoDataStore } from '@/stores/repoData'

    const data = repoDataStore();

    const list = ref(['Stars','Commits','Issues','Forks','Watchers','PR creators']);
    
    const tag_content = data.val[0].basicData.topic;
</script>

<style scoped>
    .container {  
        display: grid;
        grid-template-columns: 2fr 3fr;
        grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
        gap: 10px 15px;
        grid-auto-flow: row;
        grid-template-areas:
            "a a"
            ". ."
            ". ."
            ". ."
            ". ."
            ". ."
            ". ."
            "tag tag";
        width: 300px; 
        height: 350px; 
    }

    .content{
        background-color: #a9d2e0;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 700;
        line-height: 38px;
    }

    .data{
        background-color: #c4dee7;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 700;
        line-height: 38px;
    }

    .a{
        grid-area: a;
        font-size: 20px;
        font-weight: 500;
    }

    .tag{
        background-color: #98d8ee;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 700;
        line-height: 38px;
        grid-area: tag;
    }

    .tag_data {
        margin-top: 50px;
        display: grid; 
        grid-template-columns: 1fr 1fr 1fr 1fr 1fr; 
        grid-template-rows: 1fr 1fr; 
        gap: 10px 15px; 
        grid-template-areas: 
            ". . . . ."
            ". . . . ."; 
        width: 750px; 
        height: 100px; 
    }

    .tag_content{
        background-color: #c4f0ff;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 700;
        line-height: 38px;
    }

</style>