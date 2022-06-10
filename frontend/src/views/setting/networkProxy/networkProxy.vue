<template>
    <div>
        <content-header>
            <div slot="docs">通过增加网络代理，堡垒机可以管理不同网络内的主机和数据库资源。</div>
        </content-header>
        <a-card>
            <div class="top_search">
                <div>
                    <a-input-search
                        v-model="tableQuery.search_data"
                        @search="searchTable"
                        placeholder="请输入关键字搜索"
                        style="width: 350px"
                        allowClear
                    >
                        <a-select slot="addonBefore" style="width: 150px" v-model="tableQuery.search_type">
                            <a-select-option v-for="item in searchList" :key="item.key">{{
                                item.name
                            }}</a-select-option>
                        </a-select>
                    </a-input-search>
                </div>
                <a-button
                    v-if="$store.state.btnAuth.btnAuth.bastion_network_proxy_create"
                    @click="$refs.AuthModal.handleAuth('create-network-proxy').then(() => $refs.AddNetworkProxy.show())"
                    icon="plus"
                    type="primary"
                    >新建</a-button
                >
            </div>
            <a-table
                :loading="tableLoading"
                :dataSource="tableData"
                :columns="columns"
                bordered
                @change="tableChange"
                :pagination="{
                    ...tableQuery,
                    showSizeChanger: true,
                    showTotal: (total) => `共 ${total} 条数据`,
                    showQuickJumper: true,
                }"
            >
                <template slot="name" slot-scope="text, record">
                    <a
                        @click="
                            $router.push({
                                path: '/setting/networkProxy/networkProxyDetails',
                                query: { id: record.id },
                            })
                        "
                        >{{ text }}</a
                    >
                </template>

                <template slot="system_type" slot-scope="text, record">
                    <div v-if="record.linux_ip && record.windows_ip" class="table_cell">
                        <p>Linux</p>
                        <p>Windows</p>
                    </div>
                    <div v-else-if="record.linux_ip" class="table_cell">
                        <p>Linux</p>
                    </div>
                    <div v-else-if="record.windows_ip" class="table_cell">
                        <p>Windows</p>
                    </div>
                </template>

                <template slot="ip" slot-scope="text, record">
                    <div v-if="record.linux_ip && record.windows_ip" class="table_cell">
                        <p>{{ record.linux_ip || '--' }}</p>
                        <p>{{ record.windows_ip || '--' }}</p>
                    </div>
                    <div v-else-if="record.linux_ip" class="table_cell">
                        <p>{{ record.linux_ip || '--' }}</p>
                    </div>
                    <div v-else-if="record.windows_port" class="table_cell">
                        <p>{{ record.windows_ip || '--' }}</p>
                    </div>
                </template>

                <template slot="port" slot-scope="text, record">
                    <div v-if="record.linux_port && record.windows_port" class="table_cell">
                        <p>{{ record.linux_port || '--' }}</p>
                        <p>{{ record.windows_port || '--' }}</p>
                    </div>
                    <div v-else-if="record.linux_port" class="table_cell">
                        <p>{{ record.linux_port || '--' }}</p>
                    </div>
                    <div v-else-if="record.windows_port" class="table_cell">
                        <p>{{ record.windows_port || '--' }}</p>
                    </div>
                </template>

                <template slot="description" slot-scope="text">
                    {{ text || '--' }}
                </template>

                <template slot="action" slot-scope="text, record">
                    <a
                        v-if="$store.state.btnAuth.btnAuth.bastion_network_proxy_update"
                        @click="
                            $refs.AuthModal.handleAuth('modify-network-proxy').then(() =>
                                $refs.AddNetworkProxy.show(record)
                            )
                        "
                        >编辑</a
                    >
                    <a
                        v-if="$store.state.btnAuth.btnAuth.bastion_network_proxy_delete"
                        @click="$refs.AuthModal.handleAuth('delete-network-proxy').then(() => deleteData(record))"
                        style="color: #333; margin: 0 0 0 10px"
                        >删除</a
                    >
                </template>
            </a-table>
        </a-card>
        <AddNetworkProxy @father="getNetworkProxyData" ref="AddNetworkProxy"></AddNetworkProxy>
        <AuthModal ref="AuthModal"></AuthModal>
    </div>
</template>

<script>
import AddNetworkProxy from './model/addNetworkProxy.vue'
import { getNetworkProxy, delNetworkProxy } from '@/api/networkProxy'
import { getPageAuth } from '@/utils/pageAuth'
export default {
    data() {
        return {
            tableLoading: false,
            tableData: [],
            columns: [
                {
                    title: '名称',
                    dataIndex: 'name',
                    scopedSlots: { customRender: 'name' },
                    width: 200,
                    ellipsis: true,
                },
                {
                    title: '系统类型',
                    dataIndex: 'system_type',
                    scopedSlots: { customRender: 'system_type' },
                    width: 200,
                },
                {
                    title: 'IP地址',
                    dataIndex: 'ip',
                    scopedSlots: { customRender: 'ip' },
                    width: 200,
                },
                {
                    title: '端口',
                    dataIndex: 'port',
                    scopedSlots: { customRender: 'port' },
                    width: 100,
                },
                {
                    title: '描述',
                    dataIndex: 'description',
                    scopedSlots: { customRender: 'description' },
                },
                {
                    title: '操作',
                    scopedSlots: { customRender: 'action' },
                    align: 'center',
                    width: '120px',
                },
            ],
            tableQuery: {
                search_data: undefined,
                search_type: 'name',
                current: 1,
                pageSize: 10,
                total: 0,
            },
            searchList: [
                { name: '名称', key: 'name' },
                { name: 'Linux IP地址', key: 'linux_ip' },
                { name: 'Windows IP地址', key: 'windows_ip' },
            ],
        }
    },
    async mounted() {
        const hasAuth = await getPageAuth(this, 'visit-network-proxy')
        if (hasAuth) {
            this.getNetworkProxyData()
        }
    },
    methods: {
        // 搜索
        searchTable() {
            this.tableQuery.current = 1
            this.getNetworkProxyData()
        },
        // 换页
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
            this.getNetworkProxyData()
        },
        // 获取网络代理数据
        getNetworkProxyData() {
            this.tableLoading = true
            getNetworkProxy(this.tableQuery)
                .then((res) => {
                    if (res.code == 200 && res.data && res.data.data) {
                        this.tableQuery.current = res.data.current
                        this.tableQuery.total = res.data.total
                        res.data.data.map((item) => {
                            item.key = item.id
                        })
                        this.tableData = res.data.data
                    }
                })
                .finally(() => {
                    this.tableLoading = false
                })
        },
        // 删除
        deleteData(record) {
            let _this = this
            this.$confirm({
                title: '确认删除该项数据吗?',
                onOk() {
                    return new Promise((resolve, reject) => {
                        delNetworkProxy({ id: record.id }).then((res) => {
                            if (res.code == 200) {
                                _this.$message.success(res.message)
                                resolve()
                                _this.getNetworkProxyData()
                            }
                        })
                    })
                },
            })
        },
    },
    components: {
        AddNetworkProxy,
    },
}
</script>

<style lang="less" scoped>
.top_search {
    display: flex;
    justify-content: space-between;
    padding-bottom: 12px;
}
.table_cell {
    margin: -10px;
    p {
        margin: 0;
        padding: 10px;
        height: 42px;
    }
    p:nth-of-type(2) {
        border-top: 1px solid #e8e8e8;
    }
}
</style>