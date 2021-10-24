<template>
    <div style="height: 100%; overflow: hidden" type="flex" class="content">
        <div class="content-left" :style="{ width: `100%` }">
            <div :id="tremId" style="height: 100%" class="custom_trem"></div>
            <uploadModal ref="uploadModal" @done="getUploadFileList"></uploadModal>
            <ControlFontSize ref="ControlFontSize" @setFontSize="setFontSize"></ControlFontSize>
        </div>
    </div>
</template>
<script>
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import 'xterm/css/xterm.css'
import 'zmodem.js'
import Zmodem from 'zmodem.js/src/zmodem_browser'
import Browser from '@/utils/zmodem_browser'
import screenfull from 'screenfull'
import uploadModal from './uploadModal'
import ControlFontSize from './ControlFontSize.vue'
import { stringifyUrl } from '@/utils/util'
import { getLinkCheck } from '@/api/link-check'
Zmodem.Browser.send_files = Browser
export default {
    components: { uploadModal, ControlFontSize },
    props: {
        hostParams: {
            type: Object,
            default: () => {
                return {}
            },
        },
    },
    watch: {
        hostParams: {
            handler(val) {
                if (Object.keys(val).length) {
                    this.host_token = val.host_token
                    this.fontSize = val.fontSize
                    this.tremId = 'term_' + val.index
                    this.getAgentInfo()
                }
            },
            deep: true,
            immediate: true,
        },
    },
    data() {
        return {
            tremId: '',
            term: {},
            socket: null,
            fitAddon: null,
            zsentry: null,
            host_token: undefined,
            timer: null,
            nodeInfo: {},
            xtemLoading: false,
            fileLoading: false,
            url: '',
            showRight: true, //是否展示右侧
            fontSize: 14,
        }
    },
    methods: {
        //获取节点详情
        getAgentInfo() {
            this.$nextTick(() => {
                const nodeDom = document.getElementById(this.tremId)
                const height = parseInt(nodeDom.clientHeight / 17)
                const width = parseInt((nodeDom.clientWidth - 20) / 9)
                const protocol = window.location.protocol == 'http:' ? 'ws' : 'wss'

                const isDev = process.env.NODE_ENV === 'development'
                const query = {
                    token: this.host_token,
                    width,
                    height,
                }
                this.url = isDev
                    ? `wss://dev.opsany.cn/ws/bastion/terminalchannel/${stringifyUrl(query)}`
                    : `${protocol}://${window.location.host}/ws/bastion/terminalchannel/${stringifyUrl(query)}`

                this.xtemLoading = true
                getLinkCheck({ token: this.host_token, data_type: 'host' })
                    .then((res) => {
                        this.nodeInfo = res.data
                    })
                    .finally(() => {
                        this.xtemLoading = false
                        this.initSocket()
                    })

            })
        },

        //初始化xterm
        initXterm() {
            let term = new Terminal({
                rendererType: 'canvas', //渲染类型
                rows: 30, //行数
                convertEol: true, //启用时，光标将设置为下一行的开头
                scrollback: 500, //终端中的回滚量
                disableStdin: false, //是否应禁用输入
                cursorStyle: 'underline', //光标样式
                cursorBlink: true, //光标闪烁
                theme: {
                    background: '#060101', //背景色
                    // foreground: 'green', //字体
                },
                fontSize: this.fontSize,
            })
            this.term = term
            this.$nextTick(() => {
                const nodeDom = document.getElementById(this.tremId)
                if (!nodeDom) return
                this.term.open(nodeDom)

                const rows = parseInt(nodeDom.clientHeight / 17)
                const cols = parseInt((nodeDom.clientWidth - 20) / 9)

                this.fitAddon = new FitAddon()
                this.initZmodem()
                this.term.loadAddon(this.fitAddon)
                // 支持输入与粘贴方法
                this.term.onData((key) => {
                    this.socket.onsend(JSON.stringify(key)) //转换为字符串
                })

                this.send(JSON.stringify(['set_size', rows, cols, cols, rows]))

                this.fitAddon.fit()
                this.term.onResize((size) => {
                    const { rows, cols } = size
                    this.send(JSON.stringify(['set_size', rows, cols, cols, rows]))
                })
            })
        },

        //初始化 Zmodem
        initZmodem() {
            if (this.zsentry) this.zsentry = null
            this.zsentry = new Zmodem.Sentry({
                to_terminal: (octets) => {}, //i.e. send to the terminal
                on_retract: (octets) => {},
                sender: (octets) => {
                    this.send(new Uint8Array(octets))
                },
                on_detect: (detection) => {
                    let zsession = detection.confirm()
                    if (zsession.type === 'receive') {
                        this.downloadFile(zsession)
                    } else {
                        this.uploadFile(zsession)
                    }
                },
            })
        },

        //初始化socket实例
        async initSocket() {
            this.socket = new WebSocket(this.url)
            this.socket.onopen = this.open
            this.socket.onerror = this.error
            this.socket.onmessage = this.getMessage
            this.socket.onsend = this.send
            this.socket.onclose = this.close
            this.socket.binaryType = 'arraybuffer' // 必须设置，zmodem 才可以使用
        },

        //上传下载进度条
        updateProgress(xfer) {
            let detail = xfer.get_details(),
                name = detail.name,
                total = detail.size,
                percent
            if (total === 0) {
                percent = 100
            } else {
                percent = Math.round((xfer._file_offset / total) * 100)
            }
            this.term?.write('\r' + name + ': ' + total + ' ' + xfer._file_offset + ' ' + percent + '%    ')
        },

        //获取上传的文件回调
        getUploadFileList(zsession, fileList) {
            Zmodem.Browser.send_files(zsession, fileList, {
                on_offer_response: (obj, xfer) => {
                    !xfer && this.term?.write(obj.name + ' was upload skipped\r\n')
                },
                on_progress: (obj, xfer) => {
                    this.updateProgress(xfer)
                },
                on_file_complete: (obj) => {
                    this.term?.write('\r\n')
                },
            })
                .then((res) => {
                    zsession._last_header_name = 'ZRINIT'
                    zsession.close()
                })
                .catch((err) => {
                    console.log(err)
                })
        },

        //下载 保存文件Zmodem.Browser方法
        saveFile(buffer, xfer) {
            return Zmodem.Browser.save_to_disk(buffer, xfer.get_details().name)
        },

        //上传文件
        uploadFile(zsession) {
            this.$refs.uploadModal.show(zsession)
        },

        //下载文件
        downloadFile(zsession) {
            zsession.on('offer', (xfer) => {
                let FILE_BUFFER = []
                xfer.on('input', (payload) => {
                    this.updateProgress(xfer)
                    FILE_BUFFER.push(new Uint8Array(payload))
                })
                xfer.accept().then(() => {
                    this.saveFile(FILE_BUFFER, xfer)
                    this.term?.write('\r\n')
                    this.send(JSON.stringify('echo -en "OO"'))
                    setTimeout(() => {
                        this.initZmodem()
                    }, 1000)
                })
            })
            zsession.on('session_end', (res) => {
                console.log('--session_end--')
            })
            zsession.start()
        },

        //设置字体大小
        setFontSize(fontSize) {
            this.term.setOption('fontSize', fontSize)
            this.resizeTerm()
        },

        //设置全屏
        handleScreenFull() {
            const nodeDom = document.getElementById(this.tremId)
            this.$nextTick(() => {
                screenfull.toggle(nodeDom)
            })
        },

        open() {
            console.log('%cWebSocket is opend', 'color:#1890ff')
            this.closed = false
            this.initXterm()
        },

        error() {
            console.warn('WebSocket connection error')
        },

        getMessage(msg) {
            if (typeof msg.data == 'object') {
                this.zsentry.consume(msg.data)
            } else {
                const errorArr = [
                    { key: 1, errorMsg: '参数错误，请退出后重新连接。' },
                    { key: 2, errorMsg: '用户认证失败，请退出后重新连接。' },
                    { key: 3, errorMsg: '权限认证未通过，请联系管理员后重试。' },
                    { key: 4, errorMsg: '主机资源类型错误，请联系管理员。' },
                    { key: 5, errorMsg: '连接超时，请退出后重新连接。' },
                    { key: 6, errorMsg: '凭证验证失败，请联系管理员。' },
                    { key: 7, errorMsg: '创建连接失败，请退出后重新连接。' },
                ]
                if (msg.data.indexOf('ws_errcode') > -1) {
                    let str = msg.data.replace(/ws_errcode:/, '')
                    const errorMsgItem = errorArr.find((item) => item.key == str) || {}
                    const errorMsg = errorMsgItem.errorMsg || '连接失败,请联系管理员后重试'
                    this.term?.write(errorMsg)
                    return this.$notification.open({
                        message: '提示',
                        description: ` IP『 ${this.nodeInfo.host_address} 』${errorMsg}`,
                        icon: <a-icon type="frown" style="color: #FF4D4F" />,
                    })
                }
                this.term?.write(msg.data)
            }
        },

        send(order) {
            this.socket?.send(order)
        },

        close(e) {
            this.closed = true
            console.log('%cWebSocket is closed', 'color:orange')
        },

        closeRemote() {
            window.close()
        },

        resizeTerm() {
            const nodeDom = document.getElementById(this.tremId)
            this.$nextTick(() => {
                if (!this.closed && nodeDom) {
                    this.fitAddon.fit()
                }
            })
        },

        debounce(fn, wait = 100) {
            this.timer = null
            return () => {
                if (this.timer) {
                    clearTimeout(this.timer)
                }
                this.timer = setTimeout(fn, wait)
            }
        },
    },
    mounted() {},
    beforeDestroy() {
        this.socket.onsend(JSON.stringify(['close']))
        this.socket.close()
    },
    beforeRouteLeave() {
        this.socket.onsend(JSON.stringify(['close']))
        this.socket.close()
    },
    computed: {},
}
</script>
<style scoped lang="less">
.content {
    display: flex;
    justify-content: space-between;
    &-left {
        // width: calc(100% - 320px);
        overflow: hidden;
    }
    &-right {
        width: 320px;
        transition: width 0.1s;
    }
}
#xterm {
    height: calc(100%);
    background: #060101;
    overflow: hidden;
}
</style>
<style lang="less">
</style>