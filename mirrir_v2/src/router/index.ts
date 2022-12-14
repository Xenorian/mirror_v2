import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      path: '/chart',
      name: 'chart',
      component: () => import('../views/ChartView.vue'),
      redirect: '/chart/dashboard',
      children: [
        {
          path: 'dashboard',
          component: () => import('../components/charts/DashBoard.vue')
        },

        {
          path: 'main_contributor',
          component: () => import('../components/charts/MainContributor.vue')
        },


        {
          path: 'develop_star',
          component: () => import('../components/charts/LineChart.vue')
        },
        {
          path: 'develop_commit',
          component: () => import('../components/charts/LineChart.vue')
        },
        {
          path: 'develop_issue',
          component: () => import('../components/charts/LineChart.vue')
        },
        {
          path: 'develop_pr',
          component: () => import('../components/charts/LineChart.vue')
        },


        {
          path: 'company_commit',
          component: () => import('../components/charts/Bubblechart.vue')
        },
        {
          path: 'company_issue',
          component: () => import('../components/charts/Bubblechart.vue')
        },
        {
          path: 'company_pr',
          component: () => import('../components/charts/Bubblechart.vue')
        },
      ]
    }
  ]
})

export default router
