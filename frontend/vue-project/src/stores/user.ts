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
    populationTags: [] as string[]
  })

  // Authentication State
  const isLoggedIn = ref(false)
  const isAdmin = ref(false)

  /**
   * Sets the user state based on the specific "0K" Register/Login Response
   */
  function setUserData(apiData: any) {
    const userObj = apiData.user;
    isLoggedIn.value = true;
    profile.value.token = apiData.token;

    profile.value.id = userObj.id;
    profile.value.nickname = userObj.nickname;
    profile.value.phoneNumber = userObj.phone;
    profile.value.role = userObj.role;

    // Handle Tag (Backend sends string or null)
    if (userObj.tag) {
        // Wrap single string in array for frontend compatibility
        profile.value.populationTags = [userObj.tag];
    } else {
        profile.value.populationTags = [];
    }

    // Handle City
    if (userObj.default_city_id) {
        profile.value.defaultCity = String(userObj.default_city_id);
    }

    // Set Admin Flag
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
      populationTags: []
    };
  }

  function updateProfile(newData: any) {
    profile.value = { ...profile.value, ...newData }
  }

  // --- RETURN BLOCK ---
  // This defines what is accessible to your components
  return {
    profile,
    isLoggedIn,
    isAdmin,
    setUserData,
    logout,
    updateProfile // <--- ADDED THIS (Fixes Error #2)
  }
})
