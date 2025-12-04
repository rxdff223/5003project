<script setup lang="ts">
import { useDashboardStore } from '@/stores/dashboardData'
import { storeToRefs } from 'pinia'

const store = useDashboardStore()
const { filters } = storeToRefs(store)

const handleSearch = () => {
  store.fetchData()
}
</script>

<template>
  <a-space class="filter-bar">
    <a-select v-model:value="filters.city" style="width: 120px" @change="handleSearch">
      <a-select-option value="Beijing">Beijing</a-select-option>
      <a-select-option value="Shanghai">Shanghai</a-select-option>
      <a-select-option value="London">London</a-select-option>
    </a-select>

    <a-select v-model:value="filters.timeRange" style="width: 150px" @change="handleSearch">
      <a-select-option value="last7days">Last 7 Days</a-select-option>
      <a-select-option value="last30days">Last 30 Days</a-select-option>
    </a-select>

    <a-radio-group v-model:value="filters.pollutant" button-style="solid" @change="handleSearch">
      <a-radio-button value="pm25">PM2.5</a-radio-button>
      <a-radio-button value="pm10">PM10</a-radio-button>
      <a-radio-button value="no2">NO2</a-radio-button>
    </a-radio-group>
  </a-space>
</template>

<style scoped>
.filter-bar {
  margin-bottom: 20px;
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  width: 100%;
}
</style>
