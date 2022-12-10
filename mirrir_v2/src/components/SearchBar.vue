<template>
    <div class="mt-4">
        <el-input v-model="inputsearch" placeholder="Please input" class="input-with-select">
            <template #append>
                <el-button :icon="Search" @click="onsearch"/>
            </template>
        </el-input>
    </div>
</template>


<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
const inputsearch = ref('')
const onsearch = () => {
    console.log("search: "+inputsearch)
}

</script>