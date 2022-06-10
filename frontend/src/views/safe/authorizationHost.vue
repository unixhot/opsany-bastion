<template>
    <div>
        <ContentHeader>
            <div slot="docs">
                支持自定义主机分组，创建主机时可以直接创建和关联登录凭证，一个主机可以关联多个登录凭证。
            </div>
        </ContentHeader>
        <a-card>
            <div class="content">
                <div class="content_left">
                    <a-tree
                        @select="treeSelect"
                        :selectedKeys="selectedKeys"
                        v-if="showTree"
                        defaultExpandAll
                        :show-line="true"
                        :treeData="treeData"
                    >
                        <template slot="action" slot-scope="row">
                            <span :title="row.title" class="treetitle">{{ row.title }} ({{ row.count || 0 }})</span>
                        </template>
                    </a-tree>
                    <a-spin v-else />
                </div>
                <div class="content_right">
                    <div class="top_search">
                        <div>
                            <a-input-search
                                v-model="pagination.search_data"
                                @search="searchTable"
                                placeholder="请输入关键字搜索"
                                style="width: 300px"
                                allowClear
                            >
                                <a-select slot="addonBefore" style="width: 100px" v-model="pagination.search_type">
                                    <a-select-option v-for="item in searchList" :key="item.key">{{
                                        item.name
                                    }}</a-select-option>
                                </a-select>
                            </a-input-search>
                        </div>
                        <div>
                            <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                        </div>
                    </div>

                    <a-table
                        :loading="tableLoading"
                        @change="onChange"
                        :pagination="pagination"
                        :columns="columns"
                        :data-source="tableData"
                    >
                        <template
                            v-if="$store.state.btnAuth.btnAuth.bastion_ops_host_login"
                            slot="action"
                            slot-scope="text, record"
                        >
                            <a-button
                                v-if="record.time_frame"
                                size="small"
                                type="link"
                                @click="
                                    $refs.AuthModal.handleAuth('login-authorization-host').then(() => handleLogin(record))
                                "
                                >登录</a-button
                            >
                            <a-tooltip
                                v-else
                                placement="left"
                                title="由于访问策略限制，当前时段不允许登录。"
                                :overlayStyle="{ maxWidth: '300px' }"
                                arrow-point-at-center
                            >
                                <a-button
                                    disabled
                                    size="small"
                                    type="link"
                                    @click="
                                        $refs.AuthModal.handleAuth('login-authorization-host').then(() => handleLogin(record))
                                    "
                                    >登录</a-button
                                >
                            </a-tooltip>
                        </template>
                    </a-table>
                </div>
            </div>
        </a-card>

        <LoginHostModal ref="LoginHostModal"></LoginHostModal>
        <AuthModal ref="AuthModal"></AuthModal>

    </div>
</template>

<script>
import ContentHeader from '@/views/components/ContentHeader'

import LoginHostModal from '../resources/modal/LoginHostModal.vue'
import { getUserHost, getHostGroup } from '@/api/host'
import { getPageAuth } from '@/utils/pageAuth'
export default {
    data() {
        return {
            // 分组数据(左侧树)
            treeData: [
                {
                    key: 'all',
                    title: '全部主机',
                    scopedSlots: { title: 'action' },
                    children: [],
                },
            ],
            searchList: [
                { name: '主机名称', key: 'host_name' },
                { name: '主机地址', key: 'host_address' },
                { name: '系统类型', key: 'system_type' },
            ],
            tableData: [],
            columns: [
                {
                    title: '主机名称',
                    dataIndex: 'host_name',
                    ellipsis: true,
                    scopedSlots: { customRender: 'name' },
                    width: 220,
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
                    title: '授权时间',
                    dataIndex: 'create_time',
                    ellipsis: true,
                },
                {
                    title: '操作',
                    width: 200,
                    scopedSlots: { customRender: 'action' },
                    align: 'center',
                },
            ],
            showTree: false,
            // 分组数据(传给子组件)
            fatherData: [],
            tableLoading: false,
            pagination: {
                total: 0,
                current: 1,
                pageSize: 10,
                showTotal: (total) => `共有 ${total} 条数据`,
                showSizeChanger: true,
                showQuickJumper: true,
                search_type: 'host_name',
                search_data: undefined,
            },
            // 选中的分组id
            selectGroupId: undefined,
            // 树选中的项
            selectedKeys: ['all'],
        }
    },
    async mounted() {
        const hasAuth = await getPageAuth(this, 'visit-authorization-host')
        if (hasAuth) {
            this.getHostData()
            this.getHostGroupData()
        }
    },
    methods: {
        // 选中分组(树)
        treeSelect(val) {
            this.selectGroupId = val[0]
            this.selectedKeys = val
            this.pagination.current = 1
            this.getHostData()
        },
        // 换页
        onChange(val) {
            this.pagination.total = val.total
            this.pagination.current = val.current
            this.pagination.pageSize = val.pageSize
            this.getHostData()
        },
        // 获取主机数据
        getHostData() {
            this.tableLoading = true
            let updata = {
                current: this.pagination.current,
                pageSize: this.pagination.pageSize,
            }
            if (this.pagination.search_data) {
                updata.search_type = this.pagination.search_type
                updata.search_data = this.pagination.search_data
            }
            if (this.selectGroupId != 'all') {
                updata.group_id = this.selectGroupId
            }
            getUserHost(updata)
                .then((res) => {
                    if (res.code == 200 && res.data) {
                        this.pagination.total = res.data.total
                        this.pagination.current = res.data.current
                        this.pagination.pageSize = res.data.pageSize
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
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getHostData()
        },
        // 刷新
        refresh() {
            this.pagination = this.$options.data().pagination
            this.getHostData()
        },
        // 获取分组数据(树)
        getHostGroupData() {
            this.showTree = false
            let allNumber = 0
            getHostGroup()
                .then((res) => {
                    if (res.code == 200 && res.data) {
                        organizeTree(res.data, 2)
                        this.treeData[0].children = res.data
                        this.treeData[0].children.map((item) => {
                            allNumber += item.count
                        })
                        this.treeData[0].count = allNumber
                        this.fatherData = res.data
                        this.showTree = true
                    }

                    function organizeTree(treedata, layer) {
                        treedata.map((item) => {
                            item.key = item.id
                            item.title = item.name
                            item.scopedSlots = { title: 'action' }
                            item.layer = layer

                            item.value = item.id

                            if (item.children && item.children.length > 0) {
                                organizeTree(item.children, layer + 1)
                            }
                        })
                    }
                })
                .finally(() => {
                    this.showTree = true
                })
        },
        //登录弹窗
        handleLogin(row) {
            this.$refs.LoginHostModal.showModal(row)
        },
    },
    components: {
        ContentHeader,
        LoginHostModal,
    },
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
            width: 90px;
            display: inline-block;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
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
.dropdown {
    position: absolute;
    right: 0;
    top: 0;
}
/deep/.ant-tree-treenode-switcher-close,
/deep/.ant-tree-treenode-switcher-open {
    position: relative;
}
/deep/.ant-spin-spinning {
    width: 100%;
    height: 100%;
}
/deep/.ant-spin-dot-spin {
    top: 50%;
}
</style>