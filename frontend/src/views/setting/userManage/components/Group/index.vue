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
                    <a-select slot="addonBefore" style="width: 110px" v-model="tableQuery.search_type">
                        <a-select-option v-for="item in searchList" :key="item.key">{{ item.name }}</a-select-option>
                    </a-select>
                </a-input-search>
            </div>
            <div>
                <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                <a-button
                    icon="plus"
                    type="primary"
                    @click="$refs.AuthModal.handleAuth('create-user-group').then(() => ControlGroup())"
                    >新建</a-button
                >
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
            :rowKey="(item) => item.id"
        >
            <template slot="user_list" slot-scope="text, row">
                <a-button type="link" size="small" @click="preview(row)">查看</a-button>
            </template>
            <template slot="action" slot-scope="text, row">
                <a-button
                    type="link"
                    size="small"
                    @click="
                        $refs.AuthModal.handleAuth('modify-user-group').then(() => $refs.ControlGroup.showModal(row))
                    "
                    >编辑</a-button
                >
                <a-button
                    type="link"
                    size="small"
                    @click="$refs.AuthModal.handleAuth('delete-user-group').then(() => delGroup(row))"
                    >删除</a-button
                >
            </template>
        </a-table>
        <ControlGroup ref="ControlGroup" @done="refresh"></ControlGroup>
        <PrevieUser ref="PrevieUser"></PrevieUser>
        <AuthModal ref="AuthModal"></AuthModal>
    </div>
</template>
<script>
import { getUserGroupAdmin, delUserGroupAdmin } from '@/api/user-group-admin'
import { getPageAuth } from '@/utils/pageAuth'
import ControlGroup from './components/ControlGroup.vue'
import PrevieUser from './components/PreviewUser.vue'
export default {
    components: { ControlGroup, PrevieUser },
    data() {
        return {
            tableLoading: false,
            tableQuery: {
                search_data: undefined,
                search_type: 'name',
                current: 1,
                pageSize: 10,
                total: 0,
                data_type: 'list',
            },
            searchList: [{ name: '用户组名称', key: 'name' }],
            columns: [
                { title: '用户组名称', dataIndex: 'name', ellipsis: true },
                {
                    title: '描述',
                    dataIndex: 'description',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
                },
                {
                    title: '用户组成员',
                    dataIndex: 'user_list',
                    ellipsis: true,
                    scopedSlots: { customRender: 'user_list' },
                    align: 'center',
                },
                {
                    title: '操作',
                    dataIndex: 'action',
                    ellipsis: true,
                    scopedSlots: { customRender: 'action' },
                    width: '250px',
                    align: 'center',
                },
            ],
            tableData: [],
        }
    },
    methods: {
        searchTable() {
            this.tableQuery.current = 1
            this.getTableData()
        },
        getTableData() {
            this.tableLoading = true
            getUserGroupAdmin({ ...this.tableQuery })
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
        preview({ name, user_list }) {
            this.$refs.PrevieUser.showModal(name, user_list)
        },
        ControlGroup() {
            this.$refs.ControlGroup.showModal()
        },
        refresh() {
            this.tableQuery = this.$options.data().tableQuery
            this.getTableData()
        },
        delGroup({ id }) {
            this.$confirm({
                title: '删除确认',
                content: '请确认是否删除?',
                okType: 'danger',
                onOk: () => {
                    return delUserGroupAdmin({ id }).then((res) => {
                        this.$message.success('删除成功')
                        this.getTableData()
                    })
                },
            })
        },
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
            this.getTableData()
        },
    },
    async mounted() {
        const hasAuth = await getPageAuth(this, 'get-user-group')
        if (hasAuth) {
            this.getTableData()
        }
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