<template>
    <div class="passwordDetails_main">
        <content-header ref="contentHeader">
            <a-button slot="right" icon="arrow-left" type="primary" @click="$router.go(-1)">返回</a-button>
        </content-header>
        <div class="content">
            <a-card class="infomation" title="基础信息">
                <p>分组名称：{{groupInfo.name}}</p>
                <p>描述：{{groupInfo.description||"--"}}</p>
            </a-card>

            <a-tabs @change="tabChange" type="card">
                <a-tab-pane key="password" tab="密码凭证"></a-tab-pane>
                <a-tab-pane key="ssh_key" tab="SSH密钥"></a-tab-pane>
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_credential_group_credential_create" @click="$refs.AddVoucher.show(groupInfo)" type="primary" slot="tabBarExtraContent">添加凭证</a-button>
            </a-tabs>
            <a-table style="padding:20px" :columns="columns" :data-source="tableData">
                <template slot="login_type" slot-scope="text">
                    {{text=="auto"?"自动登录":"手动登录"}}
                </template>
                <template slot="description" slot-scope="text">
                    {{text||"--"}}
                </template>
                <template slot="action" slot-scope="text,record">
                    <a v-if="$store.state.btnAuth.btnAuth.bastion_credential_group_credential_delete" @click="remove(record)">移除</a>
                </template>
            </a-table>
        </div>
        <AddVoucher @father="getGroupData" ref="AddVoucher"></AddVoucher>
    </div>
</template>

<script>
import { getGroup, removeCredential } from "@/api/group"
import AddVoucher from "./model/addvoucher.vue"
export default {
    data() {
        return {
            tableData: [

            ],
            columns: [],
            columns1: [
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
                    title: '描述',
                    dataIndex: 'description',
                    ellipsis: true,
                    scopedSlots: { customRender: 'description' },
                },
                {
                    title: '操作',
                    ellipsis: true,
                    scopedSlots: { customRender: 'action' },
                    width: 100,
                },
            ],
            columns2: [
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
                    title: '描述',
                    dataIndex: 'description',
                    ellipsis: true,
                    scopedSlots: { customRender: 'description' },
                },
                {
                    title: '操作',
                    scopedSlots: { customRender: 'action' },
                    width: 100,
                },
            ],
            groupInfo: {},
            hidden: true,
        }
    },
    mounted() {
        this.getGroupData()
    },
    methods: {
        remove(record) {
            let _this = this
            this.$confirm({
                title: "确认移除该凭据吗？",
                onOk: function () {
                    removeCredential({ credential: record.id, credential_group: _this.$route.query.id }).then(res => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getGroupData()
                        }
                    })
                }
            })
        },
        tabChange(val) {
            if (val == "password") {
                this.columns = this.columns1
                this.tableData = this.passwordTableData
            } else {
                this.columns = this.columns2
                this.tableData = this.sshTableData
            }
        },
        // 获取分组信息
        getGroupData() {
            getGroup({ id: this.$route.query.id }).then(res => {
                if (res.data && res.data.credential) {
                    res.data.credential.password_credential.map(item => {
                        item.key = item.id
                    })
                    res.data.credential.ssh_credential.map(item => {
                        item.key = item.id
                    })
                    this.passwordTableData = res.data.credential.password_credential
                    this.sshTableData = res.data.credential.ssh_credential
                    this.tableData = this.passwordTableData
                    this.$refs.contentHeader.mainTitle1=res.data.name
                }
                this.columns = this.columns1
                this.groupInfo = res.data
            })
        }
    },
    components: { AddVoucher }
}
</script>

<style lang="less" scoped>
.passwordDetails_main {
    background: #fff;
    .card {
        width: 100%;
        /deep/ .ant-card-body {
            align-items: center;
            display: flex;
            padding: 18px;
            justify-content: space-between;
            &::before {
                content: none;
            }
            &::after {
                content: none;
            }
        }
        .title {
            font-size: 22px;
            font-weight: bold;
        }
        .breadcrumb {
            margin-left: 30px;
        }
        .docs {
            display: inline-block;
            margin-left: 40px;
            color: #00ac63;
        }
    }
    .content {
        padding: 20px;
        .infomation {
            margin: 0 0 20px 0;
            .info {
                display: flex;
                justify-content: space-between;

                span {
                    flex: 0px 1 1;
                }
            }
        }
    }
}
</style>