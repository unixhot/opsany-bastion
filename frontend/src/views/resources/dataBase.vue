<template>
    <div>
        <ContentHeader>
            <div slot="docs">数据库资源用于通过堡垒机直接登录数据库，目前支持MySQL、MongoDB、Redis。</div>
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
                            <a-dropdown
                                v-if="row.title != '默认分组'"
                                class="dropdown"
                                :trigger="['click']"
                                @click.native.stop
                            >
                                <a-menu slot="overlay">
                                    <a-menu-item
                                        v-if="
                                            $store.state.btnAuth.btnAuth.bastion_database_group_update &&
                                            row.key != 'all'
                                        "
                                        @click="$refs.AddDataBaseGroup.show(row, 'edit')"
                                        key="1"
                                    >
                                        <a-icon type="edit" />编辑
                                    </a-menu-item>
                                    <a-menu-item
                                        v-if="
                                            $store.state.btnAuth.btnAuth.bastion_database_group_create &&
                                            (row.layer < 5 || row.key == 'all')
                                        "
                                        @click="$refs.AddDataBaseGroup.show(row, 'add')"
                                        key="2"
                                    >
                                        <a-icon type="folder" />添加子文件夹
                                    </a-menu-item>
                                    <a-menu-item
                                        v-if="
                                            $store.state.btnAuth.btnAuth.bastion_database_group_delete &&
                                            row.key != 'all'
                                        "
                                        @click="deleteGroup(row)"
                                        key="3"
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
                                style="width: 320px"
                                allowClear
                            >
                                <a-select slot="addonBefore" style="width: 120px" v-model="pagination.search_type">
                                    <a-select-option v-for="item in searchList" :key="item.key">{{
                                        item.name
                                    }}</a-select-option>
                                </a-select>
                            </a-input-search>
                        </div>
                        <div>
                            <a-button @click="refresh" style="margin-right: 10px" icon="reload">刷新</a-button>
                            <a-button
                                v-if="$store.state.btnAuth.btnAuth.bastion_database_create"
                                @click="$refs.AddDataBase.show(selectGroupId)"
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
                                v-if="$store.state.btnAuth.btnAuth.bastion_database_details"
                                :title="text"
                                @click="
                                    $router.push({
                                        path: '/resources/dataBase/dataBaseDetails',
                                        query: { id: record.id },
                                    })
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
                                v-if="$store.state.btnAuth.btnAuth.bastion_database_details"
                                @click="
                                    $router.push({
                                        path: '/resources/dataBase/dataBaseDetails',
                                        query: { id: record.id },
                                    })
                                "
                                >{{ text }}</a
                            >
                            <span v-else>{{ text }}</span>
                        </template>
                        <template slot="action" slot-scope="text, record">
                            <a-button
                                v-if="$store.state.btnAuth.btnAuth.bastion_database_details"
                                size="small"
                                type="link"
                                @click="
                                    $router.push({
                                        path: '/resources/dataBase/dataBaseDetails',
                                        query: { id: record.id },
                                    })
                                "
                                >查看</a-button
                            >
                            <a-button
                                v-if="$store.state.btnAuth.btnAuth.bastion_database_login"
                                size="small"
                                type="link"
                                @click="handleLogin(record)"
                                >登录</a-button
                            >
                            <a-button
                                v-if="$store.state.btnAuth.btnAuth.bastion_database_update"
                                size="small"
                                type="link"
                                @click="$refs.AddDataBase.show(selectGroupId, record)"
                                >编辑</a-button
                            >
                            <a-button
                                v-if="$store.state.btnAuth.btnAuth.bastion_database_delete"
                                size="small"
                                type="link"
                                @click="deleteDataBase(record)"
                                style="color: #333"
                                >删除</a-button
                            >
                        </template>
                    </a-table>
                    <a-button
                        v-if="$store.state.btnAuth.btnAuth.bastion_database_delete && tableData.length > 0"
                        :disabled="selectedRowKeys.length == 0"
                        icon="delete"
                        @click="batchDelete"
                        style="float: left; margin: -50px 10px 0 0"
                        >批量删除</a-button
                    >
                </div>
            </div>
        </a-card>
        <AddDataBaseGroup @father="getDataBaseGroupData" ref="AddDataBaseGroup"></AddDataBaseGroup>
        <AddDataBase
            @father="getDataBaseData(), getDataBaseGroupData()"
            :fatherData.sync="fatherData"
            ref="AddDataBase"
        ></AddDataBase>
        <LoginHostModal ref="LoginHostModal"></LoginHostModal>
    </div>
</template>

<script>
import { getDataBase, delDataBase, getDataBaseGroup, delDataBaseGroup } from '@/api/dataBase'
import ContentHeader from '@/views/components/ContentHeader'
import AddDataBaseGroup from './modal/addDataBaseGroup.vue'
import AddDataBase from './modal/addDataBase.vue'
import LoginHostModal from './modal/LoginHostModal.vue'

export default {
    data() {
        return {
            showTree: true,
            selectedKeys: ['all'],
            // 分组数据(左侧树)
            treeData: [
                {
                    key: 'all',
                    title: '全部数据库',
                    scopedSlots: { title: 'action' },
                    children: [],
                },
            ],
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
            searchList: [
                { name: '数据库名称', key: 'host_name' },
                { name: '连接地址', key: 'host_address' },
                { name: '数据库类型', key: 'database_type' },
            ],
            selectedRowKeys: [],
            tableData: [],
            columns: [
                {
                    title: '数据库名称',
                    dataIndex: 'host_name',
                    ellipsis: true,
                    scopedSlots: { customRender: 'name' },
                    width: 220,
                },
                {
                    title: '连接地址',
                    dataIndex: 'host_address',
                    ellipsis: true,
                },
                {
                    title: '数据库类型',
                    dataIndex: 'database_type',
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
            tableLoading: false,
            // 选中的分组id
            selectGroupId: undefined,
            // 分组数据(传给子组件)
            fatherData: [],
        }
    },
    mounted() {
        this.getDataBaseData()
        this.getDataBaseGroupData()
    },
    methods: {
        // 搜索
        searchTable(val) {
            this.search_data = val
            this.pagination.current = 1
            this.getDataBaseData()
        },
        // 批量删除
        batchDelete() {
            let _this = this
            this.$confirm({
                title: '确认删除吗？',
                onOk: function () {
                    delDataBase({ id_list: _this.selectedRowKeys }).then((res) => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getDataBaseData()
                            _this.selectedRowKeys = []
                        }
                    })
                },
            })
        },
        // 删除
        deleteDataBase(record) {
            let _this = this
            this.$confirm({
                title: '确认删除该主机吗？',
                onOk: function () {
                    delDataBase({ id: record.id }).then((res) => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getDataBaseData()
                        }
                    })
                },
            })
        },
        // 获取数据库数据
        getDataBaseData() {
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
            getDataBase(updata)
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
        // 获取分组数据(树)
        getDataBaseGroupData() {
            this.showTree = false
            let allNumber = 0
            getDataBaseGroup()
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
        // 选中分组(树)
        treeSelect(val) {
            this.selectGroupId = val[0]
            this.selectedKeys = val
            this.pagination.current = 1
            this.getDataBaseData()
        },
        // 删除分组
        deleteGroup(row) {
            let _this = this
            this.$confirm({
                title: '确认删除该分组吗?',
                onOk: function () {
                    return new Promise((resolve, reject) => {
                        delDataBaseGroup({ id: row.id })
                            .then((res) => {
                                if (res.code == 200) {
                                    _this.$message.success(res.message)
                                    if (row.id == _this.selectGroupId) {
                                        _this.selectedKeys = ['all']
                                        _this.selectGroupId = 'all'
                                    }
                                    _this.getDataBaseGroupData()
                                    _this.getDataBaseData()
                                    resolve()
                                } else {
                                    _this.$message.error(res.message)
                                    reject()
                                }
                            })
                            .catch((res) => {
                                reject()
                            })
                    })
                },
            })
        },
        // 刷新
        refresh() {
            this.pagination = this.$options.data().pagination
            this.getDataBaseData()
        },
        // table选择
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys
        },
        // 换页
        onChange(val) {
            this.pagination.total = val.total
            this.pagination.current = val.current
            this.pagination.pageSize = val.pageSize
            this.getDataBaseData()
        },
        handleLogin(row) {
            this.$refs.LoginHostModal.showModal(row, false, 'dataBase')
        },
    },
    components: {
        ContentHeader,
        AddDataBaseGroup,
        AddDataBase,
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