<template>
    <div>
        <content-header >
            <a-button slot="right" icon="arrow-left" type="primary" @click="$router.go(-1)">返回</a-button>
        </content-header>
        <a-card :loading="loading">
            <a-card title="基本信息">
                <a-row :gutter="[16, 16]">
                    <a-col :span="24">策略名称：{{ info.name }}</a-col>
                    <a-col :span="24">有效期：{{ info.start_time || '-' }} ~ {{ info.end_time || '-' }}</a-col>
                </a-row>
            </a-card>

            <a-tabs type="card" style="margin-top: 20px">
                <a-tab-pane tab="关联命令" key="1">
                    <a-tabs tab-position="left">
                        <a-tab-pane tab="命令" key="1"> <Command :commandList="commandList"></Command></a-tab-pane>
                        <a-tab-pane tab="命令组" key="2">
                            <CommandGroup :commandGroupList="commandGroupList"></CommandGroup
                        ></a-tab-pane>
                    </a-tabs>
                </a-tab-pane>
                <a-tab-pane tab="授权用户" key="2">
                    <a-tabs tab-position="left">
                        <a-tab-pane tab="授权用户" key="1"> <User :userList="userList"></User></a-tab-pane>
                        <a-tab-pane tab="授权用户组" key="2">
                            <Group :userGroupList="userGroupList"></Group
                        ></a-tab-pane>
                    </a-tabs>
                </a-tab-pane>
                <a-tab-pane tab="资源凭证" key="3">
                    <a-tabs tab-position="left">
                        <a-tab-pane tab="密码凭证" key="1">
                            <PasswordVoucher :password_credential_host_id="password_credential_host_id"></PasswordVoucher
                        ></a-tab-pane>
                        <a-tab-pane tab="SSH密钥" key="2">
                            <SSHKey :ssh_credential_host_id="ssh_credential_host_id"></SSHKey
                        ></a-tab-pane>
                        <a-tab-pane tab="凭证分组" key="3">
                            <VoucherGroup :credential_group="credential_group"></VoucherGroup
                        ></a-tab-pane>
                    </a-tabs>
                </a-tab-pane>
            </a-tabs>
        </a-card>
    </div>
</template>
<script>
import { getCommandStrategy } from '@/api/command-strategy'
import { readDirfiles } from '@/utils/util'
export default {
    components: {
        ...readDirfiles(require.context('../../../../visitPolicy/visitPolicyInfo/components', true, /\.vue$/)),
        ...readDirfiles(require.context('./components', true, /\.vue$/)),
    },
    data() {
        return {
            id: undefined,
            loading: false,
            info: {},
            ipLimitList: [
                { key: 1, name: '无' },
                { key: 2, name: '黑名单' },
                { key: 3, name: '白名单' },
            ],
			commandList:[],
			commandGroupList:[],
            userList: [],
            userGroupList: [],
            password_credential_host_id: [],
            ssh_credential_host_id: [],
            credential_group: [],
        }
    },
    methods: {
        getCommandStrategy() {
            this.loading = true
            getCommandStrategy({ id: this.id })
                .then((res) => {
                    this.info = res.data.strategy
					this.commandList = res.data.command.command || []
					this.commandGroupList = res.data.command.command_group || []
                    this.userList = res.data.user.user || []
                    this.userGroupList = res.data.user.user_group || []
                    this.password_credential_host_id = res.data.credential_host.password_credential_host_id || []
                    this.ssh_credential_host_id = res.data.credential_host.ssh_credential_host_id || []
                    this.credential_group = res.data.credential_host.credential_group || []
                })
                .finally(() => {
                    this.loading = false
                })
        },
    },
    mounted() {
        this.id = this.$route.query.id
        this.getCommandStrategy()
    },
}
</script>
<style scoped lang='less'>
</style>