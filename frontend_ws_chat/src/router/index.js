import { createRouter, createWebHashHistory } from 'vue-router'
import Login from  '@/pages/Login'
import SignUp from  '@/pages/SignUp'
import Home from '@/pages/Home'
import room from '@/pages/room'

const routes = [
  {
      path:'/',
      component: Home
  },
  {
      path:'/login',
      component: Login
  },
  {
      path:'/registr',
      component: SignUp
  },
  {
    path:'/room',
    component: room
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
