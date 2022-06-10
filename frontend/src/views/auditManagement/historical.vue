<template>
    <div class="history_main">
        <ContentHeader>
            <div slot="docs">所有堡垒机登录的会话，审计查看可以播放会话的执行详情，用于做安全审核。</div>
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
                :columns="columns"
                :data-source="tableData"
            >
                <template slot="action" slot-scope="text, record">
                    <a
                        style="margin: 0 10px 0 0"
                        @click="$refs.AuthModal.handleAuth('play-history').then(() => preview(record))"
                        >播放历史</a
                    >
                    <a
                        :disabled="record.system_type != 'Linux'"
                        @click="
                            $refs.AuthModal.handleAuth('get-history').then(() =>
                                $router.push({
                                    path: '/auditManagement/historical/historicalDetails',
                                    query: { id: record.id },
                                })
                            )
                        "
                        >查看详情</a
                    >
                </template>
            </a-table>
        </a-card>
        <WindowsPlayer ref="WindowsPlayer"></WindowsPlayer>
        <PlayerModel ref="PlayerModel"></PlayerModel>
        <AuthModal ref="AuthModal"></AuthModal>
    </div>
</template>

<script>
import ContentHeader from '@/views/components/ContentHeader'
import { getSessionLog, sshKill } from '@/api/session'
import WindowsPlayer from './components/windowsPlayer'
import PlayerModel from './components/playerModel'
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
        }
    },
    async mounted() {
        const hasAuth = await getPageAuth(this, 'visit-history-session')
        if (hasAuth) {
            this.getSessionLogData()
        }
    },
    methods: {
        // 审计查看
        preview(row) {
            if (row.system_type == 'Windows') return this.$refs.WindowsPlayer.show(row.log_name)
            const file_name = row.log_name
            this.$refs.PlayerModel.show(file_name)
        },
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getSessionLogData()
        },
        // 获取会话数据
        getSessionLogData() {
            this.tableLoading = true
            let updata = {
                current: this.pagination.current,
                pageSize: this.pagination.pageSize,
                finished: 1,
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
                    } else {
                        this.tableData = []
                    }
                })
                .finally(() => {
                    this.tableLoading = false
                })
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
    },
    components: {
        ContentHeader,
        WindowsPlayer,
        PlayerModel,
    },
}
</script>
<style lang="less" scoped>
.history_main {
    background: #fff;
    .search_box {
        height: 60px;
    }
}
</style>