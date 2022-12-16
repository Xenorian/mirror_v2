<template>
        <el-table 
          :data="filterTableData" 
          style="width: 100%" 
          highlight-current-row
          @selection-change="handleSelectionChange"
          >
        <el-table-column type="selection" width="55" />
        <el-table-column label="Repository" prop="name" />
        <el-table-column label="Owner" prop="owner" />
        <el-table-column label="上次更新时间" prop="date" />
        <el-table-column align="right">
        <template #header>

          <el-row :gutter="27" >
              <el-col :span="17">
                <el-input v-model="search" 
                  size="small" 
                  placeholder="Type to search" />
              </el-col>

              <el-col :span="5">
                <el-button 
                  size="small" 
                  type="primary"
                  @click="Compare"
                  >进入对比</el-button
                >
              </el-col>
          </el-row>

        </template>


        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
            >更新缓存</el-button
          >

          <el-button size="small" 
            type="primary"
            @click="handleWatch(scope.$index, scope.row)"
            >查看项目</el-button
          >

          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            >删除项目</el-button
          >

          
        </template>
      </el-table-column>
    </el-table>
  </template>
  
<script lang="ts" setup>
    import { computed, ref } from 'vue'
    import { ElTable, ElMessage, ElMessageBox } from 'element-plus'
    import { repoDataStore } from '@/stores/repoData'
    import { useRouter } from "vue-router";

    const data = repoDataStore();
    const router = useRouter();

    const multipleSelection = ref<User[]>([])

    interface User {
      date: string
      name: string
      owner: string
    }

    const search = ref('')
    const tableData: User[] = [];

    for(let i=0;i<data.repoList.length;i++){
      tableData[i]={};
      tableData[i].date=data.repoList[i].update
      tableData[i].name=data.repoList[i].repo
      tableData[i].owner=data.repoList[i].owner
    }
    
    const handleSelectionChange = (val: User[]) => {
      multipleSelection.value = val
      data.clearData();

      for(let i=0;i<val.length;i++){
        data.addRepo(val[i].owner,val[i].name)
      }

      console.log(data.repos)
    }

    const filterTableData = computed(() =>
    tableData.filter(
        (data) =>
        !search.value ||
        data.name.toLowerCase().includes(search.value.toLowerCase())
    )
    )
    const handleEdit = (index: number, row: User) => {
      data.addRepo(row.owner,row.name)
    }

    const handleWatch = async(index: number, row: User) => {
      await data.addRepo(row.owner,row.name)
      await data.addData();
      router.replace('/chart')
    }
    
    const handleDelete = (index: number, row: User) => {
      data.addRepo(row.owner,row.name)
    }

    const Compare = async() => {
      if(multipleSelection.value.length < 2){
        ElMessageBox.alert('对比项目少于两个', 'Error!', {
          confirmButtonText: 'OK',
        })
      }
      else{
        await data.addData();
        router.replace('/chart');
      }
    }
</script>
  