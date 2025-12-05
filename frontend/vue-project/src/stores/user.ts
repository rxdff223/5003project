import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  // User Profile Data
  const profile = ref({
    nickname: 'Guest',
    phoneNumber: '',
    defaultCity: 'Shanghai',
    populationTags: [] as string[]
  })

  // Authentication State
  const isLoggedIn = ref(false)
  const isAdmin = ref(false) // <--- The specific flag you requested

  /**
   * Mock Login Function
   * @param phone - The phone number entered
   * @param role - 'user' or 'admin'
   */
  function login(phone: string, role: 'user' | 'admin' = 'user') {
    isLoggedIn.value = true
    profile.value.phoneNumber = phone

    // Logic: If the role is admin OR the phone number is literally 'admin', grant admin rights
    if (role === 'admin' || phone === 'admin') {
      isAdmin.value = true
      profile.value.nickname = 'Administrator'
    } else {
      isAdmin.value = false
      profile.value.nickname = 'User ' + phone.slice(-4)
    }
  }

  function logout() {
    isLoggedIn.value = false
    isAdmin.value = false
    profile.value = {
      nickname: 'Guest',
      phoneNumber: '',
      defaultCity: 'Shanghai',
      populationTags: []
    }
  }

  function updateProfile(newData: any) {
    profile.value = { ...profile.value, ...newData }
  }

  return {
    profile,
    isLoggedIn,
    isAdmin,
    login,
    logout,
    updateProfile
  }
})
