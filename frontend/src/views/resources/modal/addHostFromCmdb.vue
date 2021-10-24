<template>
    <div>
        <a-modal width="1000px" :visible="visible" title="配置" @cancel="onClose" @ok="onSubmit" :confirmLoading="btnLoading">
            <a-form :form="hostForm" :label-col="{ span: 2 }" :wrapper-col="{ span: 22 }">
                <a-form-item label="主机名称">
                    <a-input placeholder="请输入主机名称" v-decorator="['host_name', { rules: [{ required: true, message: '请输入主机名称' }] }]"></a-input>
                </a-form-item>

                <a-form-item label="系统类型">
                    <a-select @change="systemChange" placeholder="请选择系统类型" v-decorator="['system_type', { rules: [{ required: true, message: '请选择系统类型' }] }]">
                        <a-select-option value="Windows">Windows</a-select-option>
                        <a-select-option value="Linux">Linux</a-select-option>
                    </a-select>
                </a-form-item>

                <a-form-item label="协议类型">
                    <a-select placeholder="请选择协议类型" v-decorator="['protocol_type', { rules: [{ required: true, message: '请选择协议类型' }] }]">
                        <a-select-option value="SSH">SSH</a-select-option>
                        <a-select-option value="RDP">RDP</a-select-option>
                        <!-- <a-select-option value="Telnet">Telnet</a-select-option>
                        <a-select-option value="VNC">VNC</a-select-option> -->
                    </a-select>
                </a-form-item>

                <a-form-item label="主机地址">
                    <a-input v-show="selectedHost.ip1 == '' || selectedHost.ip1 == null || selectedHost.ip2 == '' || selectedHost.ip2 ==null" :disabled="((selectedHost.ip1!=null && selectedHost.ip1!='') && (selectedHost.ip2==null || selectedHost.ip2==''))|| ((selectedHost.ip2!=null && selectedHost.ip2!='') && (selectedHost.ip1==null || selectedHost.ip1==''))" placeholder="输入IP地址" v-decorator="['host_address', { rules: [{ required: true, message: '请输入IP地址' }] }]" />
                    <a-select v-show="selectedHost.ip1 && selectedHost.ip1 != '' && selectedHost.ip2 && selectedHost.ip2 != ''" placeholder="请选择IP地址" v-decorator="['host_address', { rules: [{ required: true, message: '请选择IP地址' }] }]">
                        <a-select-option v-for="item in ipList" :key="item.value" :value="item.value">{{
                                    item.label + ' ' + item.value
                                }}</a-select-option>
                    </a-select>
                </a-form-item>

                <a-form-item label="端口">
                    <a-input-number style="width:872px;" :min="1" :max="65535" placeholder="请输入1~65535之间的有效数字" v-decorator="['port', { rules: [{ required: true, message: '请输入1~65535之间的有效数字' }] }]"></a-input-number>
                </a-form-item>

                <a-form-item label="所属分组">
                    <a-tree-select :tree-data="fatherData" placeholder="请选择分组" v-decorator="['group', { rules: [{ required: true, message: '请选择所属分组' }] }]"></a-tree-select>
                </a-form-item>

                <a-form-item label="主机描述">
                    <a-textarea placeholder="请输入，最多输入200个汉字或字符" v-decorator="['description', { rules: [{ required: false},{max:200,message:'最多输入200个汉字或字符'}] }]"></a-textarea>
                </a-form-item>

                <a-form-item label="添加凭证">
                    <a-radio-group v-model="addMethodType" button-style="solid">
                        <a-radio-button value="immediately">
                            立即添加
                        </a-radio-button>
                        <a-radio-button value="future">
                            以后添加
                        </a-radio-button>
                        <a-radio-button value="have">
                            选择已有
                        </a-radio-button>
                    </a-radio-group>
                </a-form-item>
            </a-form>

            <a-form v-if="addMethodType=='immediately'" :form="voucherForm" :label-col="{ span: 2 }" :wrapper-col="{ span: 22 }">
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

                <a-form-item label="验证方式">
                    <a-select v-model="verificationMethod">
                        <a-select-option value="password">密码凭证</a-select-option>
                        <a-select-option value="ssh_key">SSH密钥</a-select-option>
                    </a-select>
                </a-form-item>

                <a-form-item label="凭证名称">
                    <a-input placeholder="请输入凭证名称" v-decorator="['name', { rules: [{ required: true, message: '请输入凭证名称' }] }]"></a-input>
                </a-form-item>

                <a-form-item label="资源账户">
                    <a-input placeholder="请输入资源账户的名称" v-decorator="['login_name', { rules: [{ required:true, message: '请输入资源账户' }] }]"></a-input>
                </a-form-item>
                <div v-if="verificationMethod=='password'">
                    <template v-if="loginType=='auto'">
                        <a-form-item label="密码">
                            <a-input-password placeholder="请输入密码" v-decorator="['login_password', { rules: [{ required: true, message: '请输入密码' }] }]"></a-input-password>
                        </a-form-item>
                    </template>
                </div>
                <div v-else>
                    <a-form-item label="SSH key">
                        <a-textarea placeholder="请输入SSH key" :rows="4" v-decorator="['ssh_key', { rules: [{ required:true, message: '请输入SSH key' }] }]"></a-textarea>
                    </a-form-item>
                    <template v-if="loginType=='auto'">
                        <a-form-item label="Passphrase">
                            <a-input-password placeholder="请输入Passphrase" v-decorator="['passphrase', { rules: [{ required: false, message: '请输入Passphrase' }] }]"></a-input-password>
                        </a-form-item>
                    </template>
                </div>
                <a-form-item label="描述">
                    <a-textarea placeholder="请输入，最多输入200个汉字或字符" v-decorator="['description', { rules: [{ required: false},{max:200,message:'最多输入200个汉字或字符'}] }]"></a-textarea>
                </a-form-item>
            </a-form>

            <a-form v-if="addMethodType=='have'" :form="voucherForm" :label-col="{ span: 2 }" :wrapper-col="{ span: 22 }">
                <a-form-item label="添加凭证">
                    <a-radio-group v-model="credential_type">
                        <a-radio value="password">
                            密码凭证
                        </a-radio>
                        <a-radio value="ssh">
                            SSH密钥
                        </a-radio>
                        <a-radio value="group">
                            凭证分组
                        </a-radio>
                    </a-radio-group>
                </a-form-item>
                <a-transfer :operations="operations" :titles="titles" :list-style="listStyle" style="margin:0 0 0 8.33%" @change="handleChange" :dataSource="mockData" :targetKeys="targetKeys" show-search :render="item => item.title" />
            </a-form>
        </a-modal>
    </div>
</template>

<script>
import { addHost, editHost } from "@/api/host"
import { getGroup } from "@/api/group"
import { getCredential } from "@/api/credential"
export default {
    data() {
        return {
            visible: false,
            btnLoading: false,
            hostForm: this.$form.createForm(this, { name: "hostForm" }),
            // 添加方式
            addMethodType: "immediately",

            voucherForm: this.$form.createForm(this, { name: "voucherForm" }),
            loginType: "auto",
            // 验证方式(password或ssh 立即添加时有效)
            verificationMethod: "password",
            listStyle: {
                width: '360px',
                height: '420px',
            },
            titles: [],
            titles1: ['可添加的密码凭据', '已选择的密码凭据'],
            titles2: ['可添加的SSH密钥', '已选择的SSH密钥'],
            titles3: ['可添加的凭据分组', '已选择的凭据分组'],
            operations: ['加入右侧', '加入左侧'],
            // 整体数据
            mockData: [],
            // 右侧数据的key值
            targetKeys: [],
            credential_type: "password",

            //全部密码凭证选项(穿梭框) 
            allpasswordList: [],
            // 展示的密码凭证选项(编辑主机时已经绑定过的凭证不显示)
            passwordList: [],
            //被选中的密码凭证(切换凭证类型时进行记录) 
            selectedpasswordList: [],
            //全部ssh凭证选项(穿梭框) 
            allsshList: [],
            // 展示的SSH凭证选项(编辑主机时已经绑定过的凭证不显示)
            sshList: [],
            //被选中的密码凭证(切换凭证类型时进行记录) 
            selectedsshList: [],
            //全部凭证分组选项(穿梭框) 
            allgroupList: [],
            // 展示的凭证分组选项(编辑主机时已经绑定过的凭证分组不显示)
            groupList: [],
            //被选中的凭证分组(切换凭证类型时进行记录) 
            selectedgroupList: [],
            // 选中的添加主机
            selectedHost: {},
            ipList: [],
        }
    },
    props: ["fatherData"],
    watch: {
        // 凭证类型切换时，将选中的项记录，并更新数据
        credential_type: {
            handler(val, oldval) {
                if (oldval == "password") {
                    this.selectedpasswordList = this.targetKeys
                } else if (oldval == "ssh") {
                    this.selectedsshList = this.targetKeys
                } else if (oldval == "group") {
                    this.selectedgroupList = this.targetKeys
                }
                if (val == "password") {
                    this.titles = this.titles1
                    this.mockData = this.passwordList
                    this.targetKeys = this.selectedpasswordList
                } else if (val == "ssh") {
                    this.titles = this.titles2
                    this.mockData = this.sshList
                    this.targetKeys = this.selectedsshList
                } else if (val == "group") {
                    this.titles = this.titles3
                    this.mockData = this.groupList
                    this.targetKeys = this.selectedgroupList
                }
            }
        }
    },
    methods: {
        onClose() {
            this.visible = false
            this.hostForm.resetFields()
            this.targetKeys = []
            this.voucherForm.resetFields()
            this.selectedpasswordList = []
            this.selectedsshList = []
            this.selectedgroupList = []
        },
        // 选择系统自动填写协议类型和端口
        systemChange(val) {
            if (val == "Windows") {
                this.hostForm.setFieldsValue({
                    protocol_type: "RDP",
                    port: 3389
                })
            } else if (val == "Linux") {
                this.hostForm.setFieldsValue({
                    protocol_type: "SSH",
                    port: 22
                })
            }
        },
        // 穿梭框
        handleChange(nextTargetKeys, direction, moveKeys) {
            this.targetKeys = nextTargetKeys;
        },
        // 切换登录方式
        loginTypeChange(val) {
            this.loginType = val.target.value
        },
        // 获取所有凭据(password、ssh凭据分组)
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
            getGroup({ all_data: "1" }).then(res => {
                if (res.code == 200 && res.data) {
                    let arr = []
                    res.data.map(item => {
                        arr.push({
                            key: item.id + "",
                            title: item.name
                        })
                    })
                    this.allgroupList = arr
                    this.groupList = this.allgroupList
                }
            })
        },
        show(record) {
            this.selectedHost = record
            this.visible = true
            this.credential_type = "password"
            this.getAllCredential()
            this.titles = this.titles1

            this.loginType = "auto"
            this.addMethodType = "immediately"

            console.log(record)
            let system
            if (record.opt_os && record.opt_os.indexOf("Window") > -1) {
                system = "Windows"
                this.$nextTick(function () {
                    this.systemChange("Windows")
                })
            } else if (record.opt_os && record.opt_os.indexOf("window") == -1) {
                system = "Linux"
                this.$nextTick(function () {
                    this.systemChange("Linux")
                })
            } else {
                system = ""
            }
            this.$nextTick(function () {
                this.hostForm.setFieldsValue({
                    host_name: record.show_name,
                    system_type: system,
                    host_address: record.ip1 || record.ip2,
                })
            })
            if (record.ip1 && record.ip1 != '' && record.ip2 && record.ip2 != '') {
                this.ipList = [
                    { label: '公网IP', value: record.ip1 },
                    { label: '内网IP', value: record.ip2 },
                ]
            }

        },
        // 提交
        onSubmit() {
            let values1, values2
            let p1 = new Promise((resolve, reject) => {
                this.hostForm.validateFields((err, values) => {
                    if (!err) {
                        values1 = values
                        resolve()
                    }
                })
            })

            let p2 = new Promise((resolve, reject) => {
                this.voucherForm.validateFields((err, values) => {
                    if (!err) {
                        values2 = values
                        resolve()
                    }
                })
            })

            Promise.all([p1, p2]).then((result) => {
                this.btnLoading = true
                let updata = values1
                if (this.addMethodType == "immediately") {
                    updata.credential = values2
                    updata.credential.credential_type = this.verificationMethod
                } else if (this.addMethodType == "have") {
                    if (this.credential_type == "password") {
                        this.selectedpasswordList = this.targetKeys
                    } else if (this.credential_type == "ssh") {
                        this.selectedsshList = this.targetKeys
                    } else if (this.credential_type == "group") {
                        this.selectedgroupList = this.targetKeys
                    }
                    updata.credential_list = this.selectedpasswordList.concat(this.selectedsshList)
                    updata.credential_group_list = this.selectedgroupList
                }
                updata.resource_from = "cmdb"
                updata.host_name_code=this.selectedHost.name
                addHost(updata).then(res => {
                    if (res.code == 200) {
                        this.$message.success(res.message)
                        this.onClose()
                        this.$emit("father")
                    }
                }).finally(() => {
                    this.btnLoading = false
                })

            })
        },
    }
}
</script>
<style lang="less" scoped>
</style>