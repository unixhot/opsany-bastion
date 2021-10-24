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
import { getUserList } from '@/api/user'
export default {
    props: ['userList'],
    data() {
        return {
            tableQuery: {
                current: 1,
            },
            tableData: [],
            columns: [
                { title: '用户名', dataIndex: 'username', ellipsis: true },
                { title: '昵称', dataIndex: 'ch_name', ellipsis: true },
                { title: '邮箱', dataIndex: 'email', ellipsis: true },
            ],
            tableLoading: false,
        }
    },
    methods: {
        //获取用户列表
        getUserList() {
            this.tableLoading = true
            const params = { all_data: 1 }
            getUserList(params)
                .then((res) => {
                    this.tableData = res.data.filter((item) => {
                        return this.userList.filter((it) => it == item.id).length
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
        this.getUserList()
    },
}
</script>
<style scoped lang='less'>
</style>