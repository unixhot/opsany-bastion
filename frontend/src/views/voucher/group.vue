<template>
    <div class="group_main">
        <ContentHeader>
            <div slot="docs">将凭证进行分组管理后可以直接关联到访问策略，适用于多账户同时关联场景。</div>
        </ContentHeader>
        <a-card>
            <div class="search_box">
                <a-input-search
                    allowClear
                    placeholder="请输入搜索名称"
                    @search="onSearch"
                    style="width: 200px"
                ></a-input-search>
                <a-button
                    v-if="$store.state.btnAuth.btnAuth.bastion_credential_group_create"
                    @click="$refs.AuthModal.handleAuth('create-voucher-group').then(() => $refs.AddGroup.show())"
                    style="float: right"
                    icon="plus"
                    type="primary"
                    >新建</a-button
                >
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
                        :title="text"
                        v-if="$store.state.btnAuth.btnAuth.bastion_password_details"
                        @click="
                            $refs.AuthModal.handleAuth('get-voucher-group').then(() =>
                                $router.push({ path: '/voucher/group/groupDetails', query: { id: record.id } })
                            )
                        "
                        >{{ text }}</a
                    >
                    <span :title="text" v-else>{{ text }}</span>
                </template>
                <template slot="description" slot-scope="text">
                    {{ text || '--' }}
                </template>
                <template slot="voucherTitle">
                    <span>关联资源凭证</span>
                    <a-tooltip placement="top" title="密码凭证/SSH密钥" arrow-point-at-center>
                        <a-icon style="margin: 0 0 0 3px; color: #666" type="exclamation-circle" />
                    </a-tooltip>
                </template>
                <template slot="voucher" slot-scope="text, record">
                    <a
                        v-if="$store.state.btnAuth.btnAuth.bastion_password_details"
                        @click="
                            $refs.AuthModal.handleAuth('get-voucher-group').then(() =>
                                $router.push({ path: '/voucher/group/groupDetails', query: { id: record.id } })
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
                        v-if="$store.state.btnAuth.btnAuth.bastion_password_details"
                        @click="
                            $refs.AuthModal.handleAuth('get-voucher-group').then(() =>
                                $router.push({ path: '/voucher/group/groupDetails', query: { id: record.id } })
                            )
                        "
                        >查看</a-button
                    >
                    <a-button
                        size="small"
                        type="link"
                        v-if="$store.state.btnAuth.btnAuth.bastion_credential_group_update"
                        @click="
                            $refs.AuthModal.handleAuth('modify-voucher-group').then(() => $refs.AddGroup.show(record))
                        "
                        >编辑</a-button
                    >
                    <a-button
                        size="small"
                        type="link"
                        v-if="$store.state.btnAuth.btnAuth.bastion_credential_group_delete"
                        @click="$refs.AuthModal.handleAuth('delete-voucher-group').then(() => deleteGroup(record))"
                        style="color: #333"
                        >删除</a-button
                    >
                </template>
            </a-table>
            <a-button
                v-if="tableData.length > 0"
                :disabled="selectedRowKeys.length == 0"
                @click="$refs.AuthModal.handleAuth('delete-voucher-group').then(() => batchDelete())"
                style="float: left; margin: -50px 10px 0 0"
                >批量删除</a-button
            >
        </a-card>
        <AddGroup @father="getGroupData" ref="AddGroup"></AddGroup>
        <AuthModal ref="AuthModal"></AuthModal>
    </div>
</template>

<script>
import ContentHeader from '@/views/components/ContentHeader'
import AddGroup from './model/addGroup.vue'
import { getGroup, delGroup } from '@/api/group'
import { getPageAuth } from '@/utils/pageAuth'

export default {
    data() {
        return {
            tableData: [],
            columns: [
                {
                    title: '分组名称',
                    dataIndex: 'name',
                    ellipsis: true,
                    scopedSlots: { customRender: 'name' },
                },

                {
                    title: '创建时间',
                    dataIndex: 'create_time',
                    ellipsis: true,
                },
                {
                    dataIndex: 'voucher',
                    ellipsis: true,
                    slots: { title: 'voucherTitle' },
                    scopedSlots: { customRender: 'voucher' },
                },
                {
                    title: '描述',
                    dataIndex: 'description',
                    ellipsis: true,
                    scopedSlots: { customRender: 'description' },
                },
                {
                    title: '操作',
                    scopedSlots: { customRender: 'action' },
                    width: 250,
                    align: 'center',
                },
            ],
            selectedRowKeys: [],
            pagination: {
                total: 0,
                current: 1,
                pageSize: 10,
                search_type: 'name',
                search_data: undefined,
                showTotal: (total) => `共有 ${total} 条数据`,
                showSizeChanger: true,
                showQuickJumper: true,
            },
            tableLoading: false,
        }
    },
    async mounted() {
        const hasAuth = await getPageAuth(this, 'visit-voucher-group')
        if (hasAuth) {
            this.getGroupData()
        }
    },
    methods: {
        // 搜索
        onSearch(val) {
            this.pagination.search_data = val
            this.pagination.current = 1
            this.getGroupData()
        },
        // 批量删除
        batchDelete() {
            let _this = this
            this.$confirm({
                title: '确认删除吗？',
                onOk: function () {
                    delGroup({ id_list: _this.selectedRowKeys }).then((res) => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getGroupData()
                            _this.selectedRowKeys = []
                        }
                    })
                },
            })
        },
        // table选择
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys
        },
        // 获取分组数据
        getGroupData() {
            this.tableLoading = true
            let updata = {
                current: this.pagination.current,
                pageSize: this.pagination.pageSize,
            }
            if (this.pagination.search_data) {
                updata.search_type = this.pagination.search_type
                updata.search_data = this.pagination.search_data
            }
            getGroup(updata)
                .then((res) => {
                    if (res.code == 200 && res.data) {
                        this.pagination.total = res.data.total
                        this.pagination.current = res.data.current
                        this.pagination.pageSize = res.data.pageSize
                        res.data.data.map((item) => {
                            item.key = item.id
                            item.voucher =
                                item.credential.password_credential.length + '/' + item.credential.ssh_credential.length
                        })
                        this.tableData = res.data.data
                    } else {
                        this.tableData = []
                    }
                })
                .finally(() => {
                    this.tableLoading = false
                })
        },
        // 删除
        deleteGroup(record) {
            let _this = this
            this.$confirm({
                title: '确认删除该分组吗？',
                onOk: function () {
                    delGroup({ id: record.id }).then((res) => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getGroupData()
                        }
                    })
                },
            })
        },
        // 换页
        onChange(val) {
            this.pagination.total = val.total
            this.pagination.current = val.current
            this.pagination.pageSize = val.pageSize
            this.getGroupData()
        },
    },
    components: {
        ContentHeader,
        AddGroup,
    },
}
</script>
<style lang="less" scoped>
.group_main {
    background: #fff;
}
.search_box {
    height: 52px;
}
</style>