<template>
    <div>
        <content-header >
            <div slot="docs">
                通过策略授权，将主机、用户和用户组、资源和凭证进行关联，设置用户允许和禁止支持哪些指令或指令集。
            </div>
        </content-header>
        <a-card>
            <a-tabs v-model="activeTab">
                <a-tab-pane v-for="item in tabList" :key="item.key" :tab="item.name">
                    <component :is="activeTab" v-if="item.key == activeTab"></component>
                </a-tab-pane>
            </a-tabs>
        </a-card>
    </div>
</template>
<script>
import { readDirfiles } from '@/utils/util'
import PolicyList from './components/PolicyList'
import CommandList from './components/CommandList'
import CommandGroup from './components/CommandGroup'
export default {
    components: { PolicyList, CommandList, CommandGroup },
    data() {
        return {
            tabList: [
                { key: 'PolicyList', name: '策略列表' },
                { key: 'CommandList', name: '命令列表' },
                { key: 'CommandGroup', name: '命令组' },
            ],
            activeTab: 'PolicyList',
        }
    },
    methods: {},
    mounted() {},
}
</script>
<style scoped lang='less'>
</style>