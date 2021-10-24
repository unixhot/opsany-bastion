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
import { getCommand } from '@/api/command'
export default {
    props: ['commandList'],
    data() {
        return {
            tableQuery: {
                current: 1,
            },
            tableData: [],
            columns: [
                { title: '命令名称', dataIndex: 'command', ellipsis: true },
                {
                    title: '命令类型',
                    dataIndex: 'block_type',
                    ellipsis: true,
                    customRender: (text) => {
                        return text == 1 ? '命令阻断' : '命令提醒'
                    },
                },
                {
                    title: '提示内容',
                    dataIndex: 'block_info',
                    ellipsis: true,
                },
            ],
            tableLoading: false,
        }
    },
    methods: {
        //获取用户列表
        getCommand() {
            this.tableLoading = true
            const params = { all_data: 1 }
            getCommand(params)
                .then((res) => {
                    this.tableData = res.data.filter((item) => {
                        return this.commandList.filter((it) => it == item.id).length
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
        this.getCommand()
    },
}
</script>
<style scoped lang='less'>
</style>