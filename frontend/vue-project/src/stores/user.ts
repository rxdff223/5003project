import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  // User Profile Data
  const profile = ref({
    id: null as number | null,
    nickname: 'Guest',
    phoneNumber: '',
    defaultCity: 'Shanghai',
    role: 'user',
    token: '',
    // FIX: Initialize this array so components don't crash
    populationTags: [] as string[]
  })

  // Authentication State
  const isLoggedIn = ref(false)
  const isAdmin = ref(false)

  /**
   * Sets the user state based on the specific "0K" Register/Login Response
   * @param apiData - The 'data' object from the response (containing 'token' and 'user')
   */
  function setUserData(apiData: any) {
    const userObj = apiData.user;

    // 1. Set Auth Flags
    isLoggedIn.value = true;
    profile.value.token = apiData.token;

    // 2. Map User Details
    profile.value.id = userObj.id;
    profile.value.nickname = userObj.nickname;
    profile.value.phoneNumber = userObj.phone;
    profile.value.role = userObj.role;

    // FIX: Map the backend 'tag' field (which might be null) to our array
    // Assuming backend sends a comma-separated string or array, or null
    if (Array.isArray(userObj.tag)) {
        profile.value.populationTags = userObj.tag;
    } else if (typeof userObj.tag === 'string') {
        profile.value.populationTags = userObj.tag.split(',');
    } else {
        profile.value.populationTags = [];
    }

    // 3. Handle City
    if (userObj.default_city_id) {
        profile.value.defaultCity = String(userObj.default_city_id);
    }

    // 4. Set Admin Flag
    if (userObj.role === 'admin') {
      isAdmin.value = true;
    } else {
      isAdmin.value = false;
    }
  }

  function logout() {
    isLoggedIn.value = false;
    isAdmin.value = false;
    profile.value = {
      id: null,
      nickname: 'Guest',
      phoneNumber: '',
      defaultCity: 'Shanghai',
      role: 'user',
      token: '',
      populationTags: [] // Reset this too
    };
  }

  return {
    profile,
    isLoggedIn,
    isAdmin,
    setUserData,
    logout
  }
})
