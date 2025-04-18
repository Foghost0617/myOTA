import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import TAmain from '../views/Agency/TAmain.vue'
import Govmain from '../views/Gov/Govmain.vue'
import Guidemain from '../views/Guide/Guidemain.vue'
import Touristmain from '../views/Tourist/Tourist.vue'


const routes = [
  { path: '/', component: Login },          // 默认页面：登录
  { path: '/tourist', component: Touristmain },    // 登录成功后跳转到 /agency
  { path: '/guide', component: Guidemain }   , // 登录成功后跳转到 /agency
  { path: '/agency', component: TAmain }    ,// 登录成功后跳转到 /agency
  { path: '/gov', component: Govmain }    ,// 登录成功后跳转到 /agency



]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
