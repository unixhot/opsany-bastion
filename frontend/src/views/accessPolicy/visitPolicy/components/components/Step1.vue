<template>
    <div>
        <a-form-model
            style="padding:10px 0 0 0"
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
            <a-form-model-item>
                <span slot="label">
                    <span>有效期</span>
                    <a-tooltip title="指选择策略生效时间和策略的失效时间">
                        <a-icon style="margin:0 0 0 3px;color:#666" type="exclamation-circle" />
                    </a-tooltip>
                </span>
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
            <a-form-model-item label="文件传输">
                <a-checkbox v-model="formData.file_upload"> 上传 </a-checkbox>
                <a-checkbox style="margin-left: 20px" v-model="formData.file_download"> 下载 </a-checkbox>
            </a-form-model-item>
            <a-form-model-item label="更多选项">
                <a-checkbox v-model="formData.file_manager"> 文件管理 </a-checkbox>
                <a-checkbox style="margin-left: 20px" v-model="formData.copy_tool"> 剪贴板 </a-checkbox>
            </a-form-model-item>
            <a-form-model-item class="time_item">
                <span slot="label">
                    <span>登录时段限制</span>
                    <a-tooltip title="指在策略有效期内选择登录资源的时间段权限">
                        <a-icon style="margin:0 0 0 3px;color:#666" type="exclamation-circle" />
                    </a-tooltip>
                </span>
                <SelectTime v-model="formData.login_time_limit" ref="SelectTime"></SelectTime>
            </a-form-model-item>
            <a-form-model-item label="IP限制类型">
                <a-select
                    style="width: 100%"
                    placeholder="请选择限制类型"
                    v-model="formData.ip_limit"
                    @change="formData.limit_list = []"
                >
                    <a-select-option value="1">无</a-select-option>
                    <a-select-option value="2">黑名单</a-select-option>
                    <a-select-option value="3">白名单</a-select-option>
                </a-select>
            </a-form-model-item>
            <a-form-model-item
                :label="formData.ip_limit == 2 ? '黑名单' : '白名单'"
                v-if="formData.ip_limit != 1"
                prop="limit_list"
            >
                <a-select
                    mode="tags"
                    style="width: 100%"
                    :token-separators="[',']"
                    placeholder="请输入IP后按回车键录入"
                    v-model="formData.limit_list"
                >
                </a-select>
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
                this.formData.ip_limit = val.ip_limit + ''
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
                file_upload: true,
                file_download: true,
                file_manager: true,
                copy_tool: true,
                login_time_limit: [],
                ip_blacklist: [], //ip白名单
                ip_whitelist: [], //ip黑名单
                ip_limit: '1',
                limit_list: [],
            },
            formDataRules: {
                name: [{ required: true, message: '请填写策略名称', trigger: 'change' }],
                limit_list: [{ required: true, type: 'array', message: '请填写IP', trigger: 'change' }],
            },
            labelCol: {
                span: 4,
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
                return { week: index + 1, time: Array.from({ length: 24 }, (item, index) => index) }
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