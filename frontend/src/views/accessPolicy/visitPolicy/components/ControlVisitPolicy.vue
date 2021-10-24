<template>
    <div>
        <a-drawer
            :title="id ? '编辑访问策略' : '新建访问策略'"
            :width="920"
            :visible="visible"
            :body-style="{ paddingBottom: '80px' }"
            @close="handleCancel"
        >
            <a-spin :spinning="infoLoading">
                <div style="margin-bottom: 30px">
                    <a-steps :current="activeCurrent" style="width: 70%; margin: 0 auto" @change="changeActiceCurrent">
                        <a-step title="配置基本信息"> </a-step>
                        <a-step title="关联用户/用户组" />
                        <a-step title="关联资源凭证"> </a-step>
                    </a-steps>
                </div>

                <Step1 v-show="activeCurrent == 0" ref="Step1" :strategy="strategy"></Step1>
                <Step2 v-show="activeCurrent == 1" ref="Step2" :user="user"></Step2>
                <Step3 v-show="activeCurrent == 2" ref="Step3" :credential_host="credential_host"></Step3>
            </a-spin>

            <div class="bottom_btns">
                <a-button :style="{ marginRight: '8px' }" @click="handleCancel"> 取消 </a-button>
                <a-button
                    :style="{ marginRight: '8px' }"
                    @click="activeCurrent -= 1"
                    v-if="activeCurrent == 1 || activeCurrent == 2"
                >
                    上一步
                </a-button>
                <a-button type="primary" @click="nextStep" v-if="activeCurrent == 0 || activeCurrent == 1">
                    下一步
                </a-button>
                <a-button v-if="activeCurrent == 2" type="primary" @click="handleOk" :loading="loading">
                    确定
                </a-button>
            </div>
        </a-drawer>
    </div>
</template>
<script>
import cloneDeep from 'lodash.clonedeep'
import Step1 from './components/Step1'
import Step2 from './components/Step2'
import Step3 from './components/Step3'
import { getAccessStrategy, addAccessStrategy, editAccessStrategy } from '@/api/access-strategy'
export default {
    components: { Step1, Step2, Step3 },
    data() {
        return {
            visible: false,
            loading: false,
            infoLoading: false,
            activeCurrent: 0,
            id: undefined,
            strategy: {}, //step1
            user: {}, //step2
            credential_host: {}, //step3
        }
    },
    methods: {
        showModal(id) {
            this.id = id
            if (id) this.getAccessStrategy()
            const stepList = ['Step1', 'Step2', 'Step3']
            this.activeCurrent = this.$options.data().activeCurrent
            this.$nextTick(() => {
                setTimeout(() => {
                    stepList.forEach((item) => {
                        this.$refs[item]?.resetFormData()
                    })
                }, 0)
            })
            this.visible = true
        },
        getAccessStrategy() {
            this.infoLoading = true
            getAccessStrategy({ id: this.id })
                .then((res) => {
                    const { user, strategy, credential_host } = res.data
                    this.user = user
                    this.strategy = strategy
                    this.credential_host = credential_host
                })
                .finally(() => {
                    this.infoLoading = false
                })
        },
        nextStep() {
            if (this.activeCurrent == 0) {
                const Step1 = this.$refs.Step1
                Step1.$refs.formData.validate((flag) => {
                    if (flag) {
                        this.activeCurrent += 1
                    }
                })
            } else this.activeCurrent += 1
        },
        handleOk() {
            const strategy = cloneDeep(this.$refs.Step1.formData)
            const user = this.$refs.Step2.getFormData()
            const credential_host = this.$refs.Step3.getFormData()
            const params = { strategy, user, credential_host }
            this.loading = true
            const API = { addAccessStrategy, editAccessStrategy }
            const apiKey = strategy.id ? 'editAccessStrategy' : 'addAccessStrategy'
            API[apiKey](params)
                .then((res) => {
                    this.$message.success(res.message)
                    this.visible = false
                    this.$emit('done')
                })
                .finally(() => {
                    this.loading = false
                })
        },
        handleCancel(e) {
            this.visible = false
        },
        changeActiceCurrent(val) {
            this.activeCurrent = val
        },
    },
}
</script>
<style lang="less" scoped>
.bottom_btns {
    position: absolute;
    right: 0;
    bottom: 0;
    width: 100%;
    border-top: 1px solid #e9e9e9;
    padding: 10px 16px;
    background: #fff;
    text-align: right;
    z-index: 1;
}
</style>

