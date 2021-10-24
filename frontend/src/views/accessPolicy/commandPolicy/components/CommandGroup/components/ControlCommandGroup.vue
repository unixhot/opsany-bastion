<template>
    <div>
        <a-modal
            :title="formData.id ? '编辑命令组' : '新建命令组'"
            v-model="visible"
            @ok="handleOk"
            @cancel="handleCancel"
            :confirmLoading="loading"
            width="920px"
        >
            <a-form-model
                ref="formData"
                :model="formData"
                :rules="formDataRules"
                :labelCol="{ span: 3 }"
                :wrapperCol="{ span: 21 }"
            >
                <a-form-model-item label="命令组名称" prop="name">
                    <a-input placeholder="请输入命令组名称" v-model="formData.name"></a-input>
                </a-form-model-item>
                <a-form-model-item label="描述">
                    <a-input
                        type="textarea"
                        placeholder="请输入描述"
                        v-model="formData.description"
                        :autoSize="{ minRows: 3, maxRows: 6 }"
                    ></a-input>
                </a-form-model-item>
                <a-form-model-item label="命令">
                    <Command
                        :listStyle="{ width: '300px', height: '400px' }"
                        :command_list="formData.command_list"
                        ref="Command"
                    ></Command>
                </a-form-model-item>
            </a-form-model>
        </a-modal>
    </div>
</template>
<script>
import Command from '../../PolicyList/components/components/Step2/components/Command.vue'
import * as API from '@/api/command-group'
export default {
    components: { Command },
    data() {
        return {
            visible: false,
            loading: false,
            formData: {
                id: undefined,
                name: undefined,
                description: undefined,
                command_list: [],
            },
            formDataRules: {
                name: [{ required: true, message: '请填写命令名称', trigger: 'change' }],
            },
        }
    },
    methods: {
        showModal(row = {}) {
            this.formData = this.$options.data().formData
            this.$refs.Command?.resetData()
            this.$nextTick(() => {
                this.$refs.formData?.clearValidate()
            })
            if (Object.keys(row).length) {
                for (let key in this.formData) {
                    if (key in row) {
                        this.formData[key] = row[key]
                    }
                }
                const group = row.command || []
                this.formData.command_list = group.map((item) => item.id + '')
            }
            this.visible = true
        },
        handleOk() {
            // { addCommandGroup, editCommandGroup }
            const apiKey = this.formData.id ? 'editCommandGroup' : 'addCommandGroup'
            this.formData.command_list = this.$refs.Command.getFormData()
            this.loading = true
            API[apiKey](this.formData)
                .then((res) => {
                    this.$message.success(res.message)
                    this.visible = false
                    this.$emit('done')
                })
                .finally(() => {
                    this.loading = false
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
</style>