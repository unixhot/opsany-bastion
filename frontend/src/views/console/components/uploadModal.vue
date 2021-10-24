<template>
    <div>
        <a-modal
            title="请选择上传文件"
            :visible="visible"
            :maskClosable="false"
            :confirm-loading="confirmLoading"
            @ok="handleOk"
            @cancel="handleCancel"
        >
            <a-upload-dragger
                :multiple="true"
                name="file"
                :remove="handleRemove"
                :file-list="fileList"
                :before-upload="beforeUpload"
            >
                <p class="ant-upload-drag-icon">
                    <a-icon type="inbox" />
                </p>
                <p class="ant-upload-text">单击或将文件拖到该区域以上传.</p>
                <p class="ant-upload-hint">支持单个或批量上传。</p>
            </a-upload-dragger>
        </a-modal>
    </div>
</template>
<script>
export default {
    data() {
        return {
            visible: false,
            confirmLoading: false,
            fileList: [],
            zsession: null,
        }
    },
    methods: {
        show(zsession) {
            this.visible = true
            this.zsession = zsession
            this.fileList = []
        },
        handleOk() {
            this.$emit('done', this.zsession, this.fileList)
            this.close()
        },
        close() {
            this.visible = false
        },
        handleRemove(file) {
            const index = this.fileList.indexOf(file)
            const newFileList = this.fileList.slice()
            newFileList.splice(index, 1)
            this.fileList = newFileList
        },
        handleCancel() {
            try {
                // zsession 每 5s 发送一个 ZACK 包，5s 后会出现提示最后一个包是 ”ZACK“ 无法正常关闭
                // 这里直接设置 _last_header_name 为 ZRINIT，就可以强制关闭了
                this.zsession._last_header_name = 'ZRINIT'
                this.zsession.close()
            } catch (e) {
                console.log(e)
            }
            this.close()
        },
        beforeUpload(file, fileList) {
            this.fileList = [...this.fileList, file]
            return false
        },
    },
    mounted() {},
}
</script>
<style scoped>
</style>