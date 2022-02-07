<template>
    <div class="hostDetails_main">
        <content-header ref="contentHeader">
            <a-button slot="right" icon="arrow-left" type="primary" @click="$router.go(-1)">返回</a-button>
        </content-header>
        <div class="content">
            <a-card class="infomation" title="基础信息">
                <p class="info">
                    <span>数据库名称：{{hostInfo.host_name}}</span>
                    <span>数据库类型：{{hostInfo.database_type}}</span>
                    <span>连接地址：{{hostInfo.host_address}}</span>
                    <span>网络代理：{{hostInfo.network_proxy&&hostInfo.network_proxy.name || "--"}}</span>

                </p>
                <p class="info">
                    <span>端口：{{hostInfo.port}}</span>
                    <span>所属分组：{{hostInfo.group&&hostInfo.group.name}}</span>
                    <span>创建时间：{{hostInfo.create_time}}</span>
                    <span></span>
                </p>
                <p>描述：{{hostInfo .description||"--"}}</p>
            </a-card>

            <a-tabs type="card">
                <a-tab-pane key="1" tab="关联凭证"></a-tab-pane>
            </a-tabs>

            <div class="relation">
                <a-menu :selectedKeys="selectedKeys" @select="voucherTypeChange" class="left" mode="inline" style="margin:20px 0 0 0">
                    <a-menu-item key="password">密码凭证</a-menu-item>
                    <a-menu-item key="ssh">SSH密钥</a-menu-item>
                    <a-menu-item key="group">凭证分组</a-menu-item>
                </a-menu>
                <a-table :pagination="pagination" class="right" style="padding:20px" :columns="columns" :data-source="tableData">
                    <template slot="login_type" slot-scope="text">
                        {{text=="auto"?"自动登录":"手动登录"}}
                    </template>
                    <template slot="description" slot-scope="text">
                        {{text||"--"}}
                    </template>
                    <template slot="action" slot-scope="text,record">
                        <a v-if="$store.state.btnAuth.btnAuth.bastion_database_credential_delete" @click="remove(record)">移除</a>
                    </template>
                </a-table>
            </div>

        </div>

    </div>
</template>

<script>
import { removeCredentialFromHost } from "@/api/host"
import { getDataBase } from "@/api/dataBase"

export default {
    data() {
        return {
            hostInfo: {},
            tableData: [],
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
            columns3: [
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
            selectedKeys: ["password"],
            pagination: {
                showTotal: total => `共有 ${total} 条数据`,
                showSizeChanger: true, showQuickJumper: true,
            },
        }
    },
    mounted() {
        this.getHostData(true)
    },
    methods: {
        // 移除凭据
        remove(record) {
            let _this = this
            this.$confirm({
                title: "确认移除该凭据吗？",
                onOk: function () {
                    let updata = {
                        host: _this.$route.query.id
                    }
                    if (record.type == "password" || record.type == "ssh") {
                        updata.credential = record.id
                    } else if (record.type == "group") {
                        updata.credential_group = record.id
                    }
                    removeCredentialFromHost(updata).then(res => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getHostData()
                        }
                    })
                }
            })
        },
        voucherTypeChange(event) {
            this.selectedKeys = [event.key]
            if (event.key == "password") {
                this.columns = this.columns1
                this.tableData = this.passwordTableList
            } else if (event.key == "ssh") {
                this.columns = this.columns2
                this.tableData = this.sshTableList
            } else if (event.key == "group") {
                this.columns = this.columns3
                this.tableData = this.groupTableList
            }
        },
        // 获取主机数据
        getHostData(first) {
            getDataBase({ id: this.$route.query.id }).then(res => {
                if (res.code == 200 && res.data) {
                    this.hostInfo = res.data
                    this.$refs.contentHeader.mainTitle1 = res.data.host_name
                    // 将绑定凭据进行处理
                    if (res.data.credential.password_credential) {
                        this.passwordTableList = res.data.credential.password_credential
                        this.passwordTableList.map(item => {
                            item.key = item.id
                            item.type = "password"
                        })
                    } else {
                        this.passwordTableList = []
                    }
                    if (res.data.credential.ssh_credential) {
                        this.sshTableList = res.data.credential.ssh_credential
                        this.sshTableList.map(item => {
                            item.key = item.id
                            item.type = "ssh"
                        })
                    } else {
                        this.sshTableList = []
                    }
                    if (res.data.credential.credential_group) {
                        this.groupTableList = res.data.credential.credential_group
                        this.groupTableList.map(item => {
                            item.key = item.id
                            item.type = "group"
                        })
                    } else {
                        this.groupTableList = []
                    }


                    if (first) {
                        // 第一次请求数据
                        this.columns = this.columns1
                        this.tableData = this.passwordTableList
                    } else {
                        // 保持凭据种类
                        if (this.selectedKeys[0] == "password") {
                            this.tableData = this.passwordTableList
                        } else if (this.selectedKeys[0] == "ssh") {
                            this.tableData = this.sshTableList
                        } else if (this.selectedKeys[0] == "group") {
                            this.tableData = this.groupTableList
                        }
                    }
                }
            })
        },
    }
}
</script>

<style lang="less" scoped>
.hostDetails_main {
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
        .relation {
            display: flex;
            .left {
                flex: 120px 0 0;
            }
            .right {
                flex: 0px 1 1;
            }
        }
    }
}
/deep/.ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
    background: none;
}
.ant-menu-item {
    background: none;
}
.relation {
    border: 1px solid #e8e8e8;
    border-top: none;
    margin: -16px 0 0 0;
    padding: 5px 0 0 0;
}
.ant-menu-item {
    margin: 0;
}
</style>