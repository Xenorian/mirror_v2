<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <suspense>
    <router-view class="page"/>
  </suspense>
</template>

<style scoped>
    .page{
      min-height: 600px;
      min-width: 1700px;
    }
</style>
 