<template>
    <div class="operationLog_main">
        <ContentHeader>
            <div slot="docs">
                记录堡垒机用户的所有操作记录，用于进行安全审计和查看。
            </div>
        </ContentHeader>
        <a-card>
            <!-- <div class="search_box">
                <a-button @click="download()" style="float:right;" icon="download">导出</a-button>
            </div> -->
            <a-table :loading="tableLoading" @change="onChange" :pagination="pagination" :columns="columns" :data-source="tableData"></a-table>
        </a-card>
    </div>
</template>

<script>
import ContentHeader from "@/views/components/ContentHeader"
import { getOperationLog } from '@/api/session'
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
                { title: '操作用户', dataIndex: 'username' },
                { title: '操作类型', dataIndex: 'operation_type' },
                { title: '操作对象', dataIndex: 'operation_object', },
                { title: '执行时间', dataIndex: 'create_time' },
            ],
            searchList: [
                { name: '登录用户', key: 'user' },
                { name: '主机', key: 'server' },
            ],
        }
    },
    mounted() {
        this.getOperationLogData()
    },
    methods: {
        download() {

        },
        // 获取操作日志数据
        getOperationLogData() {
            this.tableLoading = true
            let updata = {
                current: this.pagination.current,
                pageSize: this.pagination.pageSize,
            }
            getOperationLog(updata).then(res => {
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
        },
        // 换页
        onChange(val) {
            this.pagination.total = val.total
            this.pagination.current = val.current
            this.pagination.pageSize = val.pageSize
            this.getOperationLogData()
        },
    },
    components: {
        ContentHeader,
    }
}
</script>

<style lang="less" scoped>
.operationLog_main {
    background: #fff;
    .search_box {
        height: 60px;
    }
}
</style>