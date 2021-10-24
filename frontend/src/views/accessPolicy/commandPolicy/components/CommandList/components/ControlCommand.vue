<template>
    <div>
        <a-modal
            :title="formData.id ? '编辑命令' : '新建命令'"
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
                <a-form-model-item label="命令名称" prop="command">
                    <a-input placeholder="请输入命令名称" v-model="formData.command"></a-input>
                </a-form-model-item>
                <a-form-model-item label="命令类型" prop="block_type">
                    <a-select v-model="formData.block_type" placeholder="请选择命令类型">
                        <a-select-option v-for="item in block_type_list" :key="item.key" :value="item.key">
                            {{ item.name }}
                        </a-select-option>
                    </a-select>
                </a-form-model-item>
                <a-form-model-item label="提示内容" prop="block_info">
                    <a-input
                        type="textarea"
                        placeholder="请输入提示内容"
                        v-model="formData.block_info"
                        :autoSize="{ minRows: 3, maxRows: 6 }"
                    ></a-input>
                </a-form-model-item>
                <a-form-model-item label="命令组">
                    <CommandGroup
                        :listStyle="{ width: '300px', height: '400px' }"
                        :command_group_list="formData.command_group_list"
                        ref="CommandGroup"
                    ></CommandGroup>
                </a-form-model-item>
            </a-form-model>
        </a-modal>
    </div>
</template>
<script>
import CommandGroup from '../../PolicyList/components/components/Step2/components/CommandGroup.vue'
import * as API from '@/api/command'
export default {
    components: { CommandGroup },
    data() {
        return {
            visible: false,
            loading: false,
            formData: {
                id: undefined,
                command: undefined,
                block_type: undefined,
                block_info: undefined,
                command_group_list: [],
            },
            formDataRules: {
                command: [{ required: true, message: '请填写命令名称', trigger: 'change' }],
                block_type: [{ required: true, message: '请选择命令类型', trigger: 'change' }],
                block_info: [{ required: true, message: '请填写提示内容', trigger: 'change' }],
            },
            block_type_list: [
                { key: '1', name: '命令阻断' },
                { key: '2', name: '命令提醒' },
            ],
        }
    },
    methods: {
        showModal(row = {}) {
            this.formData = this.$options.data().formData
            this.$refs.CommandGroup?.resetData()
            this.$nextTick(() => {
                this.$refs.formData?.clearValidate()
            })
            if (Object.keys(row).length) {
                for (let key in this.formData) {
                    if (key in row) {
                        this.formData[key] = row[key]
                    }
                }
                const group = row.command_group || []
                this.formData.command_group_list = group.map((item) => item.id + '')
            }
            this.visible = true
        },
        handleOk() {
            // { addCommand, editCommand }
            const apiKey = this.formData.id ? 'editCommand' : 'addCommand'
            this.formData.command_group_list = this.$refs.CommandGroup.getFormData()
            this.loading = true
            API[apiKey](this.formData)
                .then((res) => {
                    console.log(res.data)
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