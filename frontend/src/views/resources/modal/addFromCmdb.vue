<template>
    <div>
        <a-drawer :body-style="{ paddingBottom: '80px' }" width="1080px" title="资源平台导入" placement="right" :visible="visible" @close="onClose">
            <a-tabs v-model="tabKey" @change="tabsChange">
                <a-tab-pane key="SERVER" :tab="`物理机 (${number.SERVER})`"></a-tab-pane>
                <a-tab-pane key="VIRTUAL_SERVER" :tab="`虚拟机 (${number.VIRTUAL_SERVER})`" force-render></a-tab-pane>
                <a-tab-pane key="CLOUD_SERVER" :tab="`云主机 (${number.CLOUD_SERVER})`"></a-tab-pane>
            </a-tabs>
            <div style="margin:0 0 12px 0;">
                <a-input-search v-model="pagination.search_data" @search="searchTable" placeholder="请输入关键字搜索" style="width: 300px" allowClear>
                    <a-select slot="addonBefore" style="width: 100px" v-model="pagination.search_type">
                        <a-select-option v-for="item in searchList" :key="item.key">{{item.name}}</a-select-option>
                    </a-select>
                </a-input-search>
            </div>
            <a-table :loading="tableLoading" :columns="columns" :dataSource="tableData" :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }" :pagination="{showSizeChanger: true, showQuickJumper: true,showTotal: total => `共有 ${total} 条数据`}">
                <span slot="ip1" slot-scope="text">{{text || "--"}}</span>
                <span slot="ip2" slot-scope="text">{{text || "--"}}</span>
                <span slot="opt_os" slot-scope="text">{{text || "--"}}</span>
                <span slot="action" slot-scope="text,record">
                    <a-button @click="$refs.AddHostFromCmdb.show(record,selectGroupId)" size="small" type=link>配置</a-button>
                </span>
            </a-table>
            <a-button v-if="tableData.length>0" :disabled="selectedRowKeys.length==0" icon="plus" @click="$refs.BatchAddition.show(selectedRowKeys,selectGroupId)" style="float:left;margin:-50px 10px 0 0">批量配置</a-button>
            <AddHostFromCmdb @father="getAgentData()" :fatherData.sync="fatherData" ref="AddHostFromCmdb"></AddHostFromCmdb>
            <BatchAddition @father="getAgentData()" :fatherData.sync="fatherData" :fatherTableData.sync="tableData" ref="BatchAddition"></BatchAddition>
        </a-drawer>

    </div>
</template>

<script>
import { getAgent } from "@/api/agent.js"
import AddHostFromCmdb from "./addHostFromCmdb.vue"
import BatchAddition from "./batchAddition.vue"
export default {
    data() {
        return {
            visible: false,
            // 主机类型tag选项
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
            // 搜索可选项
            searchList: [
                { name: '主机名称', key: '_VISIBLE_NAME' },
                { name: '公网IP', key: '_PUBLIC_IP' },
                { name: '内网IP', key: '_INTERNAL_IP' },
            ],
            pagination: {
                total: 0, current: 1, pageSize: 10, showTotal: total => `共有 ${total} 条数据`,
                search_type: '_VISIBLE_NAME', search_data: undefined,
            },
            selectGroupId: undefined,
            // 各主机类型的数量
            number: {
                SERVER: 0,
                VIRTUAL_SERVER: 0,
                CLOUD_SERVER: 0,
            },
            // 选中的主机key值
            selectedRowKeys: [],
        }
    },
    // 分组数据
    props: ["fatherData"],
    methods: {
        show(selectGroupId) {
            this.visible = true
            this.selectGroupId = selectGroupId
            this.getAgentData()
        },
        onClose() {
            this.visible = false
            this.$emit("father")
            this.selectedRowKeys=[]
        },
        tabsChange(val) {
            this.tabKey = val
            this.pagination.search_type = "_VISIBLE_NAME"
            this.pagination.search_data = undefined
            this.getAgentData()
            this.selectedRowKeys = []
        },
        // 从cmdb获取主机数据
        getAgentData() {
            this.tableLoading = true
            let updata = {}
            if (this.pagination.search_data) {
                updata.search_data = this.pagination.search_data
                updata.search_type = this.tabKey + this.pagination.search_type
            }
            getAgent(updata).then(res => {
                if (res.code == 200 && res.data) {
                    this.number = {
                        SERVER: 0,
                        VIRTUAL_SERVER: 0,
                        CLOUD_SERVER: 0,
                    }
                    res.data.map(item => {
                        item.key = item.name
                        this.number[item.host_type]++
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
                this.selectedRowKeys = []
            })
        },
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getAgentData()
        },
        // table选择
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys;
        },
    },
    components: {
        AddHostFromCmdb,
        BatchAddition
    }
}
</script>

<style lang="less" scoped>
</style>