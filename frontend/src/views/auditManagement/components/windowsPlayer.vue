<template>
    <div>
        <a-modal title="审计查看" :visible="visible" :maskClosable="false" :confirm-loading="confirmLoading" @ok="handleOk" @cancel="handleCancel" width="100%" destroyOnClose :dialog-style="{ top: '0' }" :zIndex="1000">
            <div id="player_box" @click="start" @mousemove="mousemove">
                <a-icon :type="iconType" class="icons" id="icons" ref="icons" />
            </div>
        </a-modal>
    </div>
</template>

<script>
import Guacamole from 'guacamole-common-js'
import { getWindowsReplay } from '@/api/session'
export default {
    data() {
        return {
            visible: false,
            confirmLoading: false,
            recording: {},
            iconType: 'play-circle',
            timer: null,
        }
    },

    methods: {
        show(id) {
            this.visible = true
            const url = getWindowsReplay(id)
            this.$nextTick(() => {
                let player_box = document.getElementById('player_box')
                let tunnel = new Guacamole.StaticHTTPTunnel(url, true)
                let recording = new Guacamole.SessionRecording(tunnel)
                this.recording = recording
                let recordingDisplay = recording.getDisplay()
                const recordingDisplayEl = recordingDisplay.getElement()
                player_box.appendChild(recordingDisplayEl)
                console.log(recording)
                recording.connect()
                this.$nextTick(() => {
                    recordingDisplayEl.style.margin = '0 auto'
                })
                recording.onplay = () => {
                    this.iconType = 'pause-circle'
                }
                recording.onpause = () => {
                    this.iconType = 'play-circle'
                }
            })
        },




        start() {
            if (!this.recording.isPlaying()) {
                this.recording.play()
            } else this.recording.pause()
        },
        mousemove() {
            clearTimeout(this.timer)
            this.$nextTick(() => {
                let icons = this.$refs.icons.$el
                icons.style.opacity = 0.5

                this.timer = setTimeout(() => {
                    icons.style.opacity = 0
                }, 2000)
            })
        },
        handleOk() {
            this.visible = false
        },
        handleCancel() {
            this.visible = false
        },
    }

}
</script>
<style scoped lang="less">
/deep/ .ant-modal {
    margin: 0;
    padding: 0;
    /deep/ .ant-modal-body {
        padding: 0;
    }
}
#player_box {
    width: 100%;
    height: calc(100vh - 55px - 53px);
    z-index: 0;
    overflow-y: scroll;
    position: relative;
    background: black;
    // &:hover .icons {
    //     opacity: 0.5;
    // }
    > div {
        width: 100%;
        height: calc(100vh - 55px - 53px);
        margin: 0 auto;
    }
}
.icons {
    font-size: 100px;
    opacity: 0;
    color: @primary-color;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    transition: all 0.2s;
}
</style>