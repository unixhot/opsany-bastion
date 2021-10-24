<template>
    <div>
        <a-form-model
            ref="formData"
            layout="horizontal"
            :model="formData"
            :rules="formDataRules"
            :label-col="labelCol"
            :wrapper-col="wrapperCol"
        >
            <a-form-model-item label="策略名称" prop="name">
                <a-input placeholder="请输入策略名称" :disabled="!!formData.id" v-model="formData.name"></a-input>
            </a-form-model-item>
            <a-form-model-item label="有效期">
                <a-date-picker
                    v-model="start_time"
                    allowClear
                    showTime
                    placeholder="请选择生效时间"
                    @change="(time, timeStr) => changeTime(time, timeStr, 'start_time')"
                ></a-date-picker>
                <a-date-picker
                    v-model="end_time"
                    allowClear
                    showTime
                    placeholder="请选择失效时间"
                    @change="(time, timeStr) => changeTime(time, timeStr, 'end_time')"
                    style="margin-left: 20px"
                ></a-date-picker>
            </a-form-model-item>
            <a-form-model-item label="时段限制" class="time_item">
                <SelectTime v-model="formData.login_time_limit" ref="SelectTime" allowText="允许使用命令" disabledText="禁止使用命令"></SelectTime>
            </a-form-model-item>
        </a-form-model>
    </div>
</template>
<script>
import SelectTime from '@/components/SelectTime'
export default {
    components: { SelectTime },
    props: {
        strategy: {
            type: Object,
            default: () => {
                return {}
            },
        },
    },
    watch: {
        strategy: {
            handler(val) {
                for (let key in this.formData) {
                    if (key in val) this.formData[key] = val[key]
                }
                this.start_time = val.start_time || null
                this.end_time = val.end_time || null
            },
        },
    },
    data() {
        return {
            formData: {
                id: undefined,
                name: undefined,
                start_time: undefined,
                end_time: undefined,
                login_time_limit: [],
            },
            formDataRules: {
                name: [{ required: true, message: '请填写策略名称', trigger: 'change' }],
            },
            labelCol: {
                span: 3,
            },
            wrapperCol: {
                span: 20,
            },
            start_time: null,
            end_time: null,
        }
    },
    methods: {
        changeTime(time, timeStr, prop) {
            this.formData[prop] = timeStr
        },
        resetFormData() {
            this.formData = this.$options.data().formData
            this.$nextTick(() => {
                this.$refs.formData?.clearValidate()
            })
            const weekList = Array.from({ length: 7 }, (item, index) => {
                return { week: index + 1, time: [] }
            })
            this.formData.login_time_limit = weekList
            this.start_time = null
            this.end_time = null
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
.time_item {
    /deep/ .ant-form-item-control {
        line-height: normal !important;
        margin-top: 10px;
    }
}
</style>