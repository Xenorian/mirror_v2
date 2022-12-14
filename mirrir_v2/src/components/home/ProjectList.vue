<template>
        <el-table 
          :data="filterTableData" 
          style="width: 100%" 
          highlight-current-row
          @selection-change="handleSelectionChange"
          @current-change="handleCurrentChange"
          >
        <el-table-column type="selection" width="55" />
        <el-table-column label="Repository" prop="name" />
        <el-table-column label="上次更新时间" prop="date" />
        <el-table-column align="right">
        <template #header>

          <el-row>
              <el-col :span="19">
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

          <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
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

    const multipleSelection = ref<User[]>([])

    interface User {
      date: string
      name: string
    }

    const search = ref('')
    
    const handleSelectionChange = (val: User[]) => {
      console.log(val)
      multipleSelection.value = val
    }

    const filterTableData = computed(() =>
    tableData.filter(
        (data) =>
        !search.value ||
        data.name.toLowerCase().includes(search.value.toLowerCase())
    )
    )
    const handleEdit = (index: number, row: User) => {
      console.log(index, row)
    }
    const handleDelete = (index: number, row: User) => {
      console.log(index, row)
    }

    const Compare = () => {
      if(multipleSelection.value.length < 2){
        ElMessageBox.alert('对比项目少于两个', 'Error!', {
          confirmButtonText: 'OK',
        })
      }
      else{
      console.log(multipleSelection.value)
      }
    }

    const tableData: User[] = [
    {
        date: '2022-12-11',
        name: 'Pytorch',
    },
    {
        date: '**',
        name: '**',
    },
    {
        date: '**',
        name: '**',
    },
    {
        date: '**',
        name: '**',
    },
    ]
</script>
  