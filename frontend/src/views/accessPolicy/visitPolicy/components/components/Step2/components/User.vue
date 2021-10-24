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
import { getUserList } from '@/api/user'
export default {
    props: {
        user_list: {
            type: Array,
            default: () => {
                return []
            },
        },
    },
    watch: {
        user_list: {
            handler(val) {
                this.targetKeys = val
            },
        },
    },
    data() {
        return {
            dataSource: undefined, //左边的数据
            titles: ['可选择的用户', '已选择的用户'],
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
        //获取用户
        getUserList() {
            const params = { all_data: 1 }
            getUserList(params).then((res) => {
                res.data.forEach((item) => {
                    this.$set(item, 'key', item.id + '')
                    this.$set(item, 'title', item.username)
                    this.$set(item, 'description', item.ch_name)
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
        this.getUserList()
    },
}
</script>
<style scoped lang='less'>
</style>