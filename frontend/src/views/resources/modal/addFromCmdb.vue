<template>
    <div>
        <a-drawer :body-style="{ paddingBottom: '80px' }" width="1080px" title="资源平台导入" placement="right" :visible="visible" @close="onClose">
            <a-tabs v-model="tabKey" @change="tabsChange">
                <a-tab-pane key="SERVER" tab="物理机"></a-tab-pane>
                <a-tab-pane key="VIRTUAL_SERVER" tab="虚拟机" force-render></a-tab-pane>
                <a-tab-pane key="CLOUD_SERVER" tab="云主机"></a-tab-pane>
            </a-tabs>
            <div style="margin:0 0 20px 0;">
                <a-input-search v-model="pagination.search_data" @search="searchTable" placeholder="请输入关键字搜索" style="width: 300px" allowClear>
                    <a-select slot="addonBefore" style="width: 100px" v-model="pagination.search_type">
                        <a-select-option v-for="item in searchList" :key="item.key">{{item.name}}</a-select-option>
                    </a-select>
                </a-input-search>
            </div>
            <a-table :loading="tableLoading" :columns="columns" :dataSource="tableData" :pagination="{showSizeChanger: true, showQuickJumper: true,showTotal: total => `共有 ${total} 条数据`}">
                <span slot="ip1" slot-scope="text">{{text || "--"}}</span>
                <span slot="ip2" slot-scope="text">{{text || "--"}}</span>
                <span slot="opt_os" slot-scope="text">{{text || "--"}}</span>
                <span slot="action" slot-scope="text,record">
                    <a-button @click="$refs.AddHostFromCmdb.show(record)" size="small" type=link>配置</a-button>
                </span>
            </a-table>
            <AddHostFromCmdb @father="getAgentData()" :fatherData.sync="fatherData" ref="AddHostFromCmdb"></AddHostFromCmdb>
        </a-drawer>

    </div>
</template>

<script>
import { getAgent } from "@/api/agent.js"
import AddHostFromCmdb from "./addHostFromCmdb.vue"
export default {
    data() {
        return {
            visible: false,
            tabKey: "SERVER",
            columns: [
                { title: '名称', dataIndex: 'show_name' },
                { title: '公网IP地址', dataIndex: 'ip1', scopedSlots: { customRender: 'ip1' }, },
                { title: '内网IP地址', dataIndex: 'ip2', scopedSlots: { customRender: 'ip2' }, },
                { title: '操作系统', dataIndex: 'opt_os', scopedSlots: { customRender: 'opt_os' } },
                {
                    title: '操作',
                    width: 120,
                    scopedSlots: { customRender: 'action' },
                    align: 'center',
                },
            ],
            tableData: [],
            tableLoading: false,
            searchList: [
                { name: '主机名称', key: '_VISIBLE_NAME' },
                { name: '公网IP', key: '_PUBLIC_IP' },
                { name: '内网IP', key: '_INTERNAL_IP' },
            ],
            pagination: {
                total: 0, current: 1, pageSize: 10, showTotal: total => `共有 ${total} 条数据`,
                search_type: '_VISIBLE_NAME', search_data: undefined,
            },
        }
    },
    props: ["fatherData"],
    methods: {
        show() {
            this.visible = true
            this.getAgentData()
        },
        onClose() {
            this.visible = false
            this.$emit("father")
        },
        tabsChange(val) {
            this.tabKey = val
            this.pagination.search_type="_VISIBLE_NAME"
            this.pagination.search_data=undefined
            this.getAgentData()
        },
        // 从cmdb获取主机数据
        getAgentData() {
            this.tableLoading = true
            let updata = {}
            if (this.pagination.search_data) {
                updata.search_data = this.pagination.search_data
                updata.search_type =  this.tabKey + this.pagination.search_type
            }
            getAgent(updata).then(res => {
                if (res.code == 200 && res.data) {
                    res.data.map(item => {
                        item.key = item.name
                    })
                    this.allTableData = res.data
                    this.tableData = this.allTableData.filter(item => {
                        return item.host_type == this.tabKey
                    })
                } else {
                    this.tableData = []
                }
            }).finally(() => {
                this.tableLoading = false
            })
        },
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getAgentData()
        },
    },
    components: {
        AddHostFromCmdb
    }
}
</script>

<style lang="less" scoped>
</style>