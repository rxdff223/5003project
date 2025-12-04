import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  // 1.1 User Center Data
  const profile = ref({
    nickname: 'User123',
    phoneNumber: '123-456-7890',
    defaultCity: 'Shanghai',
    populationTags: [] as string[] // e.g., ['Elderly', 'Asthma']
  })

  // Actions to update profile
  function updateProfile(newData: any) {
    profile.value = { ...profile.value, ...newData }
  }

  return { profile, updateProfile }
})
