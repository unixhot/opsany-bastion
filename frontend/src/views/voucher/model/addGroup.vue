<template>
    <div>
        <a-drawer :body-style="{ paddingBottom: '80px' }" width="980px" :title="title" placement="right" :visible="visible" @close="onClose">
            <a-form :form="groupForm" :label-col="{ span: 2 }" :wrapper-col="{ span: 22 }">
                <a-form-item label="分组名称">
                    <a-input placeholder="请输入分组名称" v-decorator="['name', { rules: [{ required: true, message: '请输入分组名称' }] }]"></a-input>
                </a-form-item>
                <a-form-item label="描述">
                    <a-textarea placeholder="请输入，最多输入200个汉字或字符" v-decorator="['description', { rules: [{ required: false},{max:200,message:'最多输入200个汉字或字符'}] }]"></a-textarea>
                </a-form-item>

                <a-form-item label="添加凭证">
                    <a-radio-group v-model="credential_type" @change="credentialTypeChange" button-style="solid">
                        <a-radio-button value="password">
                            密码凭证
                        </a-radio-button>
                        <a-radio-button value="ssh">
                            SSH密钥
                        </a-radio-button>
                    </a-radio-group>
                </a-form-item>
                <a-transfer :operations="operations" :titles="titles" :list-style="listStyle" style="margin:0 0 0 8.33%" @change="handleChange" :dataSource="mockData" :targetKeys="targetKeys" show-search :render="item => item.title" />
            </a-form>
            <footer>
                <a-button style="margin:0 8px 0 0" @click="onClose">取消</a-button>
                <a-button :loading="btnLoading" @click="onSubmit" type="primary">保存</a-button>
            </footer>
        </a-drawer>
    </div>
</template>

<script>
import { addGroup, editGroup } from "@/api/group"
import { getCredential } from "@/api/credential"
export default {
    data() {
        return {
            title: "",
            visible: false,
            groupForm: this.$form.createForm(this, { name: "groupForm" }),
            // 整体数据
            mockData: [],
            // 右侧数据的key值
            targetKeys: [],
            // 确认按钮loading
            btnLoading: false,
            isEdit: false,
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
            credential_type: "password",

            listStyle: {
                width: '360px',
                height: '420px',
            },
            titles: [],
            titles1: ['可添加的密码凭据', '已选择的密码凭据'],
            titles2: ['可添加的SSH密钥', '已选择的SSH密钥'],
            operations: ['加入右侧', '加入左侧'],
        }
    },
    mounted() {
        // this.getAllCredential()
    },
    methods: {
        credentialTypeChange(event) {
            if (event.target.value == "password") {
                this.mockData = this.passwordList
                this.selectedsshList = this.targetKeys
                this.targetKeys = this.selectedpasswordList
                this.titles=this.titles1
            } else {
                this.mockData = this.sshList
                this.selectedpasswordList = this.targetKeys
                this.targetKeys = this.selectedsshList
                this.titles=this.titles2
            }
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
        // 抽屉显示
        show(record) {
            this.getAllCredential()
            this.visible = true
            this.titles = this.titles1
            if (record) {
                this.activeGroup = record
                this.isEdit = true
                this.title = "编辑凭证分组"
                this.loginType = record.login_type
                this.$nextTick(function () {
                    this.groupForm.setFieldsValue({
                        name: record.name,
                        login_type: record.login_type,
                        login_name: record.login_name,
                        login_password: record.login_password,
                        description: record.description,
                    })
                })

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
            } else {
                this.isEdit = false
                this.title = "新建凭证分组"
            }
        },
        // 抽屉关闭
        onClose() {
            this.visible = false
            this.groupForm.resetFields()
            this.targetKeys = []
            this.selectedpasswordList = []
            this.selectedsshList = []
            this.credential_type = "password"
            this.$emit("father")
        },
        // 穿梭框
        handleChange(nextTargetKeys, direction, moveKeys) {
            this.targetKeys = nextTargetKeys;
        },
        // 提交
        onSubmit() {
            this.groupForm.validateFields((err, values) => {
                if (!err) {
                    this.btnLoading = true
                    let updata = values
                    if (this.credential_type == "password") {
                        this.selectedpasswordList = this.targetKeys
                    } else {
                        this.selectedsshList = this.targetKeys
                    }
                    updata.credential_password_list = this.selectedpasswordList
                    updata.credential_ssh_list = this.selectedsshList
                    if (this.isEdit) {
                        updata.id = this.activeGroup.id
                        editGroup(updata).then(res => {
                            if (res.code == 200) {
                                this.$message.success(res.message)
                                this.onClose()
                            }
                        }).finally(() => {
                            this.btnLoading = false
                        })
                    } else {
                        addGroup(updata).then(res => {
                            if (res.code == 200) {
                                this.$message.success(res.message)
                                this.onClose()
                            }
                        }).finally(() => {
                            this.btnLoading = false
                        })
                    }

                }
            })
        }
    }
}
</script>

<style lang="less" scoped>
footer {
    position: absolute;
    right: 0;
    bottom: 0;
    width: 100%;
    border-top: 1px solid #e9e9e9;
    padding: 10px 16px;
    background: #fff;
    text-align: right;
    z-index: 2;
}
</style>