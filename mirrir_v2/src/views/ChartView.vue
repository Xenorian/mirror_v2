<template>
  <a-layout>
    <a-layout-header class="header">

      <a-menu v-model:selectedKeys="selectedKeys1" theme="dark" mode="horizontal" @click="backToHome"
        :style="{ lineHeight: '64px' }">
        <a-menu-item key="1">回到首页</a-menu-item>

      </a-menu>
    </a-layout-header>

    <a-layout>
      <a-layout-sider width="200" style="background: #fff">
        <a-menu v-model:selectedKeys="selectedKeys2" v-model:openKeys="openKeys" mode="inline" @click="handelClick"
          :style="{ borderRight: 0 }">
          <a-menu-item key="dashboard">
            <dashboard-outlined />
            总览
          </a-menu-item>

          <a-menu-item key="main_contributor">
            <user-outlined />
            主要贡献者
          </a-menu-item>

          <a-sub-menu key="sub1">
            <template #title>
              <span>
                <line-chart-outlined />
                社区发展速度
              </span>
            </template>
            <a-menu-item key="develop_commit">Commit</a-menu-item>
            <a-menu-item key="develop_issue">Issue</a-menu-item>
            <a-menu-item key="develop_pr">Pull Request</a-menu-item>
          </a-sub-menu>
          <a-sub-menu key="sub2">
            <template #title>
              <span>
                <laptop-outlined />
                按公司查看数据
              </span>
            </template>
            <a-menu-item key="company_commit">Commit</a-menu-item>
            <a-menu-item key="company_issue">Issue</a-menu-item>
            <a-menu-item key="company_pr">Pull Request</a-menu-item>
          </a-sub-menu>
        </a-menu>
      </a-layout-sider>

      <a-layout style="padding: 0 24px 24px; height: 800px;">
        <div style="margin-top: 10px;margin-bottom: 10px;">

        </div>

        <a-layout-content :style="{
          background: '#fff',
          padding: '24px', margin: 0,
          minHeight: '400px'
        }">
          <suspense>
            <router-view class="page" />
          </suspense>
        </a-layout-content>
      </a-layout>
    </a-layout>
  </a-layout>
</template>

<script lang="ts" async setup>
import { RouterView } from 'vue-router'
import {
  DashboardOutlined, LineChartOutlined,
  UserOutlined, LaptopOutlined
} from '@ant-design/icons-vue';
import { ref, onMounted } from 'vue';
import { repoDataStore } from '@/stores/repoData'
import { useRouter } from "vue-router";


onMounted(() => {
  window.onbeforeunload = function (e) {
    var message = '不要刷新';
    e = e || window.event;
    if (e) {
      e.returnValue = message;
    }
    return "浏览器关闭！";
  }
})

const m_repoData = repoDataStore();

const selectedKeys1 = ref<string[]>(['2'])
const selectedKeys2 = ref<string[]>(['1'])
const collapsed = ref<boolean>(false)
const openKeys = ref<string[]>(['sub1'])

const router = useRouter();

const handelClick = (item) => {
  router.push(item.key)
}

const backToHome = () => {
  m_repoData.clearData();
  router.replace('/home')
}
</script>

<style>
.site-layout-background {
  background: rgb(211, 211, 211);
}
</style>