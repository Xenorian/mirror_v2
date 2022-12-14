<template>
    <div class="part1">
        <img :src="avatar">

        <div class="title">
            <h1>
                {{title}}
            </h1>
        </div>

        <div class="description">
            {{des}}
        </div>
    </div>
</template>


<script setup lang="ts">
    import { ref  } from 'vue'
    const avatar = ref('https://avatars.githubusercontent.com/u/21003710?v=4')
    const title = ref('Pytorch/Pytorch')
    const des = ref('Tensors and Dynamic neural networks in Python with strong GPU acceleration')
    
</script>

<style scoped>
    .part1{
        display: grid; 
        grid-template-columns: 1fr 3fr 1fr; 
        grid-template-rows: 1fr 1fr; 
        gap: 10px 15px; 
        grid-template-areas: 
            ". . ."
            "description description description"; 
        width: 800px; 
        height: 200px; 
    }

    .part1 img{
        height: 100px;
    }

    .title{
        font-size: 60px;
    }

    .description{
        grid-area: description;
        margin-left: 20px;
        text-align: left;
        font-size: 18px;
    }
</style>