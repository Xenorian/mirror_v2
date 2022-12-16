<template>
    <div class="mt-4">
        <el-row :gutter="6">
            <el-col :span="23" style="margin:10px ">
                添加项目
            </el-col>

            <el-col :span="12">
                <el-input v-model="owner" 
                    placeholder="Please input {owner}" 
                    class="input-with-select">
                </el-input>
            </el-col>

            <el-col :span="12">
                <el-input v-model="repo" 
                    placeholder="Please input {repo}" 
                    class="input-with-select">
                    <template #append>
                        <el-button :icon="Plus" @click="onsearch"/>
                    </template>
                </el-input>
            </el-col>
    </el-row>
    </div>
</template>


<script setup lang="ts">
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { repoDataStore } from '@/stores/repoData'

const data = repoDataStore();

const owner = ref('')
const repo = ref('')

const onsearch = () => {
    if(owner.value.length > 0 && repo.value.length > 0){
        data.addNewRepo(owner.value,repo.value)
        alert('项目已开始添加，等通知吧')
    }else{
        alert('还没输全呢')
    }
}

</script>