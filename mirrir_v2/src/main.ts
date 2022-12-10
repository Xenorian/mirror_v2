import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import ElementPlus from 'element-plus'
import Antd from 'ant-design-vue';
import 'element-plus/dist/index.css'

import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(ElementPlus)
app.use(Antd)
app.use(router)

app.mount('#app')
