<template>
    <div class="main">
        <content-header>
            <a-button slot="right" icon="arrow-left" type="primary" @click="$router.go(-1)">返回</a-button>
        </content-header>
        <div class="content">
            <a-card class="infomation" title="基础信息">
                <p class="info">
                    <span>主机名：{{infomation.host_name}}</span>
                    <span>IP地址：{{infomation.host_address}}</span>
                    <span>系统类型：{{infomation.system_type}}</span>
                    <span>协议类型：{{infomation.protocol_type}}</span>
                </p>
                <p class="info">
                    <span>端口：{{infomation.port}}</span>
                    <span>系统用户：{{infomation.login_name}}</span>
                    <span>开始时间：{{infomation.start_time}}</span>
                    <span></span>
                </p>
            </a-card>

            <a-card title="命令历史">
                <div class="search_box">
                    <a-input-search v-model="pagination.search_data" @search="searchTable" placeholder="请输入关键字搜索" style="width: 300px" allowClear>
                        <a-select slot="addonBefore" style="width: 100px" v-model="pagination.search_type">
                            <a-select-option v-for="item in searchList" :key="item.key">{{
                                item.name
                            }}</a-select-option>
                        </a-select>
                    </a-input-search>
                </div>

                <a-table :loading="tableLoading" :columns="columns" :data-source="tableData">
                    <template slot="action" slot-scope="text,record">
                        <a @click="remove(record)">移除</a>
                    </template>
                </a-table>
            </a-card>

        </div>
    </div>
</template>

<script>
import { getSessionLog, getSessionHistory } from "@/api/session"
export default {
    data() {
        return {
            infomation: {},
            tableData: [],
            columns: [
                {
                    title: '命令名称',
                    dataIndex: 'command',
                },
                {
                    title: '开始时间',
                    dataIndex: 'create_time',
                    width:200
                },
            ],
            pagination: {
                total: 0, current: 1, pageSize: 10, showTotal: total => `共有 ${total} 条数据`, search_type: "command", search_data: undefined,
                showSizeChanger: true, showQuickJumper: true,
            },
            searchList: [
                { name: '命令名称', key: 'command' },

            ],
            tableLoading:false,
        }
    },
    mounted() {
        this.getSessionLogData()
        this.getSessionHistoryData()
    },
    methods: {
        // 获取基本信息
        getSessionLogData() {
            getSessionLog({ id: this.$route.query.id }).then(res => {
                if (res.code == 200 && res.data) {
                    this.infomation = res.data
                }
            })
        },
        // 获取操作记录
        getSessionHistoryData() {
            this.tableLoading=true
            let updata = {
                session_log_id: this.$route.query.id,
            }
            if (this.pagination.search_data) {
                updata.search_type = this.pagination.search_type
                updata.search_data = this.pagination.search_data
            }
            getSessionHistory(updata).then(res => {
                if (res.code == 200 && res.data) {
                    res.data.map(item => {
                        item.key = item.id
                    })
                    this.tableData = res.data
                } else {
                    this.tableData = []
                }
            }).finally(()=>{
                this.tableLoading=false
            })
        },
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getSessionHistoryData()
        },
    }
}
</script>
<style lang="less" scoped>
.main {
    background: #fff;
}
.search_box{
    margin:0 0 20px 0;
}
.content {
    padding: 20px;
    .infomation {
        margin: 0 0 20px 0;
        .info {
            display: flex;
            justify-content: space-between;

            span {
                flex: 0px 1 1;
            }
        }
    }
}
</style>