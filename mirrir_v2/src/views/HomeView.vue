<script setup lang="ts">
import SearchBar from '../components/home/SearchBar.vue'
import Hello from '../components/home/helloSection.vue'
import List from '../components/home/ProjectList.vue'
import { repoDataStore } from '@/stores/repoData'

const m_repoData = repoDataStore();
await m_repoData.getRepoList();
</script>

<template>
  <Hello class="banner" />
  <SearchBar class="searchBar"/>
  <List class="list"/>
</template>

<style scoped>
.banner {
  max-height: 400px;
}

.searchBar{
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.list{
  max-width: 1400px;
  margin-top: 100px;
  margin-left: auto;
  margin-right: auto;
}
</style>