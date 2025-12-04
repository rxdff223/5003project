import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useDashboardStore = defineStore('dashboard', () => {
  // 1.2 Filters
  const filters = ref({
    city: 'Shanghai',
    timeRange: 'last7days', // or 'last30days', 'custom'
    pollutant: 'pm25'
  })

  // 1.2.1 & 1.3 Data (Mocked for now)
  const currentAQI = ref(156)
  const healthAdvice = ref('Air quality is poor. Wear a mask.')

  // 1.4 Hot Searches
  const hotSearches = ref([
    { rank: 1, city: 'Beijing', visits: 1200 },
    { rank: 2, city: 'Shanghai', visits: 980 },
    { rank: 3, city: 'Guangzhou', visits: 850 }
  ])

  // Mock Action to simulate fetching data when filters change
  function fetchData() {
    console.log('Fetching data for:', filters.value)
    // In real app, call API here using filters.value
    // Then update currentAQI, healthAdvice, etc.
  }

  return { filters, currentAQI, healthAdvice, hotSearches, fetchData }
})
