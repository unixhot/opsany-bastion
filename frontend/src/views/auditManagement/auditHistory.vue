<template>
    <div class="auditHistory_main">
        <ContentHeader>
            <div slot="docs">
                记录所有危险命令的执行情况，用于进行规范化管理和快速查询。
            </div>
        </ContentHeader>
        <a-card>
            <div class="search_box">
                <a-input-search v-model="pagination.search_data" @search="searchTable" placeholder="请输入关键字搜索" style="width: 300px" allowClear>
                    <a-select slot="addonBefore" style="width: 100px" v-model="pagination.search_type">
                        <a-select-option v-for="item in searchList" :key="item.key">{{
                                item.name
                            }}</a-select-option>
                    </a-select>
                </a-input-search>
                <a-button @click="refresh" style="float:right;" icon="reload">刷新</a-button>
            </div>
            <a-table :loading="tableLoading" @change="onChange" :pagination="pagination" :columns="columns" :data-source="tableData">
                <template slot="status" slot-scope="status">
                    <a-tag :color="status == 'y' ? 'green' : 'pink'"> {{ status == 'y' ? '已执行' : '未执行' }} </a-tag>
                </template>
                <template slot="block_type" slot-scope="text">
                    {{text=="confirm"?"指令提醒":"指令阻断"}}
                </template>
            </a-table>
        </a-card>
    </div>
</template>

<script>
import ContentHeader from "@/views/components/ContentHeader"
import { getCommandHistory } from '@/api/session'
export default {
    data() {
        return {
            tableData: [],
            pagination: {
                total: 0, current: 1, pageSize: 10, showTotal: total => `共有 ${total} 条数据`, search_type: "user", search_data: undefined,
                showSizeChanger: true, showQuickJumper: true,
            },
            tableLoading: false,
            columns: [
                { title: '操作用户/执行用户', dataIndex: 'user', ellipsis: true, },
                { title: '执行主机', dataIndex: 'hostname', ellipsis: true, },
                { title: '执行状态', dataIndex: 'status', ellipsis: true, scopedSlots: { customRender: 'status' }, },
                { title: '指令类型', dataIndex: 'block_type', ellipsis: true, scopedSlots: { customRender: 'block_type' }, },
                { title: '执行时间', dataIndex: 'create_time', ellipsis: true, },
                { title: '指令名称', dataIndex: 'intercept_command', ellipsis: true, },
                { title: '命令内容', dataIndex: 'command', ellipsis: true, },
            ],


            searchList: [
                { name: '登录用户', key: 'user' },
                // { name: '主机', key: 'server' },
            ],
            blockTypeList: [
                { value: 'confirm', label: '指令提醒' },
                { value: 'cancle', label: '指令阻断' },
            ],
        }
    },
    mounted() {
        this.getCommandHistoryData()
    },
    methods: {
        // 换页
        onChange(val) {
            this.pagination.total = val.total
            this.pagination.current = val.current
            this.pagination.pageSize = val.pageSize
            this.getCommandHistoryData()
        },
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getCommandHistoryData()
        },
        refresh() {
            this.getSessionLogData()
        },
        // 获取审计历史数据
        getCommandHistoryData() {
            this.tableLoading = true
            let updata = {
                current: this.pagination.current,
                pageSize: this.pagination.pageSize,
            }
            if (this.pagination.search_data) {
                if (this.pagination.search_type == "server") {
                    updata.search_type = "host__host_name"
                } else {
                    updata.search_type = this.pagination.search_type
                }
                updata.search_data = this.pagination.search_data
            }
            getCommandHistory(updata).then(res => {
                if (res.code == 200 && res.data) {
                    this.pagination.total = res.data.total
                    this.pagination.current = res.data.current
                    this.pagination.pageSize = res.data.pageSize
                    res.data.data.map(item => {
                        item.key = item.id
                    })
                    this.tableData = res.data.data
                } else {
                    this.tableData = []
                }
            }).finally(() => {
                this.tableLoading = false
            })
        }
    },
    components: {
        ContentHeader,
    }
}
</script>

<style lang="less" scoped>
.auditHistory_main {
    background: #fff;
    .search_box {
        height: 60px;
    }
}
</style>