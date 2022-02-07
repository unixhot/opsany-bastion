<template>
    <div>
        <content-header>
            <div slot="docs"></div>
        </content-header>
        <a-card>
            <a-tabs v-model="activeTab">
                <a-tab-pane v-for="item in tabList" :key="item.key" :tab="item.name">
                    <component :is="item.key" v-if="item.key == activeTab"></component>
                </a-tab-pane>
            </a-tabs>
        </a-card>
    </div>
</template>
<script>
import User from './components/User'
import Group from './components/Group'
import { getPageAuth } from '@/utils/pageAuth'
export default {
    components: { User, Group },
    data() {
        return {
            tabList: [
                { name: '用户列表', key: 'User' },
                { name: '用户组', key: 'Group' },
            ],
            activeTab: '',
        }
    },
    methods: {},
    async mounted() {
        const hasAuth = await getPageAuth(this, 'visit-user-admin')
        if (hasAuth) {
            this.activeTab = 'User'
        }
    },
}
</script>
<style scoped lang='less'>
</style>