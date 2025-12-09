<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia';
import AuthModal from '@/components/AuthModal.vue';

// Import Icons
import {
  UserOutlined,
  DashboardOutlined,
  SettingOutlined,
  LoginOutlined,
  LogoutOutlined,
  SafetyCertificateOutlined
} from '@ant-design/icons-vue';

// State
const userStore = useUserStore();
// We use storeToRefs to keep reactivity (so UI updates when you log in)
const { isLoggedIn, isAdmin, profile } = storeToRefs(userStore);

const selectedKeys = ref<string[]>(['1']);
const openKeys = ref<string[]>(['sub_user', 'sub_admin']);
const isAuthModalVisible = ref(false);

const showLogin = () => {
  isAuthModalVisible.value = true;
};

const handleLogout = () => {
  userStore.logout();
};
</script>

<template>
  <a-layout class="app-layout">

    <!-- HEADER: Global Actions (Logo + Login) -->
    <a-layout-header class="header">
      <div class="header-left">
        <div class="logo">EcoHealth</div>
      </div>

      <div class="header-right">
        <!-- 1. IF LOGGED IN: Show Avatar & Name -->
        <div v-if="isLoggedIn">
          <a-dropdown>
            <a-button type="text" class="user-btn">
              <a-avatar style="background-color: #87d068" :size="28">
                <template #icon><UserOutlined /></template>
              </a-avatar>
              <span class="username">{{ profile.nickname }}</span>
            </a-button>
            <template #overlay>
              <a-menu>
                <a-menu-item key="profile">
                  <RouterLink to="/profile">My Profile</RouterLink>
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="logout" @click="handleLogout">
                  <LogoutOutlined /> Logout
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>

        <!-- 2. IF LOGGED OUT: Show Login Button -->
        <div v-else>
          <a-button type="primary" shape="round" @click="showLogin">
            <template #icon><LoginOutlined /></template>
            Login / Register
          </a-button>
        </div>
      </div>
    </a-layout-header>

    <!-- MAIN BODY -->
    <a-layout>
      <!-- SIDEBAR: The Sole Navigator -->
      <a-layout-sider width="240" style="background: #fff">
        <a-menu
          v-model:selectedKeys="selectedKeys"
          v-model:openKeys="openKeys"
          mode="inline"
          style="height: 100%; border-right: 0"
        >
          <!-- Item 1: Dashboard (Main) -->
          <a-menu-item key="1">
            <template #icon><DashboardOutlined /></template>
            <RouterLink to="/">Dashboard</RouterLink>
          </a-menu-item>

          <!-- Item 2: User Center (Submenu) -->
          <a-sub-menu key="sub_user">
            <template #title>
              <span><UserOutlined />User Center</span>
            </template>
            <a-menu-item key="2">
               <RouterLink to="/profile">Profile & Tags</RouterLink>
            </a-menu-item>
          </a-sub-menu>

          <!-- Item 3: Admin Console (Hidden unless Admin) -->
          <a-sub-menu key="sub_admin" v-if="isAdmin">
            <template #title>
              <span><SafetyCertificateOutlined />Administration</span>
            </template>
            <a-menu-item key="3">
              <template #icon><SettingOutlined /></template>
              <RouterLink to="/admin">Admin Console</RouterLink>
            </a-menu-item>
          </a-sub-menu>

        </a-menu>
      </a-layout-sider>

      <!-- CONTENT AREA -->
      <a-layout style="padding: 24px">
        <a-layout-content :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px', borderRadius: '8px' }">
          <RouterView />
        </a-layout-content>
      </a-layout>
    </a-layout>

    <!-- Global Auth Modal -->
    <AuthModal v-model:visible="isAuthModalVisible" />

  </a-layout>
</template>

<style scoped>
.app-layout { min-height: 100vh; }

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  background: #001529; /* Dark AntD Header color */
}

.logo {
  color: white;
  font-size: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

.username {
  color: white;
  margin-left: 8px;
  font-weight: 500;
}

.user-btn:hover {
  background: rgba(255,255,255,0.1);
}
</style>
