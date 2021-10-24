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
                    <a-select slot="addonBefore" style="width: 120px" v-model="tableQuery.search_type">
                        <a-select-option v-for="item in searchList" :key="item.key">{{ item.name }}</a-select-option>
                    </a-select>
                </a-input-search>
                <!-- <a-button @click="visible = !visible" type="link">
                        高级搜索<a-icon :type="visible ? 'up' : 'down'"></a-icon>
                    </a-button> -->
            </div>
            <div>
                <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_command_group_create" icon="plus" type="primary" @click="add">新建</a-button>
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
                <!-- <a type="link" @click="viewDetail(row)">{{ text }}</a> -->
                {{ text }}
            </template>
            <template slot="user" slot-scope="text, row">
                {{ text.user.length }}/{{ text.user_group.length }}
            </template>
            <template slot="credential" slot-scope="text, row">
                {{ text.password_credential.length }}/{{ text.ssh_credential.length }}/{{
                    text.credential_group.length
                }}
            </template>
            <template slot="action" slot-scope="text, row">
                <!-- <a-button type="link" @click="viewDetail(row)">查看</a-button> -->
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_command_group_update" type="link" size="small" @click="edit(row)">编辑</a-button>
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_command_group_delete" type="link" size="small" @click="del(row)">删除</a-button>
            </template>
        </a-table>
        <ControlCommandGroup ref="ControlCommandGroup" @done="getTableData"></ControlCommandGroup>
    </div>
</template>
<script>
import ControlCommandGroup from './components/ControlCommandGroup'
import { getCommandGroup, delCommandGroup } from '@/api/command-group'
export default {
    components: { ControlCommandGroup },
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
            },
            searchList: [{ name: '命令组名称', key: 'name' }],
            tableData: [],
            columns: [
                { title: '命令组名称', dataIndex: 'name', ellipsis: true },
                {
                    title: '描述',
                    dataIndex: 'description',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
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
            // this.$router.push({ name: 'visitPolicyInfo', query: { id: row.id } })
        },
        add() {
            this.$refs.ControlCommandGroup.showModal()
        },
        edit(row) {
            this.$refs.ControlCommandGroup.showModal(row)
        },
        del({ id }) {
            this.$confirm({
                title: '删除确认',
                content: '请确认是否删除?',
                okType: 'danger',
                onOk: () => {
                    return delCommandGroup({ id }).then((res) => {
                        this.$message.success('删除成功')
                        this.getTableData()
                    })
                },
            })
        },
        getTableData() {
            this.tableLoading = true
            getCommandGroup({ ...this.tableQuery })
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