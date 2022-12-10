<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import SearchBar from './components/SearchBar.vue'
import Hello from './components/helloSection.vue'
</script>

<template>
  <Hello class="banner" />
  <SearchBar class="searchBar"/>
</template>

<style scoped>
.banner {
  max-height: 400px;
}

.searchBar{
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}
</style>
