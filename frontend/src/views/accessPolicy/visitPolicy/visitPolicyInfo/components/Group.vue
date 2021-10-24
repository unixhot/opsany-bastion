<template>
    <div>
        <a-table
            :loading="tableLoading"
            :dataSource="tableData"
            :columns="columns"
            :pagination="{
                ...tableQuery,
                showSizeChanger: true,
                showTotal: (total) => `共 ${total} 条数据`,
                showQuickJumper: true,
            }"
            @change="tableChange"
            :rowKey="(item) => item.id"
        ></a-table>
    </div>
</template>
<script>
import { getUserGroupList } from '@/api/user'
export default {
    props: ['userGroupList'],
    data() {
        return {
            tableQuery: {
                current: 1,
            },
            tableData: [],
            columns: [
                { title: '用户组名称', dataIndex: 'name', ellipsis: true },
                {
                    title: '描述',
                    dataIndex: 'description',
                    ellipsis: true,
                    customRender(text) {
                        return text || '--'
                    },
                },
            ],
            tableLoading: false,
        }
    },
    methods: {
        //获取用户列表
        getUserGroupList() {
            this.tableLoading = true
            const params = { all_data: 1 }
            getUserGroupList(params)
                .then((res) => {
                    this.tableData = res.data.filter((item) => {
                        return this.userGroupList.filter((it) => it == item.id).length
                    })
                })
                .finally(() => {
                    this.tableLoading = false
                })
        },
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
        },
    },
    mounted() {
        this.getUserGroupList()
    },
}
</script>
<style scoped lang='less'>
</style>