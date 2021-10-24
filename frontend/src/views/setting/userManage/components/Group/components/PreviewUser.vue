<template>
    <div>
        <a-modal :title="title" :visible="visible" @ok="handleOk" @cancel="handleCancel" width="900px">
            <a-table
                :dataSource="tableData"
                :columns="columns"
                :pagination="{
                    ...tableQuery,
                    showSizeChanger: true,
                    showTotal: (total) => `共 ${total} 条数据`,
                    showQuickJumper: true,
                }"
                @change="tableChange"
                :rowKey="(item) => item.username"
            >
            </a-table>
        </a-modal>
    </div>
</template>
<script>
export default {
    data() {
        return {
            tableQuery: {
                current: 1,
                pageSize: 10,
                total: 0,
            },
            title: '',
            tableData: [],
            visible: false,
            columns: [
                { title: '用户名', dataIndex: 'username', ellipsis: true },
                {
                    title: '姓名',
                    dataIndex: 'ch_name',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
                },
                {
                    title: '联系方式',
                    dataIndex: 'phone',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
                },
                {
                    title: '邮箱',
                    dataIndex: 'email',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
                },
				   {
                    title: '用户类型',
                    dataIndex: 'role',
                    ellipsis: true,
                    customRender: (text) => {
                        return text == 0 ? '普通用户' : text == 1 ? '管理员' : text == 2 ? '开发者' : ''
                    },
                },
            ],
            tableData: [],
        }
    },
    methods: {
        showModal(title, user_list) {
            this.title = title
            this.tableData = user_list
            this.visible = true
        },
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
        },
        handleOk() {
            this.visible = false
        },
        handleCancel() {
            this.visible = false
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
</style>