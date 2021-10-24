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
import { getUserGroupList } from '@/api/user'
export default {
    props: {
        user_group_list: {
            type: Array,
            default: () => {
                return []
            },
        },
    },
    watch: {
        user_group_list: {
            handler(val) {
                this.targetKeys = val
            },
        },
    },
    data() {
        return {
            dataSource: undefined, //左边的数据
            titles: ['可选择的用户组', '已选择的用户组'],
            operations: ['加入右侧', '加入左侧'],
            targetKeys: [],
            selectedKeys: [], //checkbox选中的数据
            listStyle: {
                width: '370px',
                height: '420px',
            },
        }
    },
    methods: {
        //获取用户组
        getUserGroupList() {
            const params = { all_data: 1 }
            getUserGroupList(params).then((res) => {
                res.data.forEach((item) => {
                    this.$set(item, 'key', item.id + '')
                    this.$set(item, 'title', item.name)
                    item.description = item.description || ''
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
        this.getUserGroupList()
    },
}
</script>
<style scoped lang='less'>
</style>