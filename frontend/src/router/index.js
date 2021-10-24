import Vue from 'vue'
import Router from 'vue-router'
import { constantRouterMap, asyncRouterMap, detailRouterMap } from '@/config/router.config'

Vue.use(Router)

export default new Router({
    mode: 'hash',
    scrollBehavior: () => ({ y: 0 }),
    routes: constantRouterMap,
    // routes: constantRouterMap.concat(asyncRouterMap), // -- 若不是服务器返回的菜单 可改为.concat(asyncRouterMap)  注意detailRouterMap要放在父级路由下

})