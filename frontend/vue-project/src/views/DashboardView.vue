<script setup lang="ts">
import FilterBar from '@/components/FilterBar.vue'
import HealthAlertBanner from '@/components/HealthAlertBanner.vue'
import { useDashboardStore } from '@/stores/dashboardData'
import { storeToRefs } from 'pinia'

const store = useDashboardStore()
const { hotSearches } = storeToRefs(store)
</script>

<template>
  <div class="dashboard">
    <!-- 1.2 Filters -->
    <FilterBar />

    <!-- 1.3 Health Advice -->
    <HealthAlertBanner />

    <a-row :gutter="16">
      <!-- LEFT COL: Main Data -->
      <a-col :span="16">
        <!-- 1.2.1 Weather Details -->
        <a-card title="Air Quality Trend (24h Forecast)" style="margin-bottom: 20px">
          <div class="chart-placeholder">
             [Line Chart Area: Integrate ECharts here later]
          </div>
        </a-card>

        <a-card title="Monthly Statistics">
          <div class="chart-placeholder">
             [Bar Chart Area: Compare last 12 months]
          </div>
        </a-card>
      </a-col>

      <!-- RIGHT COL: Hot Searches & Stats -->
      <a-col :span="8">
        <!-- 1.4 Hot Searches -->
        <a-card title="Trending Cities" size="small">
          <a-list item-layout="horizontal" :data-source="hotSearches">
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta :description="`${item.visits} searches today`">
                  <template #title>
                    <span class="rank">#{{ item.rank }}</span> {{ item.city }}
                  </template>
                </a-list-item-meta>
              </a-list-item>
            </template>
          </a-list>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.chart-placeholder {
  height: 200px;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  border: 1px dashed #ccc;
}
.rank {
  font-weight: bold;
  color: #faad14;
  margin-right: 8px;
}
</style>
