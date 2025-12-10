<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'
import axios from 'axios'

const userStore = useUserStore()
const isLoading = ref(false)

// --- CITY MAPPING ---
const cityMap: Record<string, number> = {
  'Beijing': 1,
  'Shanghai': 2,
  'Guangzhou': 3,
  'Shenzhen': 4,
  'Chengdu': 5
}

// Return type explicitly includes undefined
const getCityNameById = (id: number | string | null): string | undefined => {
  if (!id) return undefined
  const numId = Number(id)
  return Object.keys(cityMap).find(key => cityMap[key] === numId)
}

// --- FORM INITIALIZATION (FIXED TYPE ERROR) ---
let initialTag = 'normal'

if (Array.isArray(userStore.profile.populationTags)) {
  if (userStore.profile.populationTags.length > 0) {
    // FIX: Add "|| 'normal'" fallback.
    // TypeScript fears userStore.profile.populationTags[0] might be undefined.
    initialTag = userStore.profile.populationTags[0] || 'normal'
  }
} else if (typeof userStore.profile.populationTags === 'string') {
  initialTag = userStore.profile.populationTags
}

// Reactive Form State
// Explicitly define types to prevent "Type undefined is not assignable to string"
const formState = reactive<{
  nickname: string;
  phoneNumber: string;
  defaultCityName: string | undefined; // Allow undefined here for the Select placeholder
  populationTag: string;
}>({
  nickname: userStore.profile.nickname,
  phoneNumber: userStore.profile.phoneNumber,
  defaultCityName: getCityNameById(userStore.profile.defaultCity),
  populationTag: initialTag
})

const populationOptions = [
  { label: 'General Population', value: 'normal' },
  { label: 'Elderly', value: 'elderly' },
  { label: 'Children', value: 'children' },
  { label: 'Asthma Patients', value: 'asthma' },
  { label: 'Pregnant Women', value: 'pregnant' }
]

const onSave = async () => {
  isLoading.value = true

  const authHeader = `Bearer ${userStore.profile.token}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': authHeader
    }
  }

  // Convert Name back to ID safely
  const cityId = formState.defaultCityName ? cityMap[formState.defaultCityName] : null;

  const basicInfoData = JSON.stringify({
    nickname: formState.nickname,
    phone: formState.phoneNumber,
    default_city_id: cityId
  })

  const tagsData = JSON.stringify({
    tag: formState.populationTag
  })

  try {
    const [basicRes, tagRes] = await Promise.all([
      axios.put('http://127.0.0.1:80/users/me', basicInfoData, config),
      axios.put('http://127.0.0.1:80/users/me/tags', tagsData, config)
    ])

    const isBasicOk = basicRes.data.code === '0K' || basicRes.status === 200
    const isTagOk = tagRes.data.code === '0K' || tagRes.status === 200

    if (isBasicOk && isTagOk) {
      message.success('All changes saved successfully!')

      // Update Store
      // Error #2 is fixed because updateProfile is now exported in user.ts
      userStore.updateProfile({
        nickname: formState.nickname,
        phoneNumber: formState.phoneNumber,
        defaultCity: String(cityId),
        populationTags: [formState.populationTag]
      })
    } else {
      message.warning('Saved, but backend returned unexpected status.')
    }

  } catch (error: any) {
    console.error('Save Error:', error)
    if (error.response) {
      const status = error.response.status
      if (status === 409) message.error('Phone number conflict')
      else if (status === 401) {
        message.error('Session expired')
        userStore.logout()
      }
      else message.error(`Error: ${error.response.data?.message || 'Request Failed'}`)
    } else {
      message.error('Network Error')
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <a-card title="Personal Information Management" style="max-width: 800px; margin: 0 auto">
    <a-form :model="formState" layout="vertical">

      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Nickname">
            <a-input v-model:value="formState.nickname" :disabled="isLoading" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Phone Number">
            <a-input v-model:value="formState.phoneNumber" :disabled="true" />
            <span style="font-size: 12px; color: #999">Phone is ID (Cannot Change)</span>
          </a-form-item>
        </a-col>
      </a-row>

      <a-form-item label="Default City of Interest">
        <a-select v-model:value="formState.defaultCityName" :disabled="isLoading" placeholder="Select a city">
          <a-select-option v-for="(id, name) in cityMap" :key="id" :value="name">
            {{ name }}
          </a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item label="Population Group (Select One)">
        <a-radio-group
          v-model:value="formState.populationTag"
          :options="populationOptions"
          :disabled="isLoading"
          button-style="solid"
        />
      </a-form-item>

      <a-form-item>
        <a-button type="primary" @click="onSave" :loading="isLoading">Save Changes</a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>
