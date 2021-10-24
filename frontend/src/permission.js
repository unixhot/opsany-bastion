import router from './router'
import store from './store'
import NProgress from 'nprogress' // progress bar
import '@/components/NProgress/nprogress.less' // progress bar custom style

NProgress.configure({ showSpinner: false }) // NProgress Configuration


router.beforeEach((to, from, next) => {
    NProgress.start()
    if (!store.getters.addRouters.length) {
        store.dispatch('GenerateRoutes').then(() => {
            // 动态添加可访问路由表
            router.addRoutes(store.getters.addRouters)
            const redirect = decodeURIComponent(from.query.redirect || to.path)
            if (to.path === redirect) {
                // hack方法 确保addRoutes已完成 ,set the replace: true so the navigation will not leave a history record
                next({ ...to, replace: true })
            } else {
                // 跳转到目的路由
                next({ path: redirect })
            }
        }).catch(err => {
            next()
        })
    } else {
        next()
    }
})

router.afterEach(() => {
    NProgress.done() // finish progress bar
})