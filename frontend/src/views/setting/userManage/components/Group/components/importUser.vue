<template>
    <div>
        <a-modal title="添加组成员" :visible="visible" @ok="handleOk" @cancel="handleCancel" width="900px">
            <div class="top_search">
                <div>
                    <a-input-search
                        v-model.trim="tableQuery.search_data"
                        @search="searchTable"
                        placeholder="请输入关键字搜索"
                        style="width: 300px"
                        allowClear
                    >
                        <a-select slot="addonBefore" style="width: 100px" v-model="tableQuery.search_type">
                            <a-select-option v-for="item in searchList" :key="item.key">{{
                                item.name
                            }}</a-select-option>
                        </a-select>
                    </a-input-search>
                </div>
                <div>
                    <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                </div>
            </div>
            <a-table
                :dataSource="tableData"
                :columns="columns"
                :pagination="{
                    ...tableQuery,
                    showTotal: (total) => `共 ${total} 条数据`,
                    showQuickJumper: true,
                }"
                @change="tableChange"
                :rowKey="(item) => item.username"
                :row-selection="{ selectedRowKeys, onChange: onSelectChange }"
                :loading="tableLoading"
            >
            </a-table>
            <a-button
                v-if="!!tableData.length"
                :disabled="!tableData.length"
                @click="checkAll"
                style="float: left; margin: -50px 10px 0 0"
                >批量全选</a-button
            >
        </a-modal>
    </div>
</template>
<script>
import { getUserAdmin } from '@/api/user-admin'
export default {
    data() {
        return {
            tableQuery: {
                current: 1,
                pageSize: 99999,
                total: 0,
                data_type: 'list',
                search_data: undefined,
                search_type: 'username',
            },
            searchList: [
                { name: '用户名', key: 'username' },
                { name: '姓名', key: 'ch_name' },
            ],
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
            selectedRowKeys: [],
            tableLoading: false,
        }
    },
    methods: {
        showModal() {
            this.visible = true
			this.tableQuery = this.$options.data().tableQuery
            this.getTableData()
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
        searchTable() {
            this.tableQuery.current = 1
            this.getTableData()
        },
        refresh() {
            this.selectedRowKeys = []
            this.tableQuery = this.$options.data().tableQuery
            this.searchTable()
        },
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys
        },
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
        },
        checkAll() {
            if (this.selectedRowKeys.length == this.tableData.length) {
                this.selectedRowKeys = []
                return
            }
            this.selectedRowKeys = this.tableData.map((item) => item.username)
        },
        handleOk() {
            const selectRows = this.tableData.filter((item) => {
                return this.selectedRowKeys.filter((it) => item.username == it).length
            })
            this.$emit('done', selectRows)
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
.top_search {
    display: flex;
    justify-content: space-between;
    padding-bottom: 10px;
}
</style>