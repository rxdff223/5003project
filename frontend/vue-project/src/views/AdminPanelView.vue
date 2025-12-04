<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('data')

// Mock Data for 2.1 City Management
const cities = ref([
  { key: '1', name: 'Shanghai', province: 'Shanghai', lat: 31.23, lon: 121.47 },
  { key: '2', name: 'Beijing', province: 'Beijing', lat: 39.90, lon: 116.40 },
])
const cityColumns = [
  { title: 'City Name', dataIndex: 'name', key: 'name' },
  { title: 'Province', dataIndex: 'province', key: 'province' },
  { title: 'Lat/Lon', key: 'coords' },
  { title: 'Action', key: 'action' },
]

// Mock Data for 2.2 Health Advice
const adviceRules = ref([
  { key: '1', level: 'Mild', target: 'Children', text: 'Reduce outdoor play.' },
  { key: '2', level: 'Severe', target: 'Elderly', text: 'Stay indoors.' },
])
const adviceColumns = [
  { title: 'Pollution Level', dataIndex: 'level', key: 'level' },
  { title: 'Target Group', dataIndex: 'target', key: 'target' },
  { title: 'Suggestion', dataIndex: 'text', key: 'text' },
]
</script>

<template>
  <div class="admin-panel">
    <h2>Administrator Console</h2>

    <a-tabs v-model:activeKey="activeTab">

      <!-- 2.1 Data Management -->
      <a-tab-pane key="data" tab="Data Management">
        <div class="tab-toolbar">
          <a-button type="primary">Sync API Data Now</a-button>
          <a-button>View Sync Logs</a-button>
          <a-button type="dashed" style="margin-left: auto">Add New City</a-button>
        </div>

        <a-table :dataSource="cities" :columns="cityColumns">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'coords'">
              {{ record.lat }}, {{ record.lon }}
            </template>
            <template v-if="column.key === 'action'">
              <a>Edit</a> | <a style="color: red">Delete</a>
            </template>
          </template>
        </a-table>
      </a-tab-pane>

      <!-- 2.2 Health Advice Management -->
      <a-tab-pane key="advice" tab="Health Advice">
        <a-button type="dashed" style="margin-bottom: 16px">Add New Rule</a-button>
        <a-table :dataSource="adviceRules" :columns="adviceColumns" />
      </a-tab-pane>

      <!-- 2.3 System Monitoring -->
      <a-tab-pane key="monitor" tab="System Monitoring">
        <a-row :gutter="16">
          <a-col :span="8">
             <a-statistic title="Active Users Today" :value="11289" style="margin-right: 50px" />
          </a-col>
          <a-col :span="8">
             <a-statistic title="API Sync Success Rate" :value="98.5" suffix="%" />
          </a-col>
        </a-row>
        <!-- Sync Chart would go here -->
      </a-tab-pane>

    </a-tabs>
  </div>
</template>

<style scoped>
.tab-toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}
</style>
