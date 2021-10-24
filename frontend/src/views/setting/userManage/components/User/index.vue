<template>
    <div>
        <div class="top_search">
            <div>
                <a-input-search
                    v-model="tableQuery.search_data"
                    @search="searchTable"
                    placeholder="请输入关键字搜索"
                    style="width: 300px"
                    allowClear
                >
                    <a-select slot="addonBefore" style="width: 100px" v-model="tableQuery.search_type">
                        <a-select-option v-for="item in searchList" :key="item.key">{{ item.name }}</a-select-option>
                    </a-select>
                </a-input-search>
            </div>
            <div>
                <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                <a-button icon="download" type="primary" @click="importUser">导入</a-button>
            </div>
        </div>
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
            :rowKey="(item) => item.username"
            :row-selection="{ selectedRowKeys, onChange: onSelectChange }"
        >
            <template slot="action" slot-scope="text, row">
                <a-button type="link" size="small" @click="del(row)">移除</a-button>
            </template>
        </a-table>
        <a-button
            v-if="!!tableData.length"
            :disabled="!selectedRowKeys.length"
            @click="del()"
            style="float: left; margin: -50px 10px 0 0"
            >批量移除</a-button
        >
        <ImportUser ref="ImportUser" @done="refresh"></ImportUser>
    </div>
</template>
<script>
import { getUserAdmin, delUserAdmin } from '@/api/user-admin'
import ImportUser from './components/ImportUser.vue'
export default {
    components: { ImportUser },
    data() {
        return {
            tableLoading: false,
            tableQuery: {
                search_data: undefined,
                search_type: 'username',
                current: 1,
                pageSize: 10,
                total: 0,
                data_type: 'list',
            },
            searchList: [
                { name: '用户名', key: 'username' },
                { name: '姓名', key: 'ch_name' },
            ],
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
                { title: '操作', ellipsis: true, scopedSlots: { customRender: 'action' }, align: 'center' },
            ],
            tableData: [],
            selectedRowKeys: [],
        }
    },
    methods: {
        searchTable() {
            this.tableQuery.current = 1
            this.getTableData()
        },
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys
        },
        getTableData() {
            this.tableLoading = true
            this.selectedRowKeys = []
            getUserAdmin({ ...this.tableQuery })
                .then((res) => {
                    const {
                        data: { data, current, total },
                    } = res
                    this.tableData = data
                    this.tableQuery.current = current
                    this.tableQuery.total = total
                    if (this.tableQuery.total > 0 && this.tableQuery.current > 1 && this.tableData.length == 0) {
                        this.tableQuery.current--
                        this.getTableData()
                    }
                })
                .finally(() => {
                    this.tableLoading = false
                })
        },
        importUser() {
            this.$refs.ImportUser.showModal()
        },
        refresh() {
            this.tableQuery = this.$options.data().tableQuery
            this.getTableData()
        },
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
            this.getTableData()
        },
        del(row) {
            const params = {
                user_list: row ? [row.username] : this.selectedRowKeys,
            }
            this.$confirm({
                title: '移除确认',
                content: '请确认是否移除?',
                okType: 'danger',
                onOk: () => {
                    return delUserAdmin(params).then((res) => {
                        this.$message.success('移除成功')
                        this.getTableData()
                    })
                },
            })
        },
    },
    mounted() {
        this.getTableData()
    },
}
</script>
<style scoped lang='less'>
.top_search {
    display: flex;
    justify-content: space-between;
    padding-bottom: 10px;
}
</style>