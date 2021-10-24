<template>
    <div>
        <a-tabs v-model="activeTab" ref="tabs">
            <a-tab-pane v-for="item in tabList" :key="item.key" :tab="item.name"> </a-tab-pane>
        </a-tabs>
        <User v-show="activeTab == 'User'" ref="User" :user_list="user_list"></User>
        <Group v-show="activeTab == 'Group'" ref="Group" :user_group_list="user_group_list"></Group>
    </div>
</template>
<script>
import User from './components/User.vue'
import Group from './components/Group.vue'
export default {
    components: { User, Group },
    props: {
        user: {
            type: Object,
            default: () => {
                return {}
            },
        },
    },
    watch: {
        user: {
            handler(val) {
                this.user_list = val.user || []
                this.user_group_list = val.user_group || []
                this.user_list.forEach((item, index) => {
                    this.user_list[index] = item + ''
                })
                this.user_group_list.forEach((item, index) => {
                    this.user_group_list[index] = item + ''
                })
            },
        },
    },
    data() {
        return {
            tabList: [
                { key: 'User', name: '关联用户' },
                { key: 'Group', name: '关联用户组' },
            ],
            activeTab: 'User',
            user_list: [],
            user_group_list: [],
        }
    },
    methods: {
        resetFormData() {
            this.activeTab = this.$options.data().activeTab
            this.tabList.forEach((item) => {
                this.$refs[item.key]?.resetData()
            })
        },
        getFormData() {
            const user = this.$refs.User.getFormData()
            const user_group = this.$refs.Group.getFormData()
            return { user, user_group }
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
</style>