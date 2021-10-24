<template>
    <div>
        <a-modal @ok="onSubmit" @cancel="onClose" :confirmLoading="btnLoading" width="900px" v-model="visible" title="添加凭据">
            <a-radio-group v-model="credential_type" @change="credentialTypeChange" button-style="solid">
                <a-radio-button value="password">
                    密码凭证
                </a-radio-button>
                <a-radio-button value="ssh">
                    SSH密钥
                </a-radio-button>
            </a-radio-group>

            <a-transfer :operations="operations" :titles="titles" :list-style="listStyle" style="margin:20px 0 0 0" @change="handleChange" :dataSource="mockData" :targetKeys="targetKeys" show-search :render="item => item.title" />

        </a-modal>
    </div>
</template>

<script>
import { getCredential } from "@/api/credential"
import { editGroup } from "@/api/group"
export default {
    data() {
        return {
            visible: false,
            credential_type: "password",
            // 整体数据
            mockData: [],
            // 右侧数据的key值
            targetKeys: [],
            //全部密码凭证选项(穿梭框) 
            allpasswordList: [],
            // 展示的密码凭证选项(编辑凭证分组时已经绑定过的凭证不显示)
            passwordList: [],
            //被选中的密码凭证(切换凭证类型时进行记录) 
            selectedpasswordList: [],
            //全部ssh凭证选项(穿梭框) 
            allsshList: [],
            // 展示的SSH凭证选项(编辑凭证分组时已经绑定过的凭证不显示)
            sshList: [],
            //被选中的密码凭证(切换凭证类型时进行记录) 
            selectedsshList: [],
            listStyle: {
                width: '330px',
                height: '420px',
            },
            titles: [],
            titles1: ['可添加的密码凭据', '已选择的密码凭据'],
            titles2: ['可添加的SSH密钥', '已选择的SSH密钥'],
            operations: ['加入右侧', '加入左侧'],
            btnLoading: false,
        }
    },
    mounted() {
        // this.getAllCredential()
    },
    methods: {
        show(record) {
            this.activeGroup = record
            this.visible = true
            this.getAllCredential()
            this.titles = this.titles1
            let arr1 = [], arr2 = []
            record.credential.password_credential.map(item => {
                arr1.push(item.id + "")
            })
            this.selectedpasswordList = arr1
            record.credential.ssh_credential.map(item => {
                arr2.push(item.id + "")
            })
            this.selectedsshList = arr2
            this.targetKeys = this.selectedpasswordList
        },
        // 凭证分类change
        credentialTypeChange(event) {
            if (event.target.value == "password") {
                this.mockData = this.passwordList
                this.selectedsshList = this.targetKeys
                this.targetKeys = this.selectedpasswordList
                this.titles = this.titles1
            } else {
                this.mockData = this.sshList
                this.selectedpasswordList = this.targetKeys
                this.targetKeys = this.selectedsshList
                this.titles = this.titles2
            }
        },
        // 穿梭框
        handleChange(nextTargetKeys, direction, moveKeys) {
            this.targetKeys = nextTargetKeys;
        },
        // 获取所有凭据(password与ssh分开)
        getAllCredential() {
            getCredential({ all_data: "1", credential_type: "password" }).then(res => {
                if (res.code == 200 && res.data) {
                    let arr = []
                    res.data.map(item => {
                        arr.push({
                            key: item.id + "",
                            title: item.name
                        })
                    })
                    this.allpasswordList = arr
                    this.passwordList = this.allpasswordList
                    this.mockData = this.passwordList
                }
            })
            getCredential({ all_data: "1", credential_type: "ssh_key" }).then(res => {
                if (res.code == 200 && res.data) {
                    let arr = []
                    res.data.map(item => {
                        arr.push({
                            key: item.id + "",
                            title: item.name
                        })
                    })
                    this.allsshList = arr
                    this.sshList = this.allsshList
                }
            })
        },
        // 提交
        onSubmit() {
            this.btnLoading = true
            let updata = this.activeGroup
            if (this.credential_type == "password") {
                this.selectedpasswordList = this.targetKeys
            } else {
                this.selectedsshList = this.targetKeys
            }

            updata.credential_password_list = this.selectedpasswordList
            updata.credential_ssh_list = this.selectedsshList
            updata.id = this.activeGroup.id
            editGroup(updata).then(res => {
                if (res.code == 200) {
                    this.$message.success(res.message)
                    this.onClose()
                }
            }).finally(() => {
                this.btnLoading = false
            })
        },
        onClose() {
            this.visible = false
            this.targetKeys = []
            this.$emit("father")
            this.selectedpasswordList = []
            this.selectedsshList = []
        }
    }
}
</script>

<style lang="less" scoped>
</style>