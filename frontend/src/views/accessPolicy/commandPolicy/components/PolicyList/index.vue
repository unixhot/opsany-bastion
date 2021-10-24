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
                <!-- <a-button @click="visible = !visible" type="link">
                        高级搜索<a-icon :type="visible ? 'up' : 'down'"></a-icon>
                    </a-button> -->
            </div>
            <div>
                <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_command_strategy_create" icon="plus" type="primary" @click="add">新建</a-button>
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
                <a :title="text" type="link" @click="viewDetail(row)">{{ text }}</a>
            </template>
            <template slot="status" slot-scope="text, row">
                <a-switch v-if="$store.state.btnAuth.btnAuth.bastion_command_strategy_on_off" v-model="row.status" @click="changeStatus(row)"></a-switch> {{ text ? '开启' : '关闭' }}
            </template>
            <template slot="command" slot-scope="text, row">
                {{ text.command.length }}/{{ text.command_group.length }}
            </template>
            <template slot="user" slot-scope="text, row">
                {{ text.user.length }}/{{ text.user_group.length }}
            </template>
            <template slot="credential_host" slot-scope="text, row">
                {{ text.password_credential_host_id.length }}/{{ text.ssh_credential_host_id.length }}/{{
                    text.credential_group.length
                }}
            </template>
            <template slot="action" slot-scope="text, row">
                <a-button type="link" size="small" @click="viewDetail(row)">查看</a-button>
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_command_strategy_update" type="link" size="small" @click="edit(row)">编辑</a-button>
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_command_strategy_delete" type="link" size="small" @click="del(row)">删除</a-button>
            </template>
        </a-table>
        <ControlPolicy ref="ControlPolicy" @done="getTableData"></ControlPolicy>
    </div>
</template>
<script>
import ControlPolicy from './components/ControlPolicy.vue'
import { getCommandStrategy, delCommandStrategy } from '@/api/command-strategy'
import { editAccessStrategyStatus } from '@/api/access-strategy'
export default {
    components: { ControlPolicy },
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
                    title: '关联命令',
                    dataIndex: 'command',
                    ellipsis: true,
                    scopedSlots: { customRender: 'command' },
                },
                { title: '关联用户', dataIndex: 'user', ellipsis: true, scopedSlots: { customRender: 'user' } },
                {
                    title: '关联资源凭证',
                    dataIndex: 'credential_host',
                    ellipsis: true,
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
            this.$router.push({ name: 'policyListInfo', query: { id: row.id } })
        },
        add() {
            this.$refs.ControlPolicy.showModal()
        },
        edit(row) {
            this.$refs.ControlPolicy.showModal(row.id)
        },
        del({ id }) {
            this.$confirm({
                title: '删除确认',
                content: '请确认是否删除?',
                okType: 'danger',
                onOk: () => {
                    return delCommandStrategy({ id }).then((res) => {
                        this.$message.success('删除成功')
                        this.getTableData()
                    })
                },
            })
        },
        changeStatus(row) {
            const params = {
                id: row.id,
                status: row.status,
                type: 'command',
            }
            editAccessStrategyStatus(params).then((res) => {
                this.getTableData()
            })
        },
        getTableData() {
            this.tableLoading = true
            getCommandStrategy({ ...this.tableQuery })
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
.search_box {
    margin-bottom: 10px;
}
</style>