<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits(['update:visible'])

const userStore = useUserStore()
const activeKey = ref('login') // 'login' or 'register'

// --- Form Data ---
const loginForm = reactive({
  phone: '',
  password: ''
})

const registerForm = reactive({
  nickname: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

// --- Actions ---
const handleLogin = () => {
  if (!loginForm.phone || !loginForm.password) {
    message.error('Please enter phone and password')
    return
  }

  // SIMULATION: If phone is "admin", we log them in as admin
  const role = loginForm.phone === 'admin' ? 'admin' : 'user'
  userStore.login(loginForm.phone, role)

  message.success('Login successful!')
  closeModal()
}

const handleRegister = () => {
  if (!registerForm.nickname || !registerForm.phone || !registerForm.password) {
    message.error('Please fill in all fields')
    return
  }
  if (registerForm.password !== registerForm.confirmPassword) {
    message.error('Passwords do not match!')
    return
  }

  // In a real app, you would send API request here
  message.success('Registration successful! Please log in.')
  activeKey.value = 'login' // Switch to login tab automatically
}

const closeModal = () => {
  emit('update:visible', false)
}
</script>

<template>
  <a-modal
    :visible="visible"
    title="Welcome to EcoHealth"
    :footer="null"
    @cancel="closeModal"
    width="400px"
  >
    <a-tabs v-model:activeKey="activeKey" centered>

      <!-- TAB 1: LOGIN -->
      <a-tab-pane key="login" tab="Login">
        <a-form layout="vertical">
          <a-form-item label="Phone Number">
            <a-input v-model:value="loginForm.phone" placeholder="Try 'admin' for admin features" />
          </a-form-item>
          <a-form-item label="Password">
            <a-input-password v-model:value="loginForm.password" />
          </a-form-item>
          <a-button type="primary" block size="large" @click="handleLogin" style="margin-top: 10px">
            Login
          </a-button>
        </a-form>
      </a-tab-pane>

      <!-- TAB 2: REGISTER -->
      <a-tab-pane key="register" tab="Register">
        <a-form layout="vertical">
          <a-form-item label="Nickname">
            <a-input v-model:value="registerForm.nickname" />
          </a-form-item>
          <a-form-item label="Phone Number">
            <a-input v-model:value="registerForm.phone" />
          </a-form-item>
          <a-form-item label="Password">
            <a-input-password v-model:value="registerForm.password" />
          </a-form-item>
          <a-form-item label="Confirm Password">
            <a-input-password v-model:value="registerForm.confirmPassword" />
          </a-form-item>
          <a-button type="primary" block size="large" @click="handleRegister" style="margin-top: 10px">
            Register
          </a-button>
        </a-form>
      </a-tab-pane>

    </a-tabs>
  </a-modal>
</template>
