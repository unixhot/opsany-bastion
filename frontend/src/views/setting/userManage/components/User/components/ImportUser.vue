<template>
    <div>
        <a-drawer
            title="导入用户"
            :width="1220"
            :visible="visible"
            :body-style="{ paddingBottom: '80px' }"
            @close="handleCancel"
        >
            <div class="content_box">
                <div class="right_tree">
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
                        :defaultExpandAllRows="true"
                        :dataSource="tableData"
                        :columns="columns"
                        :pagination="{
                            ...tableQuery,
                            showSizeChanger: true,
                            showTotal: (total) => `共 ${total} 条数据`,
                            showQuickJumper: true,
                        }"
                        :row-selection="{
                            selectedRowKeys: selectedRowKeys,
                            onChange: onSelectChange,
                            getCheckboxProps: (row) => ({
                                props: {
                                    disabled: row.is_import,
                                },
                            }),
                        }"
                        @change="tableChange"
                        :rowKey="(item) => item.username"
                        :loading="treeLoading"
                    >
                        <template slot="action" slot-scope="text, row">
                            <a-button
                                type="link"
                                size="small"
                                @click="importUser(row)"
                                :loading="row.loading"
                                :disabled="row.is_import"
                                >导入</a-button
                            >
                        </template>
                    </a-table>
                    <!-- <a-button
                        v-if="!!tableData.length"
                        :disabled="!tableData.length"
                        @click="checkAll"
                        style="float: left; margin: -50px 10px 0 0"
                        >批量全选</a-button
                    > -->
                </div>
            </div>

            <div class="bottom_btns">
                <a-tooltip placement="topLeft" v-if="!!tableData.length" :style="{ marginRight: '8px' }">
                    <template slot="title">
                        <span>点击将导入{{ tableQuery.total }}个用户,此操作会耗费较长时间,请耐心等待。</span>
                    </template>
                    <a-button @click="importAll" :loading="importLoading">全部导入</a-button>
                </a-tooltip>
                <a-button :style="{ marginRight: '8px' }" @click="handleCancel"> 取消 </a-button>
                <a-tooltip placement="topLeft" v-if="!!tableData.length" :style="{ marginRight: '8px' }">
                    <template slot="title">
                        <span>点击将导入已选中的用户。</span>
                    </template>
                    <a-button type="primary" @click="handleOk" :loading="loading"> 导入 </a-button>
                </a-tooltip>
            </div>
        </a-drawer>
    </div>
</template>
<script>
import { getUserAdmin, addUserAdmin } from '@/api/user-admin'
export default {
    data() {
        return {
            visible: false,
            loading: false,
            treeLoading: false,
            importLoading: false,
            tableQuery: {
                search_data: undefined,
                search_type: 'username',
                current: 1,
                pageSize: 10,
                total: 0,
                data_type: 'import',
            },
            selectedRowKeys: [],
            searchList: [
                { name: '用户名', key: 'username' },
                { name: '姓名', key: 'display_name' },
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
                    title: '邮箱',
                    dataIndex: 'email',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
                },
                { title: '操作', ellipsis: true, scopedSlots: { customRender: 'action' }, align: 'center' },
            ],
            tableData: [],
        }
    },
    methods: {
        searchTable() {
            this.tableQuery.current = 1
            this.selectedRowKeys = []
            this.getTableData()
        },
        showModal() {
            this.tableData = []
            this.selectedRowKeys = []
            this.tableQuery = this.$options.data().tableQuery
            this.visible = true
            this.getTableData()
        },
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys
        },
        getTableData() {
            this.treeLoading = true
            getUserAdmin({ ...this.tableQuery })
                .then((res) => {
                    this.tableData = res.data.data
                    this.tableQuery.total = res.data.total
                })
                .finally(() => {
                    this.treeLoading = false
                })
        },
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
            this.selectedRowKeys = []
            this.getTableData()
        },
        refresh() {
            this.selectedRowKeys = []
            this.tableQuery = this.$options.data().tableQuery
            this.searchTable()
        },
        checkAll() {
            if (this.selectedRowKeys.length == this.tableData.length) {
                this.selectedRowKeys = []
                return
            }
            this.selectedRowKeys = this.tableData.map((item) => item.username)
        },
        //全部导入
        importAll() {
			const hide = this.$message.loading('正在同步导入中...')
            this.importLoading = true
            addUserAdmin({ import_type: 'all' })
                .then((res) => {
                    this.selectedRowKeys = []
                    this.$emit('done')
                    this.$message.success(res.message)
                    this.getTableData()
                    this.visible = false
                })
                .finally(() => {
                    this.importLoading = false
					hide()
                })
        },
        handleCancel(e) {
            this.visible = false
        },
        handleOk() {
            this.loading = true
            addUserAdmin({ username_list: this.selectedRowKeys })
                .then((res) => {
                    this.selectedRowKeys = []
                    this.$emit('done')
                    this.$message.success(res.message)
                    this.getTableData()
                })
                .finally(() => {
                    this.loading = false
                    this.visible = false
                })
        },
        //
        importUser(row) {
            this.$set(row, 'loading', true)
            addUserAdmin({ username_list: [row.username] })
                .then((res) => {
                    this.selectedRowKeys = []
                    this.$emit('done')
                    this.$message.success(res.message)
                    this.getTableData()
                })
                .finally(() => {
                    this.$set(row, 'loading', false)
                })
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
.content_box {
    display: flex;
    .left_tree {
        flex: 250px 0 0;
        border-right: 1px solid #eeeeee;
        padding: 0 10px;
        overflow: hidden;
    }
    .right_tree {
        flex: 0 1 1;
        padding: 0 10px;
    }
}
.top_search {
    display: flex;
    justify-content: space-between;
    padding-bottom: 10px;
}
.bottom_btns {
    position: absolute;
    right: 0;
    bottom: 0;
    width: 100%;
    border-top: 1px solid #e9e9e9;
    padding: 10px 16px;
    background: #fff;
    text-align: right;
    z-index: 1;
}
</style>