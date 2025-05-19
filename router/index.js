import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

export const staticRoutes = [
  {
    path: '/',
    component: () => import('@/views/index/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '*',
    redirect: '/404',
    hidden: true
  }
]
export const asyncRoutes = []

const createRouter = () => new Router({
  mode: 'history', // require service support
  base: '/web/',
  scrollBehavior: () => ({ y: 0 }),
  routes: staticRoutes
})
const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
