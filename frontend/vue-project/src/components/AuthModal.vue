<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'
import axios from 'axios'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits(['update:visible'])

const userStore = useUserStore()
const activeKey = ref('login')
const isLoading = ref(false)

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


const handleLogin = () => {
  // ... (Keeping existing login logic or waiting for your confirmation)
  if (!loginForm.phone || !loginForm.password) {
    message.error('Please fill in all fields')
    return
  }

  isLoading.value = true

  // 2. Prepare Data (Strict JSON format)
  const data = JSON.stringify({
    "phone": loginForm.phone,
    "password": loginForm.password,
  });

  const config = {
     method: 'post',
     url: 'http://127.0.0.1:80/auth/login',
     headers: {
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type,Authorization',
        'Origin': 'http://localhost:80',
        'Content-Type': 'application/json'
     },
     data : data
  };

  axios(config)
  .then(function (response) {
     console.log(JSON.stringify(response.data));
     const resData = response.data;

     if (resData.code === 'OK') {
        message.success('Login successful!');
        userStore.setUserData(resData.data);

        // Close the popup
        closeModal();
     }
  })
  .catch(function (error) {
     console.log(error);
     message.error('Login failed');
  })
  .finally(() => {
     // Ensure loading stops regardless of success or failure
     isLoading.value = false;
     loginForm.phone = '';
     loginForm.password = '';
  });


}


const handleRegister = () => {
  // 1. Frontend Validation
  if (!registerForm.nickname || !registerForm.phone || !registerForm.password) {
    message.error('Please fill in all fields')
    return
  }
  if (registerForm.password !== registerForm.confirmPassword) {
    message.error('Passwords do not match!')
    return
  }

  isLoading.value = true

  // 2. Prepare Data (Strict JSON format)
  const data = JSON.stringify({
    "phone": registerForm.phone,
    "password": registerForm.password,
    "nickname": registerForm.nickname
  });

  // 3. Axios Config
  const config = {
    method: 'post',
    url: 'http://127.0.0.1:80/auth/register', // Ensure this matches your backend route
    headers: {
      'Content-Type': 'application/json'
    },
    data: data
  };

  // 4. Send Request
  axios(config)
    .then((response) => {
      // The backend returns http 200 for business success "0K"
      console.log(JSON.stringify(response.data));
      const resData = response.data;
      console.log(response.data);

      if (resData.code === 'OK') {
        message.success('Registration successful! You are now logged in.')

        // AUTO-LOGIN: Pass the data object { token: "...", user: {...} } to store
        userStore.setUserData(resData.data)

        // Close the modal immediately
        closeModal()

        // Reset form
        registerForm.phone = ''
        registerForm.password = ''
        registerForm.nickname = ''
        registerForm.confirmPassword = ''
      } else {
        console.log(resData.code)
        // Fallback for other non-0K codes
        message.error(resData.message || 'Registration failed')
      }
    })
    .catch((error) => {
      // Handle HTTP Errors (409, 400, 500)
      if (error.response) {
        // The server responded with a status code out of the 2xx range
        const status = error.response.status;
        const errorMsg = error.response.data?.message;

        if (status === 409) {
          message.error(errorMsg || 'Phone number already exists');
        } else if (status === 400) {
          message.error(errorMsg || 'Missing required fields');
        } else {
          message.error(`Error (${status}): ${errorMsg || 'Unknown error'}`);
        }
      } else if (error.request) {
        // The request was made but no response was received
        message.error('Server no response. Please check your network.');
      } else {
        message.error('Request setup error: ' + error.message);
      }
      console.error('Register Error:', error);
    })
    .finally(() => {
      isLoading.value = false;
      registerForm.phone = '';
      registerForm.nickname = '';
      registerForm.password = '';
      registerForm.confirmPassword = ''
    })
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
    :maskClosable="!isLoading"
  >
    <a-tabs v-model:activeKey="activeKey" centered>

      <!-- TAB 1: LOGIN -->
      <a-tab-pane key="login" tab="Login">
        <a-form layout="vertical">
          <a-form-item label="Phone Number">
            <a-input v-model:value="loginForm.phone" placeholder="Phone number" :disabled="isLoading" />
          </a-form-item>
          <a-form-item label="Password">
            <a-input-password v-model:value="loginForm.password" :disabled="isLoading" />
          </a-form-item>
          <a-button
            type="primary"
            block
            size="large"
            @click="handleLogin"
            style="margin-top: 10px"
            :loading="isLoading"
          >
            Login
          </a-button>
        </a-form>
      </a-tab-pane>

      <!-- TAB 2: REGISTER -->
      <a-tab-pane key="register" tab="Register">
        <a-form layout="vertical">
          <a-form-item label="Nickname">
            <a-input v-model:value="registerForm.nickname" placeholder="Your display name" :disabled="isLoading" />
          </a-form-item>
          <a-form-item label="Phone Number">
            <a-input v-model:value="registerForm.phone" placeholder="11-digit mobile number" :disabled="isLoading" />
          </a-form-item>
          <a-form-item label="Password">
            <a-input-password v-model:value="registerForm.password" :disabled="isLoading" />
          </a-form-item>
          <a-form-item label="Confirm Password">
            <a-input-password v-model:value="registerForm.confirmPassword" :disabled="isLoading" />
          </a-form-item>
          <a-button
            type="primary"
            block
            size="large"
            @click="handleRegister"
            style="margin-top: 10px"
            :loading="isLoading"
          >
            Register & Auto Login
          </a-button>
        </a-form>
      </a-tab-pane>

    </a-tabs>
  </a-modal>
</template>
