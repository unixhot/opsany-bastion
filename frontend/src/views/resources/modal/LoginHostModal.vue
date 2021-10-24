<template>
    <div>
        <a-modal
            v-model="visible"
            :closable="false"
            :bodyStyle="{ padding: 0 }"
            width="650px"
            :confirmLoading="loading"
            @ok="handleOk"
            @cancel="handleCancel"
        >
            <div class="header">
                <div class="header_left">
                    <div>
                        <img :src="require('@/assets/remote_host.png')" alt="" />
                    </div>
                </div>
                <div class="header_right">
                    <strong>{{ hostInfo.host_name }}</strong>
                    <div>主机地址：{{ hostInfo.host_address }}</div>
                    <div>协议类型：{{ hostInfo.protocol_type }}</div>
                    <div>端口：{{ hostInfo.port }}</div>
                </div>
            </div>
            <a-spin :spinning="infoLoading">
                <div class="content">
                    <a-form-model
                        ref="formData"
                        layout="horizontal"
                        :model="formData"
                        :rules="formDataRules"
                        :label-col="labelCol"
                        :wrapper-col="wrapperCol"
                    >
                        <a-form-model-item label="资源凭证" prop="credential_host_id">
                            <a-select
                                style="width: 100%"
                                placeholder="请选择资源凭证"
                                v-model="formData.credential_host_id"
                                @change="changeCredential"
                            >
                                <a-select-option v-for="item in credentialList" :key="item.id" :value="item.id">
                                    {{ item.login_name }}/{{ item.host_address }}({{ item.credential_name }})
                                </a-select-option>
                            </a-select>
                        </a-form-model-item>
                        <a-form-model-item label="密码" v-if="isHand">
                            <a-input-password v-model="formData.password" placeholder="请输入密码"></a-input-password>
                        </a-form-model-item>
                        <a-form-model-item label="字体大小" v-if="hostInfo.system_type == 'Linux'">
                            <a-input-number
                                style="width: 100%"
                                v-model="formData.font_size"
                                placeholder="请输入字体大小"
                                :min="14"
                                :max="20"
                                allowClear
                            ></a-input-number>
                        </a-form-model-item>
                        <a-form-model-item label="分辨率" v-if="hostInfo.system_type == 'Windows'">
                            <a-select
                                style="width: 100%"
                                placeholder="请选择分辨率"
                                v-model="formData.winSize"
                                @change="changeCredential"
                                allowClear
                            >
                                <a-select-option v-for="item in screenArr" :key="item.key" :value="item.key">
                                    {{ item.width }} * {{ item.height }}
                                </a-select-option>
                            </a-select>
                        </a-form-model-item>
                    </a-form-model>
                </div>
            </a-spin>
        </a-modal>
    </div>
</template>
<script>
import { getResourceCredential } from '@/api/resource-credential'
import { linkCheck } from '@/api/link-check'
import { stringifyUrl } from '@/utils/util'
import screenArr from '@/utils/screenArr'
import cloneDeep from 'lodash.clonedeep'

export default {
    data() {
        return {
            visible: false,
            infoLoading: false,
            loading: false,
            hostInfo: {},
            formData: {
                host_id: undefined,
                credential_host_id: undefined,
                password: undefined,
                width: undefined,
                height: undefined,
                font_size: 14,
                winSize: 8,
            },
            formDataRules: {
                credential_host_id: [{ required: true, message: '请选择资源凭证', trigger: 'change' }],
            },
            labelCol: {
                span: 4,
            },
            wrapperCol: {
                span: 20,
            },
            credentialList: [],
            isHand: false, //是否为手动登录
            screenArr, //分辨率列表
            localOpen: false, //是否为本地打开
        }
    },
    methods: {
        showModal(row, localOpen = false) {
            this.localOpen = localOpen
            this.hostInfo = cloneDeep(row)
            this.formData = this.$options.data().formData
            this.$nextTick(() => {
                this.$refs.formData?.clearValidate()
            })
            this.isHand = false
            this.getResourceCredential()
            this.visible = true
        },
        getResourceCredential() {
            this.infoLoading = true
            const params = { host_id: this.hostInfo.id, data_type: 'host' }
            getResourceCredential(params)
                .then((res) => {
                    this.credentialList = res.data
                    if (res.data.length > 0) {
                        this.formData.credential_host_id = res.data[0].id
                        const isHand = res.data[0].login_type == 'hand'
                        this.isHand = isHand
                    }
                })
                .finally(() => {
                    this.infoLoading = false
                })
        },
        changeCredential(val) {
            const activeItem = this.credentialList.find((item) => item.id == val) || {}
            const isHand = activeItem.login_type == 'hand'
            if (isHand != this.isHand) this.formData.password = undefined
            this.isHand = isHand
        },
        handleOk() {
            this.$refs.formData.validate((flag) => {
                if (flag) {
                    this.loading = true
                    this.formData.host_id = this.hostInfo.id
                    linkCheck(this.formData)
                        .then((res) => {
                            const otherAppUrl = window.API_ROOT.replace('/bastion/', '')
                            const isDev = process.env.NODE_ENV === 'development'
                            const routeName = this.hostInfo.system_type == 'Windows' ? 'webWindows' : 'remoteLinux'
                            const query = {
                                host_token: res.data,
                                fontSize: this.formData.font_size,
                            }
                            if (routeName == 'webWindows') {
                                delete query.fontSize
                                if (this.formData.winSize) {
                                    query.winSize = this.formData.winSize
                                }
                            }
                            if (this.localOpen) {
                                this.visible = false
                                return this.$emit('getHostToken', query,this.hostInfo)
                            }
                            const url = isDev
                                ? `${window.location.origin}/#/console/${routeName}${stringifyUrl(query)}`
                                : `${otherAppUrl}/bastion/#/console/${routeName}${stringifyUrl(query)}`
                            window.open(url)
                            this.visible = false
                        })
                        .finally(() => {
                            this.loading = false
                        })
                }
            })
        },
        handleCancel() {
            this.visible = false
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
.header {
    display: flex;
    align-items: center;
    border-bottom-left-radius: 20%;
    border-bottom-right-radius: 20%;
    border: 1px solid #eeeeee;
    box-shadow: 0 1px 8px rgba(0, 0, 0, 0.15);
    padding: 40px 30px;
    &_left {
        div {
            width: 120px;
            height: 120px;
            border: 0.5p solid #eeeeee;
            border-radius: 50%;
            background: #ffffff;
            line-height: 120px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }
    }
    &_right {
        margin-left: 30px;
        strong {
            display: inline-block;
            margin-bottom: 10px;
            font-size: 16px;
        }
        > div {
            padding: 3px 0;
        }
    }
}
.content {
    padding: 20px;
    margin-top: 20px;
}
</style>