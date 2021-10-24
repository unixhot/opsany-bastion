<template>
    <div>
        <a-table
            :loading="tableLoading"
            :dataSource="credential_group"
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
    props: ['credential_group'],
    data() {
        return {
            tableQuery: {
                current: 1,
            },
            tableData: [],
            columns: [
                { title: '名称', dataIndex: 'name', ellipsis: true },
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