<template>
    <div>
        <content-header>
            <a-button @click="$router.go(-1)" icon="arrow-left" type="primary" slot="right">返回</a-button>
        </content-header>
        <a-card>
            <a-card>
                <h3 style="margin:0;" slot="title">
                    名称：{{infomation.name}}
                </h3>
                <div class="infomation">
                    <div v-if="infomation.linux_ip" class="infomation_row">
                        <p>
                            <span class="cell_title">系统类型：</span>
                            <span class="cell_content">Linux</span>
                        </p>
                        <p>
                            <span class="cell_title">主机地址：</span>
                            <span class="cell_content">{{infomation.linux_ip}}</span>
                        </p>
                        <p>
                            <span class="cell_title">端口：</span>
                            <span class="cell_content">{{infomation.linux_port}}</span>
                        </p>
                    </div>
                    <div v-if="infomation.windows_ip" class="infomation_row">
                        <p>
                            <span class="cell_title">系统类型：</span>
                            <span class="cell_content">Windows</span>
                        </p>
                        <p>
                            <span class="cell_title">主机地址：</span>
                            <span class="cell_content">{{infomation.windows_ip}}</span>
                        </p>
                        <p>
                            <span class="cell_title">端口：</span>
                            <span class="cell_content">{{infomation.windows_port}}</span>
                        </p>
                    </div>
                    <div class="infomation_row">
                        <p>
                            <span class="cell_title">描述：</span>
                            <span class="cell_content">{{infomation.description || "--"}}</span>
                        </p>
                    </div>
                </div>
            </a-card>

            <a-card :bodyStyle="{padding:'20px 0 20px 0'}" style="margin:30px 0 0 0" title="配置资源">
                <div class="relation">
                    <a-menu :selectedKeys="selectedKeys" @select="TypeChange" class="left" mode="inline" style="margin:20px 0 0 0">
                        <a-menu-item key="host">关联主机</a-menu-item>
                        <a-menu-item key="database">关联数据库</a-menu-item>
                    </a-menu>

                    <div class="right">
                        <div class="top_search">
                            <div>
                                <a-input-search @search="searchTable" v-model="pagination.search_data" placeholder="请输入关键字搜索" style="width: 320px" allowClear>
                                    <a-select slot="addonBefore" style="width: 120px" v-model="pagination.search_type">
                                        <a-select-option v-for="item in searchList" :key="item.key">{{item.name}}</a-select-option>
                                    </a-select>
                                </a-input-search>
                            </div>
                            <div>
                                <a-button @click="$refs.RelationHost.show()" v-if="$store.state.btnAuth.btnAuth.bastion_network_proxy_host_create&&selectedKeys[0]&&selectedKeys[0] =='host'" type="primary">关联主机</a-button>
                                <a-button @click="$refs.RelationDataBase.show()" v-else-if="$store.state.btnAuth.btnAuth.bastion_network_proxy_database_create&&selectedKeys[0]&&selectedKeys[0] =='database'" type="primary">关联数据库</a-button>
                            </div>
                        </div>
                        <a-table :loading="tableLoading" :pagination="pagination" @change="onChange" :columns="columns" :data-source="tableData">
                            <template slot="login_type" slot-scope="text">
                                {{text=="auto"?"自动登录":"手动登录"}}
                            </template>
                            <template slot="description" slot-scope="text">
                                {{text||"--"}}
                            </template>
                            <template slot="action" slot-scope="text,record">
                                <a v-if="$store.state.btnAuth.btnAuth.bastion_network_proxy_host_delete&&selectedKeys[0]&&selectedKeys[0] =='host'||$store.state.btnAuth.btnAuth.bastion_network_proxy_database_delete&&selectedKeys[0]&&selectedKeys[0] =='database'" @click="remove(record)">移除</a>
                            </template>
                        </a-table>
                    </div>
                </div>
            </a-card>
        </a-card>

        <RelationHost @father="getNetworkProxyRelationHostData" ref="RelationHost"></RelationHost>
        <RelationDataBase @father="getNetworkProxyRelationHostData" ref="RelationDataBase"></RelationDataBase>
    </div>
</template>

<script>
import { getNetworkProxy, getNetworkProxyRelationHost, delNetworkProxyRelationHost } from "@/api/networkProxy"
import RelationHost from "./model/relationHost.vue"
import RelationDataBase from "./model/relationDataBase.vue"
export default {
    data() {
        return {
            // 详情
            infomation: {},
            // 选中的关联类型
            selectedKeys: ["host"],
            pagination: {
                current: 1, pageSize: 10, total: 0,
                showSizeChanger: true, showQuickJumper: true, search_type: "host_name", search_data: "",
                showTotal: total => `共有 ${total} 条数据`,
            },
            columns: [],
            tableData: [],
            columns1: [
                {
                    title: '主机名称',
                    dataIndex: 'host_name',
                    ellipsis: true,
                },
                {
                    title: '主机地址',
                    dataIndex: 'host_address',
                    ellipsis: true,
                },
                {
                    title: '系统类型',
                    dataIndex: 'system_type',
                    ellipsis: true,
                },
                {
                    title: '操作',
                    width: 200,
                    scopedSlots: { customRender: 'action' },
                    align: 'center'
                },
            ],
            columns2: [
                {
                    title: '数据库名称',
                    dataIndex: 'host_name',
                    ellipsis: true,
                },
                {
                    title: '数据库地址',
                    dataIndex: 'host_address',
                    ellipsis: true,
                },
                {
                    title: '数据库类型',
                    dataIndex: 'database_type',
                    ellipsis: true,
                },
                {
                    title: '操作',
                    width: 200,
                    scopedSlots: { customRender: 'action' },
                    align: 'center'
                },
            ],
            searchList: [],
            searchList1: [
                { name: '主机名称', key: 'host_name' },
                { name: '主机地址', key: 'host_address' },
                { name: '系统类型', key: 'system_type' },
            ],
            searchList2: [
                { name: '数据库名称', key: 'host_name' },
                { name: '数据库地址', key: 'host_address' },
                { name: '数据库类型', key: 'database_type' },
            ],
            tableLoading: false,
        }
    },
    mounted() {
        this.getNetworkProxyInfo()
        this.getNetworkProxyRelationHostData()
        this.columns = this.columns1
        this.searchList = this.searchList1
    },
    methods: {
        //移除与当前网络代理关联的主机或数据库
        remove(record) {
            let _this = this
            this.$confirm({
                title: "确认移除该条数据吗?",
                onOk() {
                    return new Promise((resolve, reject) => {
                        delNetworkProxyRelationHost({ network_proxy_id: _this.$route.query.id, resource_id: record.id }).then(res => {
                            if (res.code == 200) {
                                _this.$message.success(res.message)
                                resolve()
                                _this.getNetworkProxyRelationHostData()
                            }
                        })
                    })
                }
            })
        },
        // 获取详情信息
        getNetworkProxyInfo() {
            getNetworkProxy({ id: this.$route.query.id }).then(res => {
                this.infomation = res.data
            })
        },
        // 搜索
        searchTable(val) {
            this.pagination.current = 1
            this.getNetworkProxyRelationHostData()
        },
        // 类型切换
        TypeChange(event) {
            this.selectedKeys = [event.key]
            if (event.key == "host") {
                this.columns = this.columns1
                this.searchList = this.searchList1
                this.pagination.search_type = "host_name"
                this.pagination.search_data = ""
                this.pagination.current = 1
                this.getNetworkProxyRelationHostData()
            } else if (event.key == "database") {
                this.columns = this.columns2
                this.searchList = this.searchList2
                this.pagination.search_type = "host_name"
                this.pagination.search_data = ""
                this.pagination.current = 1
                this.getNetworkProxyRelationHostData()
            }
        },
        //获取与当前网络代理关联的主机或数据库
        getNetworkProxyRelationHostData() {
            let updata = {
                network_proxy_id: this.$route.query.id,
                resource_type: this.selectedKeys[0],
                pageSize: this.pagination.pageSize,
                current: this.pagination.current,
            }
            if (this.pagination.search_data) {
                updata.search_type = this.pagination.search_type
                updata.search_data = this.pagination.search_data
            }
            this.tableLoading = true
            getNetworkProxyRelationHost(updata).then(res => {
                if (res.code == 200 && res.data && res.data.data) {
                    this.pagination.current = res.data.current
                    this.pagination.pageSize = res.data.pageSize
                    this.pagination.total = res.data.total
                    res.data.data.map(item => {
                        item.key = item.id
                    })
                    this.tableData = res.data.data
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
            this.getNetworkProxyRelationHostData()
        },
    },
    components: {
        RelationHost,
        RelationDataBase,
    }
}
</script>

<style lang="less" scoped>
.infomation {
    .infomation_row {
        display: flex;
        p {
            flex: 0px 1 1;
            display: flex;
            margin: 0 0 20px 0;
            .cell_title {
                flex: 80px 0 0;
                text-align: right;
            }
            .cell_content {
                flex: 0px 1 1;
            }
        }
    }
}
.relation {
    border-top: none;
    margin: -16px 0 0 0;
    padding: 5px 0 0 0;
    display: flex;
    .left {
        flex: 120px 0 0;
    }
    .right {
        flex: 0px 1 1;
        padding: 20px;
        .top_search {
            display: flex;
            justify-content: space-between;
            margin: 0 0 12px 0;
        }
    }
}
/deep/.ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
    background: none;
}
.ant-menu-item {
    background: none;
    margin: 0;
}
</style>