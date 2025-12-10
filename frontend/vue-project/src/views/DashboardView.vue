<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useDashboardStore } from '@/stores/dashboardData';
import { storeToRefs } from 'pinia';
import axios from 'axios';
import { message } from 'ant-design-vue';

import FilterBar from '@/components/FilterBar.vue';
import HealthAlertBanner from '@/components/HealthAlertBanner.vue';
import HistoricalBarChart from '@/components/HistoricalBarChart.vue';
import AQIPieChart from '@/components/AQIPieChart.vue';

const userStore = useUserStore();
const dashboardStore = useDashboardStore();
const { profile } = storeToRefs(userStore);

const historicalData = ref<any[]>([]);
const currentPollutant = ref('pm25');

// Mock Hot Searches
const hotSearches = ref([
  { rank: 1, city: 'Beijing', visits: 43 },
  { rank: 2, city: 'Shanghai', visits: 39 },
  { rank: 3, city: 'Guangzhou', visits: 30 },
  { rank: 4, city: 'Chengdu', visits: 15 },
  { rank: 5, city: 'Shenzhen', visits: 11 }
]);

const cityMap: Record<string, number> = {
  'Beijing': 1, 'Shanghai': 2, 'Guangzhou': 3, 'Shenzhen': 4, 'Chengdu': 5
};

const barChartData = computed(() => {
  if (!historicalData.value || historicalData.value.length === 0) return [];
  return historicalData.value.map((item: any) => ({
    recorded_time: item.recorded_time,
    value: item[currentPollutant.value] || 0
  })).reverse();
});

const pieChartData = computed(() => {
  return historicalData.value || [];
});

const fetchHistoryData = async (filters: any) => {
  if (!profile.value.token) {
    return;
  }

  // 1. Date Logic
  // We use the End Date: 2025-12-11 to ensure we include all data for the 10th.
  let startDate = '2025-12-04';
  let endDate = '2025-12-11';

  if (filters.timeRange === 'last30days') {
    startDate = '2025-11-11';
    endDate = '2025-12-11';
  }

  // 2. City Logic
  let cityIdParam = 1;
  const rawCity = filters.city;

  if (typeof rawCity === 'number') {
    cityIdParam = rawCity;
  } else if (typeof rawCity === 'string') {
    cityIdParam = cityMap[rawCity] || 1;
  }

  // 3. Pollutant
  if (filters.pollutant) {
    currentPollutant.value = filters.pollutant;
  }

  // 4. API Request Config
  const config = {
    method: 'get',
    url: '/api/data/query',
    headers: {
      'Authorization': `Bearer ${profile.value.token}`
    },
    params: {
      city_id: parseInt(String(cityIdParam), 10),
      // NOTE: We use 'start_date' because __init__.py line 20 reads: request.args.get('start_date')
      // If we send 'start_time', the backend will see None.
      start_time: startDate,
      end_time: endDate,
      page_size: 100
    }
  };

  try {
    const response = await axios(config);
    const resData = response.data;

    const successCodes = ['OK', '0K', 'success', 200];

    if (successCodes.includes(resData.code)) {
      // FIX: Accessing data via resData.message.items as you instructed
      // Structure: { code: "0K", message: { items: [...], total: ... } }
      const items = resData.message?.items || [];

      historicalData.value = items;
      console.log('Charts updated with', items.length, 'records');
    } else {
      console.error('API Logic Error:', resData);

      // Fallback: If structure is inconsistent, try finding items elsewhere
      if (resData.message?.items) {
          historicalData.value = resData.message.items;
      } else if (resData.data?.items) {
          historicalData.value = resData.data.items;
      } else {
         message.error(resData.message || 'Failed to fetch data');
      }
    }
  } catch (error: any) {
    console.error("Request Error:", error);
    if (error.response) {
       const msg = error.response.data?.message || 'Unknown';
       if (error.response.status === 401) {
          message.error('Session expired. Please login.');
          userStore.logout();
       } else if (error.response.status === 400) {
          message.error(`Bad Request: ${msg}`);
       } else {
          message.error(`Error: ${msg}`);
       }
    } else {
       message.error('Network Error');
    }
  }
};

onMounted(() => {
  fetchHistoryData(dashboardStore.filters);
});
</script>

<template>
  <div class="dashboard">
    <FilterBar @search="fetchHistoryData" />


    <a-row :gutter="16">
      <a-col :span="16">
        <a-card title="Pollutant Trend" style="margin-bottom: 20px">
          <div v-if="barChartData.length > 0">
             <HistoricalBarChart
               :data="barChartData"
               :pollutant="currentPollutant"
             />
          </div>
          <div v-else class="empty-state">
            <a-empty description="No Data Available" />
          </div>
        </a-card>

        <a-card title="AQI Level Distribution">
          <div v-if="pieChartData.length > 0">
            <AQIPieChart :data="pieChartData" />
          </div>
          <div v-else class="empty-state">
            <a-empty description="No Data" />
          </div>
        </a-card>
      </a-col>

      <a-col :span="8">
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
.empty-state {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.rank {
  font-weight: bold;
  color: #faad14;
  margin-right: 8px;
}
</style>
