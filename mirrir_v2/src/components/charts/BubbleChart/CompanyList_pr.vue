<template>
    <el-row :gutter="10">
        <el-col :span="10">
            <el-input v-model="listsearch" 
            size="small" 
            placeholder="Type to search"/>
        </el-col>
    </el-row>
    
    <el-row :gutter="10">
        <el-table class ="table" :data="filterTableData" height="600"
        :default-sort="{ prop: 'value', order: 'descending' }">
            <el-table-column label="Company" prop="name" width="300"/>
            <el-table-column label="Num" prop="value" width="200" sortable/>
        </el-table>
    </el-row>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { repoDataStore } from '@/stores/repoData'

const data = repoDataStore();

interface Comp_info {
    name: string
    value: number
}
const listsearch = ref('')
const tableData: Comp_info[] = data.val[0].bubbledata_pr
tableData.sort((a,b)=>{
    if(a.value<b.value){
        return 1
    }else if(a.value>b.value){
        return -1
    }else{
        return 0
    }
})
const filterTableData = computed(() =>
    tableData.filter(
        (data) =>
            !listsearch.value ||
            data.name.toLowerCase().includes(listsearch.value.toLowerCase())
    )
)


</script>

<style  scoped>
.table{
    margin-top: 20px;
    max-height: 90%;
    max-width: 100%;
    text-align: left;
}
</style>