<template>
    <div class="password_main">
        <ContentHeader>
            <div slot="docs">
                SSH密钥凭证支持设置密码，需要提前将公钥放置在对应用户家目录的.ssh/authorized_keys文件中。
            </div>
        </ContentHeader>

        <a-card>
            <div class="search_box">
                <a-input-search allowClear placeholder="请输入搜索名称" @search="onSearch" style="width:200px;"></a-input-search>
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_ssh_create" @click="$refs.AddSsh.show()" style="float:right;" icon="plus" type="primary">新建</a-button>
            </div>
            <a-table :loading="tableLoading" @change="onChange" :pagination="pagination" :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }" :columns="columns" :data-source="tableData">
                <template slot="name" slot-scope="text,record">
                    <a :title="text" v-if="$store.state.btnAuth.btnAuth.bastion_password_details" @click="$router.push({path:'/voucher/ssh/sshDetails',query:{id:record.id}})">{{text}}</a>
                    <span :title="text" v-else>{{text}}</span>
                </template>
                <template slot="login_type" slot-scope="text">
                    {{text=="auto"?"自动登录":"手动登录"}}
                </template>
                <template slot="description" slot-scope="text">
                    {{text||"--"}}
                </template>
                <template slot="relation" slot-scope="text,record">
                    <a v-if="$store.state.btnAuth.btnAuth.bastion_password_details" @click="$router.push({path:'/voucher/ssh/sshDetails',query:{id:record.id}})">{{text}}</a>
                    <span v-else>{{text}}</span>
                </template>
                <template slot="action" slot-scope="text,record">
                    <a-button size="small" type='link' v-if="$store.state.btnAuth.btnAuth.bastion_password_details" @click="$router.push({path:'/voucher/ssh/sshDetails',query:{id:record.id}})">查看</a-button>
                    <a-button size="small" type='link' v-if="$store.state.btnAuth.btnAuth.bastion_ssh_update" @click="$refs.AddSsh.show(record)">编辑</a-button>
                    <a-button size="small" type='link' v-if="$store.state.btnAuth.btnAuth.bastion_ssh_delete" @click="deletePassword(record)" style="color:#333">删除</a-button>
                </template>
            </a-table>
            <a-button v-if="tableData.length>0" :disabled="selectedRowKeys.length==0" @click="batchDelete" style="float:left;margin:-50px 10px 0 0">批量删除</a-button>
        </a-card>

        <AddSsh @father="getCredentialData()" ref="AddSsh"></AddSsh>
    </div>
</template>

<script>
import ContentHeader from "@/views/components/ContentHeader"
import AddSsh from "./model/addSsh.vue"
import { getCredential, delCredential } from "@/api/credential"
export default {
    data() {
        return {
            tableData: [],
            columns: [
                {
                    title: '凭证名称',
                    dataIndex: 'name',
                    ellipsis: true,
                    scopedSlots: { customRender: 'name' },
                },
                {
                    title: '资源账户',
                    dataIndex: 'login_name',
                    ellipsis: true,
                },
                {
                    title: '登录方式',
                    dataIndex: 'login_type',
                    ellipsis: true,
                    scopedSlots: { customRender: 'login_type' },
                },
                {
                    title: '关联主机',
                    dataIndex: 'relation',
                    ellipsis: true,
                    scopedSlots: { customRender: 'relation' },
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
                    align: "center",
                },
            ],
            selectedRowKeys: [],
            pagination: {
                total: 0, current: 1, pageSize: 10, showTotal: total => `共有 ${total} 条数据`, search_type: "name",
                search_data: undefined, showSizeChanger: true, showQuickJumper: true
            },
            tableLoading: false,
        }
    },
    mounted() {
        this.getCredentialData()
    },
    methods: {
        // 搜索
        onSearch(val) {
            this.pagination.search_data = val
            this.pagination.current = 1
            this.getCredentialData()
        },
        // 换页
        onChange(val) {
            this.pagination.total = val.total
            this.pagination.current = val.current
            this.pagination.pageSize = val.pageSize
            this.getCredentialData()
        },
        // 删除
        deletePassword(record) {
            let _this = this
            this.$confirm({
                title: "确认删除该密码凭证吗？",
                onOk: function () {
                    delCredential({ id: record.id }).then(res => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getCredentialData()
                        }
                    })
                }
            })
        },
        // 批量删除
        batchDelete() {
            let _this = this
            this.$confirm({
                title: "确认删除吗？",
                onOk: function () {
                    delCredential({ id_list: _this.selectedRowKeys }).then(res => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getCredentialData()
                            _this.selectedRowKeys = []
                        }
                    })
                }
            })
        },
        // table选择
        onSelectChange(selectedRowKeys) {
            this.selectedRowKeys = selectedRowKeys;
        },
        // 获取凭据数据
        getCredentialData() {
            this.tableLoading = true
            let updata = {
                current: this.pagination.current,
                pageSize: this.pagination.pageSize,
                credential_type: "ssh_key",
            }
            if (this.pagination.search_data) {
                updata.search_type = "name"
                updata.search_data = this.pagination.search_data
            }
            getCredential(updata).then(res => {
                if (res.code == 200 && res.data) {
                    this.pagination = {
                        total: res.data.total,
                        current: res.data.current,
                        pageSize: res.data.pageSize,
                    }
                    res.data.data.map(item => {
                        item.key = item.id
                        item.relation = item.host_list.length
                    })
                    this.tableData = res.data.data
                } else {
                    this.tableData = []
                }
            }).finally(() => {
                this.tableLoading = false
            })
        }
    },
    components: {
        ContentHeader,
        AddSsh,
    }
}
</script>
<style lang="less" scoped>
.password_main {
    background: #fff;
}
.search_box {
    height: 52px;
}
</style>