<template>
    <div>
        <a-drawer
            :title="formData.id ? '编辑用户组' : '新建用户组'"
            :width="1220"
            :visible="visible"
            :body-style="{ paddingBottom: '80px' }"
            @close="handleCancel"
        >
            <a-form-model
                ref="formData"
                layout="horizontal"
                :model="formData"
                :rules="formDataRules"
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
            >
                <a-form-model-item label="用户组名称" prop="name">
                    <a-input placeholder="请输入用户组名称" v-model="formData.name"></a-input>
                </a-form-model-item>
                <a-form-model-item label="描述" prop="description">
                    <a-input
                        placeholder="请输入描述"
                        type="textarea"
                        :autoSize="{ minRows: 3, maxRows: 6 }"
                        v-model="formData.description"
                    ></a-input>
                </a-form-model-item>
                <a-form-model-item label="添加组员" prop="username_list">
                    <a-select v-model="formData.username_list" hidden></a-select>
                    <a-button @click="$refs.ImportUser.showModal()" style="margin-bottom:10px">选择添加</a-button>
                    <a-table
                        :dataSource="tableData"
                        :columns="columns"
                        :pagination="{
                            ...tableQuery,
                            showSizeChanger: true,
                            showTotal: (total) => `共 ${total} 条数据`,
                            showQuickJumper: true,
                        }"
                        @change="tableChange"
                        :rowKey="(item) => item.id"
                    >
                        <template slot="action" slot-scope="text, row, index">
                            <a-button type="link" size="small" @click="delUser(index)">移除</a-button>
                        </template>
                    </a-table>
                </a-form-model-item>
            </a-form-model>

            <div class="bottom_btns">
                <a-button :style="{ marginRight: '8px' }" @click="handleCancel"> 取消 </a-button>
                <a-button type="primary" @click="handleOk" :loading="loading"> 确定 </a-button>
            </div>
            <ImportUser ref="ImportUser" @done="setTableData"></ImportUser>
        </a-drawer>
    </div>
</template>
<script>
import * as API from '@/api/user-group-admin'
import ImportUser from './importUser.vue'
export default {
    components: { ImportUser },
    data() {
        return {
            visible: false,
            loading: false,
            tableQuery: {
                current: 1,
                pageSize: 10,
                total: 0,
            },
            formData: {
                id: undefined,
                name: undefined,
                username_list: [],
                description: undefined,
            },
            formDataRules: {
                name: [{ required: true, message: '请填写用户组名称', trigger: 'change' }],
                username_list: [{ required: true, message: '请选择组员添加', type: 'array', trigger: 'change' }],
            },
            labelCol: {
                span: 3,
            },
            wrapperCol: {
                span: 20,
            },
            columns: [
                { title: '用户名', dataIndex: 'username', ellipsis: true },
                {
                    title: '姓名',
                    dataIndex: 'ch_name',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
                },
                {
                    title: '联系方式',
                    dataIndex: 'phone',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
                },
                {
                    title: '邮箱',
                    dataIndex: 'email',
                    ellipsis: true,
                    customRender: (text) => {
                        return text || '--'
                    },
                },
                {
                    title: '操作',
                    dataIndex: 'action',
                    ellipsis: true,
                    scopedSlots: { customRender: 'action' },
                    align: 'center',
                },
            ],
            tableData: [],
        }
    },
    methods: {
        showModal(row) {
            this.formData = this.$options.data().formData
            this.$nextTick(() => {
                this.$refs.formData?.clearValidate()
            })
            this.tableData = []
            this.tableQuery = this.$options.data().tableQuery
            if (row) {
                for (let key in this.formData) {
                    if (key in row) this.formData[key] = row[key]
                }
                this.formData.username_list = row.user_list.map((item) => item.username)
                this.tableData = row.user_list
            }
            this.visible = true
        },
        tableChange({ current, pageSize }) {
            this.tableQuery.current = current
            this.tableQuery.pageSize = pageSize
        },
        handleCancel(e) {
            this.visible = false
        },
        setTableData(tableData) {
            this.tableData = tableData
            this.formData.username_list = tableData.map((item) => item.username)
            this.$refs.formData.validateField('username_list')
        },
        delUser(index) {
            console.log(index)
            this.tableData.splice(index, 1)
            this.formData.username_list = this.tableData.map((item) => item.username)
            this.$refs.formData.validateField('username_list')
        },
        handleOk() {
            this.$refs.formData.validate((flag) => {
                if (flag) {
                    this.loading = true
                    const apiKey = this.formData.id ? 'editUserGroupAdmin' : 'addUserGroupAdmin'
                    API[apiKey](this.formData)
                        .then((res) => {
                            this.$emit('done')
                            this.$message.success(res.message)
                            this.visible = false
                        })
                        .finally(() => {
                            this.loading = false
                        })
                }
            })
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
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