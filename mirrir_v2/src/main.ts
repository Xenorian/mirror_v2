import { createApp } from 'vue'
import { createPinia,defineStore } from 'pinia'

import App from './App.vue'
import router from './router'

import ElementPlus from 'element-plus'
import Antd from 'ant-design-vue';
import 'element-plus/dist/index.css'
import 'ant-design-vue/dist/antd.css';

import './assets/main.css'

const app = createApp(App)

import piniaPluginPersist from 'pinia-plugin-persist'
const pinia = createPinia()
pinia.use(piniaPluginPersist)

app.use(pinia)
app.use(createPinia())
app.use(ElementPlus)
app.use(Antd)
app.use(router)

app.mount('#app')
