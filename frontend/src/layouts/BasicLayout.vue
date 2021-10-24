<template>
    <pro-layout
        :title="title"
        :logo="require('../assets/logo-reverse.png')"
        :menus="menus"
        :collapsed="collapsed"
        :mediaQuery="query"
        :isMobile="isMobile"
        :handleMediaQuery="handleMediaQuery"
        :handleCollapse="handleCollapse"
        :i18nRender="i18nRender"
        v-bind="settings"
        style="padding: 20px"
        :menuHeaderRender="menuHeaderRender"
    >
        <!-- <setting-drawer :settings="settings" @change="handleSettingChange" /> -->
        <template v-slot:rightContentRender>
            <right-content :top-menu="settings.layout === 'topmenu'" :is-mobile="isMobile" :theme="settings.theme" />
        </template>
        <template v-slot:footerRender>
            <global-footer />
        </template>
        <router-view />
    </pro-layout>
</template>


<script>
import { SettingDrawer, updateTheme } from '@ant-design-vue/pro-layout'
import { i18nRender } from '@/locales'
import { mapState, mapActions } from 'vuex'
import { SIDEBAR_TYPE, TOGGLE_MOBILE_TYPE } from '@/store/mutation-types'
import { asyncRouterMap } from '@/config/router.config.js'

import defaultSettings from '@/config/defaultSettings'
import RightContent from '@/components/GlobalHeader/RightContent'
import GlobalFooter from '@/components/GlobalFooter'
import opsLogo from '../assets/ops-logo.png'

export default {
    name: 'BasicLayout',
    components: {
        SettingDrawer,
        RightContent,
        GlobalFooter,
    },
    data() {
        return {
            // preview.pro.antdv.com only use.
            isProPreviewSite: process.env.VUE_APP_PREVIEW === 'true' && process.env.NODE_ENV !== 'development',
            // end

            // base
            menus: [],
            // 侧栏收起状态
            collapsed: false,
            title: defaultSettings.title,
            settings: {
                // 布局类型
                layout: defaultSettings.layout, // 'sidemenu', 'topmenu'
                // 定宽: true / 流式: false
                contentWidth: defaultSettings.layout === 'sidemenu' ? false : defaultSettings.contentWidth === 'Fixed',
                // 主题 'dark' | 'light'
                theme: defaultSettings.navTheme,
                // 主色调
                primaryColor: defaultSettings.primaryColor,
                fixedHeader: defaultSettings.fixedHeader,
                fixSiderbar: defaultSettings.fixSiderbar,
                colorWeak: defaultSettings.colorWeak,

                hideHintAlert: false,
                hideCopyButton: false,
            },
            // 媒体查询
            query: {},

            // 是否手机模式
            isMobile: false,

            menuHeaderRender: (title, logo) => {
                return (
                    <a href="#" onClick={this.clickLogo}>
                        {logo}
                        <h1>{defaultSettings.title}</h1>
                    </a>
                )
            },
        }
    },
    computed: {
        ...mapState({
            // 动态主路由
            mainMenu: (state) => state.permission.addRouters,
        }),
    },
    created() {
        // this.menus = asyncRouterMap.find((item) => item.path === '/').children
        this.menus = this.mainMenu.find((item) => item.path === '/').children
        this.collapsed = !this.sidebarOpened
    },
    mounted() {
        this.getUserInfo()
        const userAgent = navigator.userAgent
        if (userAgent.indexOf('Edge') > -1) {
            this.$nextTick(() => {
                this.collapsed = !this.collapsed
                setTimeout(() => {
                    this.collapsed = !this.collapsed
                }, 16)
            })
        }

        // first update color
        // updateTheme(this.settings.primaryColor)
    },
    methods: {
        ...mapActions(['getUserInfo']),
        i18nRender,
        handleMediaQuery(val) {
            this.query = val
            if (this.isMobile && !val['screen-xs']) {
                this.isMobile = false
                return
            }
            if (!this.isMobile && val['screen-xs']) {
                this.isMobile = true
                this.collapsed = false
                this.settings.contentWidth = false
                // this.settings.fixSiderbar = false
            }
        },
        handleCollapse(val) {
            this.collapsed = val
        },
        handleSettingChange({ type, value }) {
            type && (this.settings[type] = value)
            switch (type) {
                case 'contentWidth':
                    this.settings[type] = value === 'Fixed'
                    break
                case 'layout':
                    if (value === 'sidemenu') {
                        this.settings.contentWidth = false
                    } else {
                        this.settings.fixSiderbar = false
                        this.settings.contentWidth = true
                    }
                    break
            }
        },
        clickLogo(e) {
            window.location.href = window.API_ROOT
        },
        logoRender() {
            return <image src={opsLogo} />
        },
    },
}
</script>

<style lang="less">
@import './BasicLayout.less';
#logo {
    a {
        img {
            width: 32px;
            height: 32px;
        }
    }
}
</style>
