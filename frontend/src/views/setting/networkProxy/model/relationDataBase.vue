<template>
    <a-modal width="1000px" :okButtonProps="{props:{disabled:selectedRowKeys.length==0}}" :visible="visible" title="关联主机" :confirmLoading="btnLoading" @cancel="onCancel" @ok="onOk">
        <div class="content">
            <div class="content_left">
                <a-tree @select="treeSelect" :selectedKeys="selectedKeys" defaultExpandAll :show-line="true" :treeData="treeData">
                    <template slot="action" slot-scope="row">
                        <span :title="row.title" class="treetitle">{{ row.title }}</span>
                    </template>
                </a-tree>
            </div>
            <div class="content_right">
                <div class="top_search">
                    <div>
                        <a-input-search v-model="pagination.search_data" @search="searchTable" placeholder="请输入关键字搜索" style="width: 320px" allowClear>
                            <a-select slot="addonBefore" style="width: 120px" v-model="pagination.search_type">
                                <a-select-option v-for="item in searchList" :key="item.key">{{
                                item.name
                            }}</a-select-option>
                            </a-select>
                        </a-input-search>
                    </div>
                    <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                </div>
                <a-table @change="onChange" :scroll="{y:420}" :loading="tableLoading" :pagination="pagination" :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }" :columns="columns" :data-source="tableData">

                </a-table>
                <a-button @click="allCheck" style="position:relative;top:-50px;" v-if="tableData.length>0">批量全选</a-button>
            </div>
        </div>
    </a-modal>
</template>

<script>
import { getDataBase, getDataBaseGroup, } from "@/api/dataBase"
import { addNetworkProxyRelationHost } from "@/api/networkProxy"
export default {
    data() {
        return {
            visible: false,
            // 分组数据(左侧树)
            treeData: [
                {
                    key: "all",
                    title: "全部主机",
                    scopedSlots: { title: "action" },
                    children: [

                    ]
                }
            ],
            // 树选中的项
            selectedKeys: ["all"],
            pagination: {
                total: 0, current: 1, pageSize: 10,showTotal: total => `共有 ${total} 条数据`,
                showSizeChanger: true, showQuickJumper: true, search_type: 'host_name',
                search_data: undefined,
            },
            searchList: [
                { name: '数据库名称', key: 'host_name' },
                { name: '数据库地址', key: 'host_address' },
                { name: '数据库类型', key: 'database_type' },
            ],
            tableLoading: false,
            selectedRowKeys: [],
            columns: [
                {
                    title: '数据库名称',
                    dataIndex: 'host_name',
                    ellipsis: true,
                    scopedSlots: { customRender: 'name' },
                    width: 220,
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
            ],
            tableData: [],
            btnLoading: false,
        }
    },
    mounted() {

    },
    methods: {
        // 换页
        onChange(val) {
            this.pagination.total = val.total
            this.pagination.current = val.current
            this.pagination.pageSize = val.pageSize
            this.getDataBaseData()
        },
        // 刷新
        refresh() {
            this.pagination = this.$options.data().pagination
            this.getDataBaseData()
        },
        // 全选
        allCheck() {
            this.selectedRowKeys = this.selectedRowKeys.length == this.tableData.length ? [] : this.tableData.map((item) => item.id)
        },
        // table选择
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys;
        },
        show() {
            this.visible = true
            this.getDataBaseGroupData()
            this.getDataBaseData()
        },
        onCancel() {
            this.visible = false
            this.selectedRowKeys = []
            this.selectedKeys = ["all"]
            this.selectGroupId = "all"
            this.tableData = []
        },
        onOk() {
            this.btnLoading = true
            addNetworkProxyRelationHost({ network_proxy_id: this.$route.query.id, resource_list: this.selectedRowKeys }).then(res => {
                if (res.code == 200) {
                    this.$message.success(res.message)
                    this.$emit("father")
                    this.onCancel()
                }
            }).finally(() => {
                this.btnLoading = false
            })
        },
        // 选中分组(树)
        treeSelect(val) {
            this.selectGroupId = val[0]
            this.selectedKeys = val
            this.pagination.current = 1
            this.getDataBaseData()
        },
        // 获取分组数据(树)
        getDataBaseGroupData() {
            this.showTree = false
            getDataBaseGroup().then(res => {
                if (res.code == 200 && res.data) {
                    organizeTree(res.data, 2)
                    this.treeData[0].children = res.data
                    this.fatherData = res.data
                    this.showTree = true
                }

                function organizeTree(treedata, layer) {
                    treedata.map(item => {
                        item.key = item.id
                        item.title = item.name
                        item.scopedSlots = { title: "action" }
                        item.layer = layer

                        item.value = item.id

                        if (item.children && item.children.length > 0) {
                            organizeTree(item.children, layer + 1)
                        }
                    })
                }
            })
        },
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getDataBaseData()
        },
        // 获取主机数据
        getDataBaseData() {
            this.tableLoading = true
            let updata = {
                network_proxy: this.$route.query.id,
                all_data: 1,
            }
            if (this.pagination.search_data) {
                updata.search_type = this.pagination.search_type
                updata.search_data = this.pagination.search_data
            }
            if (this.selectGroupId != "all") {
                updata.group_id = this.selectGroupId
            }
            getDataBase(updata).then(res => {
                if (res.code == 200 && res.data) {
                    res.data.map(item => {
                        item.key = item.id
                    })
                    this.tableData = res.data
                }
            }).finally(() => {
                this.tableLoading = false
            })
        },
    }
}
</script>

<style lang="less" scoped>
.content {
    display: flex;
    background: #fff;
    .content_left {
        flex: 0px 300 300;
        border-right: 1px solid #f5f5f5;
        // padding: 0 20px 0 0;
        min-width: 200px;
        .treetitle {
            width: 100%;
            display: inline-block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        /deep/.ant-tree-node-content-wrapper {
            max-width: calc(100% - 50px);
        }
    }
    .content_right {
        flex: 0px 1325 1325;
        padding: 0 0 0px 20px;
        .top_search {
            display: flex;
            justify-content: space-between;
            height: 52px;
        }
    }
}
</style>