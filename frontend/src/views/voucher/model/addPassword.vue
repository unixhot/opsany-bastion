<template>
    <div>
        <a-drawer :body-style="{ paddingBottom: '80px' }" width="980px" :title="title" placement="right" :visible="visible" @close="onClose">
            <a-form :form="passwordForm" :label-col="{ span: 2 }" :wrapper-col="{ span: 22 }">
                <a-form-item label="凭证名称">
                    <a-input placeholder="请输入凭证名称" v-decorator="['name', { rules: [{ required: true, message: '请输入凭证名称' }] }]"></a-input>
                </a-form-item>
                <a-form-item label="登录方式">
                    <a-radio-group @change="loginTypeChange" v-decorator="['login_type', { initialValue: 'auto' ,rules: [{ required: true, message: '请选择登录方式' }] }]">
                        <a-radio value="auto">
                            自动登录
                        </a-radio>
                        <a-radio value="hand">
                            手动登录
                        </a-radio>
                    </a-radio-group>
                </a-form-item>
                <a-form-item label="资源账户">
                    <a-input placeholder="请输入资源账户的名称" v-decorator="['login_name', { rules: [{ required: true , message: '请输入资源账户' }] }]"></a-input>
                </a-form-item>

                <template v-if="loginType=='auto'">
                    <a-form-item label="密码">
                        <a-input-password placeholder="请输入密码" v-decorator="['login_password', { rules: [{ required: true, message: '请输入密码' }] }]"></a-input-password>
                    </a-form-item>
                </template>

                <a-form-item label="描述">
                    <a-textarea placeholder="请输入，最多输入200个汉字或字符" v-decorator="['description', { rules: [{ required: false},{max:200,message:'最多输入200个汉字或字符'}] }]"></a-textarea>
                </a-form-item>

                <a-form-item label="关联资源">
                    <a-radio-group v-model="resources_type" @change="resourcesTypeChange" button-style="solid">
                        <a-radio-button value="host">
                            主机资源
                        </a-radio-button>
                        <!-- <a-radio-button value="app">
                            应用资源
                        </a-radio-button> -->
                    </a-radio-group>
                </a-form-item>
                <a-transfer :operations="operations" :titles="titles" :list-style="listStyle" style="margin:0 0 0 8.33%" @change="handleChange" :dataSource="mockData" :targetKeys="targetKeys" show-search :render="item => item.title" />
            </a-form>
            <footer>
                <a-button @click="onClose">取消</a-button>
                <a-button :loading="btnLoading" @click="onSubmit" style="margin:0 0px 0 8px" type="primary">保存</a-button>
            </footer>
        </a-drawer>
    </div>
</template>

<script>
import { addCredential, editCredential } from "@/api/credential"
import { getHost } from "@/api/host"
export default {
    data() {
        return {
            title: "",
            visible: false,
            passwordForm: this.$form.createForm(this, { name: "passwordForm" }),
            // 整体数据
            mockData: [],
            // 右侧数据的key值
            targetKeys: [],
            // 新增or修改
            isEdit: false,
            // 确认按钮loading
            btnLoading: false,
            loginType: "auto",
            resources_type: "host",
            //全部主机资源选项(穿梭框) 
            allhostList: [],
            // 展示的主机资源选项(编辑时已经绑定过的主机资源不显示)
            hostList: [],
            //被选中的主机(切换资源类型时进行记录) 
            selectedhostList: [],
            //全部应用资源选项(穿梭框) 
            allappList: [],
            // 展示的应用资源选项(编辑时已经绑定过的应用资源不显示)
            appList: [],
            //被选中的应用资源(切换资源类型时进行记录) 
            selectedappList: [],

            listStyle: {
                width: '360px',
                height: '420px',
            },
            titles: ['可选中的主机资源', '已选择的主机资源'],
            operations: ['加入右侧', '加入左侧'],
        }
    },
    mounted() {
        // this.getAllHost()
    },
    methods: {

        // 资源类型切换
        resourcesTypeChange() {

        },
        // 获取所有资源
        getAllHost() {
            getHost({ all_data: 1 }).then(res => {
                if (res.code == 200 && res.data) {
                    let arr = []
                    res.data.map(item => {
                        arr.push({
                            key: item.id + "",
                            title: item.host_name
                        })
                    })
                    this.allhostList = arr
                    this.hostList = this.allhostList
                    this.mockData = this.hostList
                }
            })
        },
        // 切换登录方式
        loginTypeChange(val) {
            this.loginType = val.target.value
        },
        // 抽屉显示
        show(record) {
            this.visible = true
            this.getAllHost()
            if (record) {
                this.activePassword = record
                this.isEdit = true
                this.title = "编辑密码凭证"
                this.loginType = record.login_type

                let arr1 = []
                record.host_list.map(item => {
                    arr1.push(item.id + "")
                })
                this.selectedhostList = arr1
                this.targetKeys = this.selectedhostList
                this.$nextTick(function () {
                    this.passwordForm.setFieldsValue({
                        name: record.name,
                        login_type: record.login_type,
                        login_name: record.login_name,
                        login_password: "******",
                        description: record.description,
                    })
                })
            } else {
                this.isEdit = false
                this.title = "新建密码凭证"
                this.loginType = "auto"

            }
        },
        // 抽屉关闭
        onClose() {
            this.visible = false
            this.passwordForm.resetFields()
            this.$emit("father")
            this.targetKeys = []
            this.selectedhostList = []
            this.selectedappList = []
        },
        // 穿梭框
        handleChange(nextTargetKeys, direction, moveKeys) {
            this.targetKeys = nextTargetKeys;
        },
        // 提交
        onSubmit() {
            this.passwordForm.validateFields((err, values) => {
                if (!err) {
                    this.btnLoading = true
                    let updata = values
                    updata.credential_type = "password"
                    if (this.resources_type == "host") {
                        this.selectedhostList = this.targetKeys
                    } else {
                        this.selectedappList = this.targetKeys
                    }
                    updata.host_list = this.selectedhostList
                    if (this.isEdit) {
                        updata.id = this.activePassword.id
                        editCredential(updata).then(res => {
                            if (res.code == 200) {
                                this.$message.success(res.message)
                                this.onClose()
                            }
                        }).finally(() => {
                            this.btnLoading = false
                        })
                    } else {
                        addCredential(updata).then(res => {
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