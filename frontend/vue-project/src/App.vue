<script setup lang="ts">
import { ref } from 'vue';
import { RouterView, RouterLink } from 'vue-router';
import {
  UserOutlined,
  DashboardOutlined,
  SettingOutlined,
} from '@ant-design/icons-vue';
import {
  Layout as ALayout,
  LayoutHeader as ALayoutHeader,
  LayoutSider as ALayoutSider,
  LayoutContent as ALayoutContent,
  Menu as AMenu,
  MenuItem as AMenuItem,
  SubMenu as ASubMenu,
} from 'ant-design-vue';

// State for menu
const selectedKeys = ref<string[]>(['1']);
</script>

<template>
  <a-layout class="app-layout">
    <a-layout-header class="header">
      <div class="logo">EcoHealth App</div>
      <a-menu theme="dark" mode="horizontal" :style="{ lineHeight: '64px' }">
        <a-menu-item key="1"><RouterLink to="/">Dashboard</RouterLink></a-menu-item>
        <a-menu-item key="2"><RouterLink to="/admin">Admin Console</RouterLink></a-menu-item>
      </a-menu>
    </a-layout-header>

    <a-layout>
      <a-layout-sider width="200" style="background: #fff">
        <a-menu
          v-model:selectedKeys="selectedKeys"
          mode="inline"
          style="height: 100%; border-right: 0"
        >
          <a-menu-item key="1">
            <template #icon><DashboardOutlined /></template>
            <RouterLink to="/">Total Data Query</RouterLink>
          </a-menu-item>

          <a-sub-menu key="sub1">
            <template #title>
              <span><UserOutlined />User Center</span>
            </template>
            <a-menu-item key="2">
               <RouterLink to="/profile">Profile & Tags</RouterLink>
            </a-menu-item>
          </a-sub-menu>

          <a-menu-item key="3">
            <template #icon><SettingOutlined /></template>
            <RouterLink to="/admin">System Monitor</RouterLink>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>

      <a-layout style="padding: 24px">
        <a-layout-content :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }">
          <RouterView />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </a-layout>
</template>

<style scoped>
.app-layout { min-height: 100vh; }
.header { display: flex; align-items: center; padding: 0 24px; }
.logo {
  color: white; font-size: 18px; font-weight: bold; margin-right: 40px;
}
</style>
