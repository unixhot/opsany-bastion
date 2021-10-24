<template>
    <div>
        <a-modal
            title="审计查看"
            :visible="visible"
            :maskClosable="false"
            :confirm-loading="confirmLoading"
            @ok="handleOk"
            @cancel="handleCancel"
            width="960px"
        >
            <div id="player_box" v-html="asciinemaPlayerHtml"></div>
        </a-modal>
    </div>
</template>

<script>
import { baseUrl } from '@/api/session'
export default {
    data() {
        return {
            visible: false,
            confirmLoading: false,
            asciinemaPlayerHtml: '',
        }
    },
    methods: {
        show(file_name) {
            const fileSrc = baseUrl + 'session-log/terminal/' + `${file_name}`+"/"
            this.visible = true
            this.asciinemaPlayerHtml = ''
            this.$nextTick(() => {
                    const asciinemaPlayerHtml = `<asciinema-player id="asciinemaPlayerHtml" cols="132"  src="${fileSrc}"></asciinema-player>`
                    this.asciinemaPlayerHtml = asciinemaPlayerHtml
            })
        },
        handleOk() {
            this.visible = false
        },
        handleCancel() {
            this.visible = false
            const player_box = document.getElementById('player_box')
            const isHaveAsciinemaPlayer = document.getElementById('asciinemaPlayerHtml')
            isHaveAsciinemaPlayer && player_box.removeChild(isHaveAsciinemaPlayer)
        },
    },
    mounted() {},
}
</script>
<style scoped lang="less">

</style>