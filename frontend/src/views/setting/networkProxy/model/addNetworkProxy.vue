<template>
    <a-drawer :bodyStyle="{paddingBottom:'80px'}" width="800px" :visible="visible" @close="onClose">
        <h3 slot="title" class="drawer_title">
            <span>{{title}}</span>
            <a-alert style="margin:0 0 0 20px;font-weight:500" closable message="Linux和Windows至少创建一项，否则数据创建不成功" type="warning" show-icon />
        </h3>
        <a-form-model ref="ruleForm" :model="formData" :rules="rules" :label-col="{span:3}" :wrapper-col="{span:21}">

            <div>
                <h3>创建名称 <span style="color:red">*</span></h3>
                <a-form-model-item label="名称" prop="name">
                    <a-input v-model="formData.name" placeholder="请输入名称"></a-input>
                </a-form-model-item>
            </div>

            <div>
                <h3>Linux</h3>
                <a-form-model-item label="IP地址" prop="linux_ip">
                    <a-input v-model="formData.linux_ip" placeholder="请输入IP地址"></a-input>
                </a-form-model-item>
                <a-form-model-item label="端口" prop="linux_port">
                    <a-input-number :min="1" :max="65535" v-model="formData.linux_port" style="width:100%;" placeholder="请输入端口范围1-65535"></a-input-number>
                </a-form-model-item>
                <a-form-model-item label="用户名" prop="linux_login_name">
                    <a-input v-model="formData.linux_login_name" placeholder="请输入用户名"></a-input>
                </a-form-model-item>
                <a-form-model-item label="密码" prop="linux_login_password">
                    <a-input-password v-model="formData.linux_login_password" placeholder="请输入密码"></a-input-password>
                </a-form-model-item>
            </div>

            <div>
                <h3>Windows</h3>
                <a-form-model-item label="IP地址" prop="windows_ip">
                    <a-input v-model="formData.windows_ip" placeholder="请输入IP地址"></a-input>
                </a-form-model-item>
                <a-form-model-item label="端口">
                    <a-input-number :min="1" :max="65535" v-model="formData.windows_port" style="width:100%;" placeholder="请输入端口范围1-65535"></a-input-number>
                </a-form-model-item>
            </div>

            <div>
                <h3>网络代理描述</h3>
                <a-form-model-item label="描述" prop="description">
                    <a-textarea v-model="formData.description" placeholder="请输入网络代理描述，字数在200字以内"></a-textarea>
                </a-form-model-item>
            </div>

        </a-form-model>
        <footer>
            <a-button :loading="btnLoading" @click="onSubmit" style="float:right;margin:0 20px 0 10px" type="primary">确定</a-button>
            <a-button @click="onClose" style="float:right;">取消</a-button>
        </footer>
    </a-drawer>
</template>

<script>
import { addNetworkProxy, editNetworkProxy } from "@/api/networkProxy"

export default {
    data() {
        return {
            visible: false,
            title: "新建网络代理",
            formData: {},
            rules: {
                name: [{ required: true, message: "请填写名称", whitespace: true },],
                linux_ip: [{ pattern: /^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$/, message: "请输入有效的IP地址" }],
                windows_ip: [{ pattern: /^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$/, message: "请输入有效的IP地址" }],
                description: [{ max: 200, message: "描述字数在200字以内" }],
                linux_login_name: [{ pattern: /^[^\u4e00-\u9fa5]*$/, message: '用户名不能含有中文' }],
                linux_login_password: [{ pattern: /^[^\u4e00-\u9fa5]*$/, message: '密码不能含有中文' }],
            },
            btnLoading: false,
            activeNetworkProxy: {}
        }
    },
    methods: {
        show(record) {
            this.visible = true
            if (record) {
                this.title = "编辑网络代理"
                this.isEdit = true
                this.activeNetworkProxy = record
                this.formData = {
                    name: record.name,
                    linux_ip: record.linux_ip,
                    linux_port: record.linux_port,
                    linux_login_name: record.linux_login_name,
                    linux_login_password: record.linux_login_name ? "******" : "",
                    windows_ip: record.windows_ip,
                    windows_port: record.windows_port,
                    description: record.description,
                }
            } else {
                this.title = "新建网络代理"
                this.isEdit = false
            }
        },
        onClose() {
            this.visible = false
            this.formData = {}
            this.activeNetworkProxy = {}
            this.$emit("father")
        },
        onSubmit() {
            this.$refs.ruleForm.validate(valid => {
                if (valid) {
                    this.btnLoading = true
                    if (this.isEdit) {
                        editNetworkProxy({ ...this.formData, id: this.activeNetworkProxy.id }).then(res => {
                            if (res.code == 200) {
                                this.$message.success(res.message)
                                this.onClose()
                            }
                        }).finally(() => {
                            this.btnLoading = false
                        })
                    } else {
                        addNetworkProxy(this.formData).then(res => {
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
.ant-timeline-item {
}
h3 {
    font-weight: 1000;
    font-size: 14px;
}
footer {
    position: absolute;
    bottom: 0px;
    z-index: 3;
    background: #fff;
    width: 100%;
    left: 0;
    padding: 15px;
    border-top: 1px solid #e8e8e8;
}
.drawer_title {
    display: flex;
    align-items: center;
    margin: 0;
    font-size: 1.17em;
}
/deep/.ant-alert {
    padding: 1px 30px 2px 37px;
}
/deep/.ant-alert-icon {
    top: 5.5px;
}
/deep/.ant-alert-close-icon {
    top: 1px;
}
</style>