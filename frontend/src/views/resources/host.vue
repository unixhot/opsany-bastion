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
                            <a-dropdown v-if="row.key != 1" class="dropdown" :trigger="['click']" @click.native.stop>
                                <a-menu slot="overlay">
                                    <a-menu-item
                                        @click="$refs.AddGroup.show(row, 'edit')"
                                        key="1"
                                        v-if="
                                            row.key != 'all' && $store.state.btnAuth.btnAuth.bastion_host_group_update
                                        "
                                    >
                                        <a-icon type="edit" />编辑
                                    </a-menu-item>
                                    <a-menu-item
                                        @click="$refs.AddGroup.show(row, 'add')"
                                        key="2"
                                        v-if="
                                            (row.layer < 5 || row.key == 'all') &&
                                            $store.state.btnAuth.btnAuth.bastion_host_group_create
                                        "
                                    >
                                        <a-icon type="folder" />添加子文件夹
                                    </a-menu-item>
                                    <a-menu-item
                                        @click="deleteGroup(row)"
                                        key="3"
                                        v-if="
                                            row.key != 'all' && $store.state.btnAuth.btnAuth.bastion_host_group_delete
                                        "
                                    >
                                        <a-icon type="delete" />删除
                                    </a-menu-item>
                                </a-menu>
                                <a-button type="link" icon="more"> </a-button>
                            </a-dropdown>
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
                            <!-- <a-dropdown style="margin: 0 10px 0 0">
                                <a-menu slot="overlay">
                                    <a-menu-item @click="$refs.AddFromCmdb.show(selectGroupId)" key="1">
                                        资源平台导入
                                    </a-menu-item>
                                </a-menu>
                                <a-button
                                    v-if="$store.state.btnAuth.btnAuth.bastion_host_import"
                                    style="margin-left: 8px"
                                >
                                    导入主机 <a-icon type="down" />
                                </a-button>
                            </a-dropdown> -->
                            <!-- @click="$refs.AddHost.show(selectGroupId)" -->

                            <a-button
                                v-if="$store.state.btnAuth.btnAuth.bastion_host_create"
                                @click="
                                    $refs.AuthModal.handleAuth('create-host-resources').then(() =>
                                        $refs.AddHost.show(selectGroupId)
                                    )
                                "
                                type="primary"
                                icon="plus"
                                >新建</a-button
                            >
                        </div>
                    </div>

                    <a-table
                        :loading="tableLoading"
                        @change="onChange"
                        :pagination="pagination"
                        :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }"
                        :columns="columns"
                        :data-source="tableData"
                    >
                        <template slot="name" slot-scope="text, record">
                            <a
                                v-if="$store.state.btnAuth.btnAuth.bastion_host_details"
                                :title="text"
                                @click="
                                    $refs.AuthModal.handleAuth('get-host-resources').then(() =>
                                        $router.push({ path: '/resources/host/hostDetails', query: { id: record.id } })
                                    )
                                "
                                >{{ text }}</a
                            >
                            <span v-else>{{ text }}</span>
                        </template>
                        <template slot="voucherTitle">
                            <span>关联资源凭证</span>
                            <a-tooltip placement="top" title="密码凭证/SSH密钥/凭证分组" arrow-point-at-center>
                                <a-icon style="margin: 0 0 0 3px; color: #666" type="exclamation-circle" />
                            </a-tooltip>
                        </template>
                        <template slot="voucher" slot-scope="text, record">
                            <a
                                v-if="$store.state.btnAuth.btnAuth.bastion_host_details"
                                @click="
                                    $refs.AuthModal.handleAuth('get-host-resources').then(() =>
                                        $router.push({ path: '/resources/host/hostDetails', query: { id: record.id } })
                                    )
                                "
                                >{{ text }}</a
                            >
                            <span v-else>{{ text }}</span>
                        </template>
                        <template slot="action" slot-scope="text, record">
                            <a-button
                                size="small"
                                type="link"
                                v-if="$store.state.btnAuth.btnAuth.bastion_host_details"
                                @click="
                                    $refs.AuthModal.handleAuth('get-host-resources').then(() =>
                                        $router.push({ path: '/resources/host/hostDetails', query: { id: record.id } })
                                    )
                                "
                                >查看</a-button
                            >
                            <a-button
                                size="small"
                                type="link"
                                v-if="$store.state.btnAuth.btnAuth.bastion_host_login"
                                @click="
                                    $refs.AuthModal.handleAuth('login-host-resources').then(() =>
                                        $refs.LoginHostModal.showModal(record)
                                    )
                                "
                                >登录</a-button
                            >
                            <a-button
                                size="small"
                                type="link"
                                v-if="$store.state.btnAuth.btnAuth.bastion_host_update"
                                @click="
                                    $refs.AuthModal.handleAuth('modify-host-resources').then(() =>
                                        $refs.AddHost.show(selectGroupId, record)
                                    )
                                "
                                >编辑</a-button
                            >
                            <a-button
                                size="small"
                                type="link"
                                v-if="$store.state.btnAuth.btnAuth.bastion_host_delete"
                                @click="
                                    $refs.AuthModal.handleAuth('delete-host-resources').then(() => deleteHost(record))
                                "
                                style="color: #333"
                                >删除</a-button
                            >
                        </template>
                    </a-table>
                    <a-button
                        v-if="tableData.length > 0"
                        :disabled="selectedRowKeys.length == 0"
                        icon="delete"
                        @click="$refs.AuthModal.handleAuth('delete-host-resources').then(() => batchDelete())"
                        style="float: left; margin: -50px 10px 0 0"
                        >批量删除</a-button
                    >
                </div>
            </div>
        </a-card>
        <AddGroup @father="getHostGroupData" ref="AddGroup"></AddGroup>
        <AddHost @father="getHostData(), getHostGroupData()" :fatherData.sync="fatherData" ref="AddHost"></AddHost>
        <LoginHostModal ref="LoginHostModal"></LoginHostModal>
        <AddFromCmdb
            @father="getHostData(), getHostGroupData()"
            :fatherData.sync="fatherData"
            ref="AddFromCmdb"
        ></AddFromCmdb>
        <AuthModal ref="AuthModal"></AuthModal>
    </div>
</template>

<script>
import ContentHeader from '@/views/components/ContentHeader'
import AddHost from './modal/addHost.vue'
import LoginHostModal from './modal/LoginHostModal.vue'
import { getHost, delHost, getHostGroup, delHostGroup } from '@/api/host'
import AddGroup from './modal/addGroup.vue'
import AddFromCmdb from './modal/addFromCmdb.vue'
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
            selectedRowKeys: [],
            tableData: [],
            columns: [
                {
                    title: '主机名称',
                    dataIndex: 'host_name',
                    ellipsis: true,
                    scopedSlots: { customRender: 'name' },
                    width: 200,
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
                    dataIndex: 'voucher',
                    ellipsis: true,
                    slots: { title: 'voucherTitle' },
                    scopedSlots: { customRender: 'voucher' },
                    width: 150,
                },
                {
                    title: '创建时间',
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
        // const hasAuth = await getPageAuth(this, 'visit-host-resources')
        // if (hasAuth) {
        this.getHostData()
        this.getHostGroupData()
        // }
    },
    methods: {
        // 删除
        deleteHost(record) {
            let _this = this
            this.$confirm({
                title: '确认删除该主机吗？',
                onOk: function () {
                    delHost({ id: record.id }).then((res) => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getHostData()
                        }
                    })
                },
            })
        },
        // 批量删除
        batchDelete() {
            let _this = this
            this.$confirm({
                title: '确认删除吗？',
                onOk: function () {
                    delHost({ id_list: _this.selectedRowKeys }).then((res) => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getHostData()
                            _this.selectedRowKeys = []
                        }
                    })
                },
            })
        },
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
        // table选择
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys
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
            getHost(updata)
                .then((res) => {
                    if (res.code == 200 && res.data) {
                        this.pagination.total = res.data.total
                        this.pagination.current = res.data.current
                        this.pagination.pageSize = res.data.pageSize
                        res.data.data.map((item) => {
                            item.key = item.id
                            item.voucher =
                                (item.credential.password_credential
                                    ? item.credential.password_credential.length
                                    : '0') +
                                '/' +
                                (item.credential.ssh_credential ? item.credential.ssh_credential.length : '0') +
                                '/' +
                                (item.credential.credential_group ? item.credential.credential_group.length : '0')
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
            getHostGroup()
                .then((res) => {
                    if (res.code == 200 && res.data) {
                        organizeTree(res.data, 2)
                        this.treeData[0].children = res.data
                        this.fatherData = res.data
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
        // 删除分组
        deleteGroup(row) {
            let _this = this
            this.$confirm({
                title: '确认删除该分组吗?',
                onOk: function () {
                    delHostGroup({ id: row.id }).then((res) => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            if (row.id == _this.selectGroupId) {
                                _this.selectedKeys = ['all']
                                _this.selectGroupId = 'all'
                            }
                            _this.getHostGroupData()
                            _this.getHostData()
                        } else {
                            _this.$message.error(res.message)
                        }
                    })
                },
            })
        },
    },
    components: {
        ContentHeader,
        AddHost,
        AddGroup,
        LoginHostModal,
        AddFromCmdb,
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