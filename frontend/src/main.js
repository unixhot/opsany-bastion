// with polyfills
import 'core-js/stable'
import 'regenerator-runtime/runtime'

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/'
import i18n from './locales'
import { VueAxios } from './utils/request'
import ProLayout, { PageHeaderWrapper } from '@ant-design-vue/pro-layout'
import themePluginConfig from '../config/themePluginConfig'
import ContentHeader from '@/views/components/ContentHeader'
import VCharts from 'v-charts'
import countTo from 'vue-count-to'
import searchBox from './components/searchBox'
import bootstrap from './core/bootstrap'
import './core/lazy_use'
import './utils/filter' // global filter
import './global.less'
import './permission' // permission control

Vue.config.productionTip = false

// mount axios to `Vue.$http` and `this.$http`
Vue.use(VueAxios)
Vue.use(VCharts)
Vue.component('pro-layout', ProLayout)
Vue.component('page-header-wrapper', PageHeaderWrapper)
Vue.component('content-header', ContentHeader)
Vue.component('count-to', countTo)
Vue.component('search-box', searchBox)

window.umi_plugin_ant_themeVar = themePluginConfig.theme

new Vue({
    router,
    store,
    i18n,
    created: bootstrap,
    render: h => h(App)
}).$mount('#app')