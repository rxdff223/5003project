<script setup lang="ts">
import { useDashboardStore } from '@/stores/dashboardData'
import { storeToRefs } from 'pinia'

// Define the emitted event
const emit = defineEmits<{
  (e: 'search', filters: any): void
}>()

const store = useDashboardStore()
const { filters } = storeToRefs(store)

const handleSearch = () => {

  console.log('FilterBar: Emitting search with', filters.value)

  // Emit a COPY of the value to avoid reference issues
  emit('search', { ...filters.value })
}
</script>

<template>
  <a-space class="filter-bar">
    <span class="label">City:</span>
    <a-select
      v-model:value="filters.city"
      style="width: 120px"
      @change="handleSearch"
      placeholder="Select City"
    >
      <a-select-option :value="1">Beijing</a-select-option>
      <a-select-option :value="2">Shanghai</a-select-option>
      <a-select-option :value="3">Guangzhou</a-select-option>
      <a-select-option :value="4">Shenzhen</a-select-option>
      <a-select-option :value="5">Chengdu</a-select-option>
    </a-select>

    <span class="label">Time:</span>
    <a-select
      v-model:value="filters.timeRange"
      style="width: 150px"
      @change="handleSearch"
    >
      <a-select-option value="last7days">Last 7 Days</a-select-option>
      <a-select-option value="last30days">Last 30 Days</a-select-option>
    </a-select>

    <span class="label">Pollutant:</span>
    <a-radio-group
      v-model:value="filters.pollutant"
      button-style="solid"
      @change="handleSearch"
    >
      <a-radio-button value="pm25">PM2.5</a-radio-button>
      <a-radio-button value="pm10">PM10</a-radio-button>
      <a-radio-button value="no2">NO2</a-radio-button>
      <a-radio-button value="so2">SO2</a-radio-button>
      <a-radio-button value="o3">O3</a-radio-button>
      <a-radio-button value="co">CO</a-radio-button>
    </a-radio-group>
  </a-space>
</template>

<style scoped>
.filter-bar {
  margin-bottom: 20px;
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
.label {
  font-weight: bold;
  margin-right: 4px;
  color: #333;
}
</style>
