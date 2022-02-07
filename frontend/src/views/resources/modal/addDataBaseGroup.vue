<template>
    <a-modal :confirmLoading="btnLoading" @ok="onGroupSubmit" v-model="visiable" :title="title">
        <a-form :form="groupForm">
            <a-form-item label="分组名称">
                <a-input v-decorator="['name', { rules: [{ required: true, message: '请填写分组名称' }] }]"></a-input>
            </a-form-item>
        </a-form>
    </a-modal>
</template>

<script>
import { addDataBaseGroup, editDataBaseGroup } from "@/api/dataBase"
export default {
    data() {
        return {
            visiable: false,
            groupForm: this.$form.createForm(this, { name: "groupForm" }),
            title: "",
            // 确认按钮loading
            btnLoading: false,
        }
    },
    methods: {
        show(row, type) {
            this.groupForm.resetFields()
            this.visiable = true
            this.type = type
            this.activeGroup = row
            if (type == "edit") {
                this.title = "编辑分组"
                this.$nextTick(function () {
                    this.groupForm.setFieldsValue({
                        name: row.title,
                    })
                })

            } else {
                this.title = "添加分组"
            }
        },
        // 新建分组
        onGroupSubmit() {
            this.groupForm.validateFields((err, values) => {
                this.btnLoading = true
                if (!err) {
                    let updata = values
                    if (this.type == "add") {
                        if (this.activeGroup.key != "all") {
                            updata.parent = this.activeGroup.key
                        } else {
                            updata.parent = null
                        }
                        addDataBaseGroup(updata).then(res => {
                            if (res.code == 200) {
                                this.$message.success(res.message)
                                this.$emit("father")
                                this.visiable = false
                            }
                        }).finally(() => {
                            this.btnLoading = false
                        })
                    } else {
                        updata.id = this.activeGroup.id
                        editDataBaseGroup(updata).then(res => {
                            if (res.code == 200) {
                                this.$message.success(res.message)
                                this.$emit("father")
                                this.visiable = false
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
</style>