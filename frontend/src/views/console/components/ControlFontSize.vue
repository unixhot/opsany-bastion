<template>
    <div>
        <a-modal title="设置字体大小" :visible="visible" :maskClosable="false" @ok="handleOk" @cancel="handleCancel">
            <a-form-model
                ref="formData"
                layout="horizontal"
                :model="formData"
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
            >
                <a-form-model-item label="字体大小">
                    <a-input-number
                        style="width: 100%"
                        v-model="formData.font_size"
                        placeholder="请输入字体大小"
                        :min="14"
                        :max="20"
                        allowClear
                    ></a-input-number>
                </a-form-model-item>
            </a-form-model>
        </a-modal>
    </div>
</template>
<script>
export default {
    data() {
        return {
            visible: false,
            formData: {
                font_size: 14,
            },
            formDataRules: {
                credential_id: [{ required: true, message: '请选择资源凭证', trigger: 'change' }],
            },
            labelCol: {
                span: 4,
            },
            wrapperCol: {
                span: 20,
            },
        }
    },
    methods: {
        show() {
            this.visible = true
        },
        handleOk() {
            this.formData.font_size && this.$emit('setFontSize', this.formData.font_size)
            this.handleCancel()
        },
        handleCancel() {
            this.visible = false
        },
    },
    mounted() {},
}
</script>
<style scoped>
</style>