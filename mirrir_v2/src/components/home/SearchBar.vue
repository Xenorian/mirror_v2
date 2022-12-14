<template>
    <div class="mt-4">
        <el-input v-model="inputsearch" 
            placeholder="Please input {owner}/{repo}" 
            class="input-with-select">
            <template #append>
                <el-button :icon="Plus" @click="onsearch"/>
            </template>
        </el-input>
    </div>
</template>


<script setup lang="ts">
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const inputsearch = ref('')
const onsearch = () => {
    alert('项目已添加')
    console.log(inputsearch.value)
}

</script>