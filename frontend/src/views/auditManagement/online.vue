<template>
    <div class="online_main">
        <ContentHeader>
            <div slot="docs">当前正在使用堡垒机的登录会话，操作强制下线会中断用户的当前请求链接。</div>
        </ContentHeader>
        <a-card>
            <div class="search_box">
                <a-input-search
                    v-model="pagination.search_data"
                    @search="searchTable"
                    placeholder="请输入关键字搜索"
                    style="width: 300px"
                    allowClear
                >
                    <a-select slot="addonBefore" style="width: 100px" v-model="pagination.search_type">
                        <a-select-option v-for="item in searchList" :key="item.key">{{ item.name }}</a-select-option>
                    </a-select>
                </a-input-search>
                <a-button @click="refresh" style="float: right" icon="reload">刷新</a-button>
            </div>
            <a-table
                :loading="tableLoading"
                @change="onChange"
                :pagination="pagination"
                :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }"
                :columns="columns"
                :data-source="tableData"
            >
                <template slot="action" slot-scope="text, record">
                    <a
                        v-if="$store.state.btnAuth.btnAuth.bastion_session_off_line"
                        @click="$refs.AuthModal.handleAuth('logout-session').then(() => offline(record))"
                        >强制下线</a
                    >
                </template>
            </a-table>
            <a-button
                v-if="tableData.length > 0"
                :disabled="selectedRow.length == 0"
                icon="delete"
                @click="$refs.AuthModal.handleAuth('logout-session').then(() => batchDelete())"
                style="float: left; margin: -50px 10px 0 0"
                >批量下线</a-button
            >
        </a-card>
        <AuthModal ref="AuthModal"></AuthModal>
    </div>
</template>

<script>
import ContentHeader from '@/views/components/ContentHeader'
import { getSessionLog, delSessionLog } from '@/api/session'
import { getPageAuth } from '@/utils/pageAuth'
export default {
    data() {
        return {
            tableData: [],
            pagination: {
                total: 0,
                current: 1,
                pageSize: 10,
                showTotal: (total) => `共有 ${total} 条数据`,
                search_type: 'user',
                search_data: undefined,
                showSizeChanger: true,
                showQuickJumper: true,
            },
            tableLoading: false,
            columns: [
                { title: '登录用户', dataIndex: 'user' },
                { title: '主机', dataIndex: 'host_name' },
                { title: 'IP地址', dataIndex: 'host_address', width: '170px' },
                { title: '系统用户', dataIndex: 'login_name' },
                { title: '开始时间', dataIndex: 'start_time' },
                {
                    title: '操作',
                    key: 'action',
                    scopedSlots: { customRender: 'action' },
                    align: 'center',
                },
            ],
            searchList: [
                { name: '登录用户', key: 'user' },
                { name: '主机', key: 'server' },
            ],
            selectedRowKeys: [],
            selectedRow: [],
        }
    },
    async mounted() {
        const hasAuth = await getPageAuth(this, 'visit-online-session')
        if (hasAuth) {
            this.getSessionLogData()
        }
    },
    methods: {
        // table选择
        onSelectChange(selectedRowKeys, selectedRow) {
            this.selectedRow = selectedRow
            this.selectedRowKeys = selectedRowKeys
        },
        // 获取会话数据
        getSessionLogData() {
            this.tableLoading = true
            let updata = {
                current: this.pagination.current,
                pageSize: this.pagination.pageSize,
            }
            if (this.pagination.search_data) {
                if (this.pagination.search_type == 'server') {
                    updata.search_type = 'host__host_name'
                } else {
                    updata.search_type = this.pagination.search_type
                }
                updata.search_data = this.pagination.search_data
            }
            getSessionLog(updata)
                .then((res) => {
                    if (res.code == 200 && res.data) {
                        this.pagination.total = res.data.total
                        this.pagination.current = res.data.current
                        this.pagination.pageSize = res.data.pageSize
                        res.data.data.map((item) => {
                            item.key = item.id
                        })
                        this.tableData = res.data.data
                        this.selectedRow = []
                    } else {
                        this.tableData = []
                    }
                })
                .finally(() => {
                    this.tableLoading = false
                })
        },
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getSessionLogData()
        },
        refresh() {
            this.getSessionLogData()
        },
        // 换页
        onChange(val) {
            this.pagination.total = val.total
            this.pagination.current = val.current
            this.pagination.pageSize = val.pageSize
            this.getSessionLogData()
        },
        // 下线
        offline(row) {
            let params = {
                log_name: row.log_name,
                channel: row.channel,
            }

            this.$confirm({
                title: '强制下线确认',
                content: '请确认是否强制下线此连接?',
                okType: 'danger',
                onOk: () => {
                    delSessionLog({ session_list: [params] }).then((res) => {
                        this.$message.success('操作成功')
                        this.getSessionLogData()
                    })
                },
            })
        },
        // 批量删除
        batchDelete() {
            let _this = this
            this.$confirm({
                title: '确认删除该分组吗？',
                onOk: function () {
                    let arr = []
                    _this.selectedRow.map((item) => {
                        arr.push({
                            log_name: item.log_name,
                            channel: item.channel,
                        })
                    })
                    delSessionLog({ session_list: arr }).then((res) => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getSessionLogData()
                            _this.selectedRowKeys = []
                        }
                    })
                },
            })
        },
    },
    components: {
        ContentHeader,
    },
}
</script>

<style lang="less" scoped>
.online_main {
    background: #fff;
    .search_box {
        height: 60px;
    }
}
</style>