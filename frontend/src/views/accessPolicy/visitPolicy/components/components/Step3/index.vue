<template>
    <div>
        <a-tabs v-model="activeTab" ref="tabs">
            <a-tab-pane v-for="item in tabList" :key="item.key" :tab="item.name"> </a-tab-pane>
        </a-tabs>
        <PasswordVoucher
            v-show="activeTab == 'PasswordVoucher'"
            ref="PasswordVoucher"
            :password_credential_host_id="password_credential_host_id"
        ></PasswordVoucher>
        <SSHKey v-show="activeTab == 'SSHKey'" ref="SSHKey" :ssh_credential_host_id="ssh_credential_host_id"></SSHKey>
        <VoucherGroup
            v-show="activeTab == 'VoucherGroup'"
            ref="VoucherGroup"
            :credential_group="credential_group"
        ></VoucherGroup>
    </div>
</template>
<script>
import PasswordVoucher from './components/PasswordVoucher.vue'
import SSHKey from './components/SSHKey.vue'
import VoucherGroup from './components/VoucherGroup.vue'
export default {
    components: { PasswordVoucher, SSHKey, VoucherGroup },
    props: {
        credential_host: {
            type: Object,
            default: () => {
                return {}
            },
        },
    },
    watch: {
        credential_host: {
            handler(val) {
                const password_credential_host_id = val.password_credential_host_id || []
                const ssh_credential_host_id = val.ssh_credential_host_id || []
                const credential_group = val.credential_group || []

                this.password_credential_host_id = password_credential_host_id.map((item) => item.id + '')
                this.ssh_credential_host_id = ssh_credential_host_id.map((item) => item.id + '')
                this.credential_group = credential_group.map((item) => item.id + '')
            },
        },
    },
    data() {
        return {
            tabList: [
                { key: 'PasswordVoucher', name: '关联密码凭证' },
                { key: 'SSHKey', name: '关联SSH密钥' },
                { key: 'VoucherGroup', name: '关联凭证分组' },
            ],
            activeTab: 'PasswordVoucher',
            password_credential_host_id: [], //密码凭证
            ssh_credential_host_id: [], //ssh凭证
            credential_group: [], //凭证分组
        }
    },
    methods: {
        resetFormData() {
            this.activeTab = this.$options.data().activeTab
            this.tabList.forEach((item) => {
                this.$refs[item.key]?.resetData()
            })
        },
        getFormData() {
            const password_credential_host_id = this.$refs.PasswordVoucher.getFormData()
            const ssh_credential_host_id = this.$refs.SSHKey.getFormData()
            const credential_group = this.$refs.VoucherGroup.getFormData()
            return { password_credential_host_id, ssh_credential_host_id, credential_group }
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
</style>