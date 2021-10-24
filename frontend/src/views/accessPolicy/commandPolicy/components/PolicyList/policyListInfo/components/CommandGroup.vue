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
import { getCommandGroup } from '@/api/command-group'
export default {
    props: ['commandGroupList'],
    data() {
        return {
            tableQuery: {
                current: 1,
            },
            tableData: [],
            columns: [
                { title: '命令组名称', dataIndex: 'name', ellipsis: true },
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
        getCommandGroup() {
            this.tableLoading = true
            const params = { all_data: 1 }
            getCommandGroup(params)
                .then((res) => {
                    this.tableData = res.data.filter((item) => {
                        return this.commandGroupList.filter((it) => it == item.id).length
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
        this.getCommandGroup()
    },
}
</script>
<style scoped lang='less'>
</style>