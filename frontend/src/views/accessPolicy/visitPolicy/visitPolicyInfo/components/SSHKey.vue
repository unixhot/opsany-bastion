<template>
    <div>
        <a-table
            :loading="tableLoading"
            :dataSource="ssh_credential_host_id"
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
export default {
    props: ['ssh_credential_host_id'],
    data() {
        return {
            tableQuery: {
                current: 1,
            },
            tableData: [],
            columns: [
                { title: '凭证名称', dataIndex: 'credential.name', ellipsis: true },
                { title: '主机名称', dataIndex: 'host.host_name', ellipsis: true },
                {
                    title: 'IP地址',
                    dataIndex: 'host.host_address',
                    ellipsis: true,
                },
            ],
            tableLoading: false,
        }
    },
    methods: {
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
</style>