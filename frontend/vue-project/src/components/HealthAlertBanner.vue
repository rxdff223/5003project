<script setup lang="ts">
import { computed } from 'vue'
import { useDashboardStore } from '@/stores/dashboardData'
import { useUserStore } from '@/stores/user'

const dashStore = useDashboardStore()
const userStore = useUserStore()

// 1.3 Personalized Logic
const personalizedMessage = computed(() => {
  const isAsthma = userStore.profile.populationTags.includes('Asthma')
  const baseMsg = `Current AQI is ${dashStore.currentAQI}.`

  if (dashStore.currentAQI > 100 && isAsthma) {
    return `Warning for Asthma Patients: ${baseMsg} Please keep windows closed and turn on air purifier.`
  }
  return `${baseMsg} ${dashStore.healthAdvice}`
})

const alertType = computed(() => dashStore.currentAQI > 100 ? 'warning' : 'success')
</script>

<template>
  <a-alert
    :message="personalizedMessage"
    :type="alertType"
    show-icon
    closable
    style="margin-bottom: 20px"
  />
</template>
