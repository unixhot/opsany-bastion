<template>
    <div>
        <a-tabs v-model="activeTab" ref="tabs">
            <a-tab-pane v-for="item in tabList" :key="item.key" :tab="item.name"> </a-tab-pane>
        </a-tabs>
        <Command v-show="activeTab == 'Command'" ref="Command" :command_list="command_list"></Command>
        <CommandGroup
            v-show="activeTab == 'CommandGroup'"
            ref="CommandGroup"
            :command_group_list="command_group_list"
        ></CommandGroup>
    </div>
</template>
<script>
import Command from './components/Command.vue'
import CommandGroup from './components/CommandGroup.vue'
export default {
    components: { Command, CommandGroup },
    props: {
        command: {
            type: Object,
            default: () => {
                return {}
            },
        },
    },
    watch: {
        command: {
            handler(val) {
                this.command_list = val.command || []
                this.command_group_list = val.command_group || []
                this.command_list.forEach((item, index) => {
                    this.command_list[index] = item + ''
                })
                this.command_group_list.forEach((item, index) => {
                    this.command_group_list[index] = item + ''
                })
            },
        },
    },
    data() {
        return {
            tabList: [
                { key: 'Command', name: '关联命令' },
                { key: 'CommandGroup', name: '关联命令组' },
            ],
            activeTab: 'Command',
            command_list: [],
            command_group_list: [],
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
            const command = this.$refs.Command.getFormData()
            const command_group = this.$refs.CommandGroup.getFormData()
            // if (this.activeTab == 'Command') return { command }
            // else return { command_group }
            return { command, command_group }
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
</style>