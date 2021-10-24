<template>
    <div class="passwordDetails_main">
        <content-header ref="contentHeader">
            <a-button slot="right" icon="arrow-left" type="primary" @click="$router.go(-1)">返回</a-button>
        </content-header>
        <div class="content">
            <a-card class="infomation" title="基础信息">
                <p class="info">
                    <span>凭证名称：{{credentialInfo.name}}</span>
                    <span>登录方式：{{credentialInfo.login_type=="auto"?"自动登录":"手动登录"}}</span>
                    <span>资源账户: {{credentialInfo.login_name}}</span>
                </p>
                <p>描述：{{credentialInfo.description||"--"}}</p>
            </a-card>

            <a-tabs type="card">
                <a-tab-pane key="1" tab="关联的主机"></a-tab-pane>
                <!-- <a-tab-pane key="2" tab="关联的应用"></a-tab-pane> -->
                <a-button v-if="$store.state.btnAuth.btnAuth.bastion_ssh_resource_create" @click="$refs.AssociatedResources.show(credentialInfo)" type="primary" slot="tabBarExtraContent">关联资源</a-button>
            </a-tabs>
            <a-table style="padding:20px" :columns="columns" :data-source="tableData">
                <template slot="action" slot-scope="text,record">
                    <a v-if="$store.state.btnAuth.btnAuth.bastion_ssh_resource_delete" @click="remove(record)">移除</a>
                </template>
            </a-table>
        </div>
        <AssociatedResources @father="getCredentialData()" ref="AssociatedResources"></AssociatedResources>
    </div>
</template>

<script>
import { getCredential } from "@/api/credential"
import { removeCredentialFromHost } from "@/api/host"
import AssociatedResources from "./model/associatedResources.vue"
export default {
    data() {
        return {
            tableData: [],
            columns: [
                {
                    title: '主机名称',
                    dataIndex: 'host_name',
                    scopedSlots: { customRender: 'name' },
                },
                {
                    title: '主机地址',
                    dataIndex: 'host_address',
                },
                {
                    title: '系统类型',
                    dataIndex: 'system_type',
                },
                {
                    title: '协议类型',
                    dataIndex: 'protocol_type',
                },
                {
                    title: '操作',
                    scopedSlots: { customRender: 'action' },
                },
            ],
            credentialInfo: {},
            hidden: true,
        }
    },
    mounted() {
        this.getCredentialData()
    },
    methods: {
        remove(record) {
            let _this = this
            this.$confirm({
                title: "确认移除该资源吗？",
                onOk: function () {
                    removeCredentialFromHost({ credential: _this.$route.query.id, host: record.id }).then(res => {
                        if (res.code == 200) {
                            _this.$message.success(res.message)
                            _this.getCredentialData()
                        }
                    })
                }
            })
        },
        // 获取主机数据
        getCredentialData() {
            getCredential({ id: this.$route.query.id }).then(res => {
                this.credentialInfo = res.data
                res.data.host_list.map(item => {
                    item.key = item.id
                })
                this.hostList = res.data.host_list
                this.tableData = this.hostList
                this.$refs.contentHeader.mainTitle1=res.data.name
            })
        }
    },
    components: { AssociatedResources }
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