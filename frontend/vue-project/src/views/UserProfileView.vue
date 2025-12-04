<script setup lang="ts">
import { reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'

const userStore = useUserStore()
const formState = reactive({ ...userStore.profile })

const populationOptions = [
  { label: 'General Population', value: 'General' },
  { label: 'Elderly', value: 'Elderly' },
  { label: 'Children', value: 'Children' },
  { label: 'Asthma Patients', value: 'Asthma' },
  { label: 'Pregnant Women', value: 'Pregnant' }
]

const onSave = () => {
  userStore.updateProfile(formState)
  message.success('Profile updated successfully!')
}
</script>

<template>
  <a-card title="Personal Information Management" style="max-width: 800px; margin: 0 auto">
    <a-form :model="formState" layout="vertical">

      <!-- 1.1 Personal Info -->
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="Nickname">
            <a-input v-model:value="formState.nickname" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="Phone Number">
            <a-input v-model:value="formState.phoneNumber" />
          </a-form-item>
        </a-col>
      </a-row>

      <a-form-item label="Default City of Interest">
        <a-select v-model:value="formState.defaultCity">
          <a-select-option value="Beijing">Beijing</a-select-option>
          <a-select-option value="Shanghai">Shanghai</a-select-option>
          <a-select-option value="London">London</a-select-option>
        </a-select>
      </a-form-item>

      <!-- 1.1 Population Tag Setting -->
      <a-form-item label="Population Group (For Personalized Advice)">
        <a-checkbox-group v-model:value="formState.populationTags" :options="populationOptions" />
      </a-form-item>

      <a-form-item>
        <a-button type="primary" @click="onSave">Save Changes</a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>
