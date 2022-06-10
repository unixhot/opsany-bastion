<template>
    <div>
        <content-header>
            <div slot="docs">
                通过策略授权将主机和应用资源、用户和用户组、资源和凭证进行关联，设置用户在什么时间，以什么凭证登录指定的主机或者应用。
            </div>
        </content-header>
        <a-card>
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
                            <a-select-option v-for="item in searchList" :key="item.key">{{
                                item.name
                            }}</a-select-option>
                        </a-select>
                    </a-input-search>
                    <!-- <a-button @click="visible = !visible" type="link">
                        高级搜索<a-icon :type="visible ? 'up' : 'down'"></a-icon>
                    </a-button> -->
                </div>
                <div>
                    <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                    <a-button
                        v-if="$store.state.btnAuth.btnAuth.bastion_access_strategy_create"
                        icon="plus"
                        type="primary"
                        @click="$refs.AuthModal.handleAuth('create-access-credential').then(() => add())"
                        >新建</a-button
                    >
                </div>
            </div>
            <search-box :visible="visible" class="search_box">
                <a-row type="flex" :gutter="[36]">
                    <a-col :xxl="8" :xl="12" :lg="12" :md="24" :sm="24" :xs="24"> </a-col>
                    <a-col :xxl="8" :xl="12" :lg="12" :md="24" :sm="24" :xs="24"> </a-col>
                    <a-col :xxl="8" :xl="12" :lg="12" :md="24" :sm="24" :xs="24"> </a-col>
                    <a-col :span="24" style="text-align: right">
                        <a-button @click="refresh">重置</a-button>
                        <a-button type="primary" style="margin-left: 10px" @click="searchTable">搜索</a-button>
                    </a-col>
                </a-row>
            </search-box>
            <a-table
                :defaultExpandAllRows="true"
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
                <template slot="name" slot-scope="text, row">
                    <a
                        :title="text"
                        type="link"
                        @click="$refs.AuthModal.handleAuth('get-access-credential').then(() => viewDetail(row))"
                        >{{ text }}</a
                    >
                </template>
                <template slot="status" slot-scope="text, row">
                    <a-switch
                        v-if="$store.state.btnAuth.btnAuth.bastion_access_strategy_on_off"
						:checked="row.status"
						:loading="row.stateLoading"
                        @click="$refs.AuthModal.handleAuth('modify-access-credential').then(() => changeStatus(row))"
                    ></a-switch>
                    {{ text ? '开启' : '关闭' }}
                </template>
                <template slot="userTitle">
                    <span>关联用户</span>
                    <a-tooltip placement="top" title="用户/用户组" arrow-point-at-center>
                        <a-icon style="margin: 0 0 0 3px; color: #666" type="exclamation-circle" />
                    </a-tooltip>
                </template>
                <template slot="user" slot-scope="text"> {{ text.user.length }}/{{ text.user_group.length }} </template>
                <template slot="voucherTitle">
                    <span>关联资源凭证</span>
                    <a-tooltip placement="top" title="密码凭证/SSH密钥/凭证分组" arrow-point-at-center>
                        <a-icon style="margin: 0 0 0 3px; color: #666" type="exclamation-circle" />
                    </a-tooltip>
                </template>
                <template slot="credential_host" slot-scope="text, row">
                    {{ text.password_credential_host_id.length }}/{{ text.ssh_credential_host_id.length }}/{{
                        text.credential_group.length
                    }}
                </template>
                <template slot="action" slot-scope="text, row">
                    <a-button
                        type="link"
                        size="small"
                        @click="$refs.AuthModal.handleAuth('get-access-credential').then(() => viewDetail(row))"
                        >查看</a-button
                    >
                    <a-button
                        type="link"
                        size="small"
                        v-if="$store.state.btnAuth.btnAuth.bastion_access_strategy_update"
                        @click="$refs.AuthModal.handleAuth('modify-access-credential').then(() => edit(row))"
                        >编辑</a-button
                    >
                    <a-button
                        type="link"
                        size="small"
                        v-if="$store.state.btnAuth.btnAuth.bastion_access_strategy_delete"
                        @click="$refs.AuthModal.handleAuth('delete-access-credential').then(() => del(row))"
                        >删除</a-button
                    >
                </template>
            </a-table>
            <ControlVisitPolicy ref="ControlVisitPolicy" @done="getTableData"></ControlVisitPolicy>
            <AuthModal ref="AuthModal"></AuthModal>
        </a-card>
    </div>
</template>
<script>
import ControlVisitPolicy from './components/ControlVisitPolicy.vue'
import { getAccessStrategy, delAccessStrategy, editAccessStrategyStatus } from '@/api/access-strategy'
import { getPageAuth } from '@/utils/pageAuth'
export default {
    components: { ControlVisitPolicy },
    data() {
        return {
            tableLoading: false,
            visible: false,
            tableQuery: {
                search_data: undefined,
                search_type: 'name',
                current: 1,
                pageSize: 10,
                total: 0,
                data_type: 'list',
                status: undefined,
                call_type: undefined,
                execute_type: undefined,
            },
            searchList: [{ name: '策略名称', key: 'name' }],
            tableData: [],
            columns: [
                { title: '策略名称', dataIndex: 'name', ellipsis: true, scopedSlots: { customRender: 'name' } },
                { title: '状态', dataIndex: 'status', ellipsis: true, scopedSlots: { customRender: 'status' } },
                {
                    dataIndex: 'user',
                    ellipsis: true,
                    slots: { title: 'userTitle' },
                    scopedSlots: { customRender: 'user' },
                },
                {
                    dataIndex: 'credential_host',
                    ellipsis: true,
                    slots: { title: 'voucherTitle' },
                    scopedSlots: { customRender: 'credential_host' },
                },
                { title: '创建时间', dataIndex: 'create_time', ellipsis: true },
                { title: '操作', ellipsis: true, scopedSlots: { customRender: 'action' }, align: 'center' },
            ],
        }
    },
    methods: {
        searchTable() {
            this.tableQuery.current = 1
            this.getTableData()
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
        //查看详情
        viewDetail(row) {
            this.$router.push({ name: 'visitPolicyInfo', query: { id: row.id } })
        },
        add() {
            this.$refs.ControlVisitPolicy.showModal()
        },
        edit(row) {
            this.$refs.ControlVisitPolicy.showModal(row.id)
        },
        del({ id }) {
            this.$confirm({
                title: '删除确认',
                content: '请确认是否删除?',
                okType: 'danger',
                onOk: () => {
                    return delAccessStrategy({ id }).then((res) => {
                        this.$message.success('删除成功')
                        this.getTableData()
                    })
                },
            })
        },
        changeStatus(row) {
            const params = {
                id: row.id,
                status: !row.status,
                type: 'access',
            }
			row.stateLoading = true
            editAccessStrategyStatus(params).then((res) => {
                this.getTableData()
            }).finally(() => {
				row.stateLoading = false
			})
        },
        getTableData() {
            this.tableLoading = true
            getAccessStrategy({ ...this.tableQuery })
                .then((res) => {
                    const {
                        data: { data, current, total },
                    } = res
                    this.tableData = data
                    this.tableQuery.current = current
                    this.tableQuery.total = total
                    this.tableData.forEach((item) => {
                        this.$set(item, 'stateLoading', false)
                    })
                    if (this.tableQuery.total > 0 && this.tableQuery.current > 1 && this.tableData.length == 0) {
                        this.tableQuery.current--
                        this.getTableData()
                    }
                })
                .finally(() => {
                    this.tableLoading = false
                })
        },
    },
    async mounted() {
        const hasAuth = await getPageAuth(this, 'use-access-credential')
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
.search_box {
    margin-bottom: 10px;
}
</style>