<template>
    <div>
        <a-transfer
            :dataSource="dataSource"
            :targetKeys="targetKeys"
            :selectedKeys="selectedKeys"
            @change="handleChange"
            @selectChange="handleSelectChange"
            showSearch
            :render="(item) => item.title"
            :list-style="listStyle"
            :operations="operations"
            :titles="titles"
            :lazy="false"
        ></a-transfer>
    </div>
</template>
<script>
import { getResourceCredential } from '@/api/resource-credential'
export default {
    props: {
        credential_group: {
            type: Array,
            default: () => {
                return []
            },
        },
    },
    watch: {
        credential_group: {
            handler(val) {
                this.targetKeys = val
            },
        },
    },
    data() {
        return {
            dataSource: undefined, //左边的数据
            titles: ['可选择的凭证分组', '已选择的凭证分组'],
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
        //获取密码凭证
        getResourceCredential() {
            const params = { data_type: 'group' }
            getResourceCredential(params).then((res) => {
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
        this.getResourceCredential()
    },
}
</script>
<style scoped lang='less'>
</style>