<template>
    <div>
        <a-transfer
            :dataSource="dataSource"
            :targetKeys="targetKeys"
            :selectedKeys="selectedKeys"
            @change="handleChange"
            @selectChange="handleSelectChange"
            showSearch
            :render="(item) => `${item.title}-${item.description}`"
            :list-style="listStyle"
            :operations="operations"
            :titles="titles"
            :lazy="false"
        ></a-transfer>
    </div>
</template>
<script>
import { getCommandGroup } from '@/api/command-group'
export default {
    props: {
        command_group_list: {
            type: Array,
            default: () => {
                return []
            },
        },
        listStyle: {
            type: Object,
            default: () => {
                return {
                    width: '370px',
                    height: '420px',
                }
            },
        },
    },
    watch: {
        command_group_list: {
            handler(val) {
                this.targetKeys = val
            },
			immediate:true
        },
    },
    data() {
        return {
            dataSource: undefined, //左边的数据
            titles: ['可选择的命令组', '已选择的命令组'],
            operations: ['加入右侧', '加入左侧'],
            targetKeys: [],
            selectedKeys: [], //checkbox选中的数据
        }
    },
    methods: {
        //获取命令组
        getCommandGroup() {
            const params = { all_data: 1 }
            getCommandGroup(params).then((res) => {
                res.data.forEach((item) => {
                    this.$set(item, 'key', item.id + '')
                    this.$set(item, 'title', item.name)
                    this.$set(item, 'description', item.description || '--')
                })
                this.dataSource = res.data
            })
        },
        handleChange(nextTargetKeys) {
            this.targetKeys = nextTargetKeys
        },
        handleSelectChange(sourceSelectedKeys, targetSelectedKeys) {
            this.selectedKeys = [...sourceSelectedKeys, ...targetSelectedKeys]
        },
        resetData() {
            this.targetKeys = []
            this.selectedKeys = []
        },
        getFormData() {
            return this.targetKeys
        },
    },
    mounted() {
        this.getCommandGroup()
    },
}
</script>
<style scoped lang='less'>
</style>