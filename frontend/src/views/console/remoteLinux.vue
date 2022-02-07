<template>
    <div style="height: 100%; overflow: hidden" type="flex" class="content">
        <div class="content-left" :style="{ width: `calc(100% - ${showRight ? '320px' : '0px'})` }">
            <div id="xterm"></div>
            <div class="xterm_bottom">
                <div @click="$refs.ControlFontSize.show()"><a-icon type="font-size" /> 字体大小</div>
                <div @click="handleScreenFull"><a-icon type="fullscreen" /> 全屏</div>
                <div @click="handleShowRight"><a-icon :type="showRight ? 'eye' : 'eye-invisible'" /> 会话详情</div>
            </div>
            <uploadModal ref="uploadModal" @done="getUploadFileList"></uploadModal>
            <ControlFontSize ref="ControlFontSize" @setFontSize="setFontSize"></ControlFontSize>
        </div>
        <div style="height: 100%" class="content-right" :style="{ width: showRight ? '320px' : '0px' }">
            <div class="rightbox">
                <a-tabs v-model="tabs_key" @change="changeTabs">
                    <a-tab-pane key="1" tab="会话详情" class="session_info">
                        <a-spin :spinning="xtemLoading">
                            <div style="height: 100%">
                                <div>
                                    <div class="term_info_box">
                                        <div class="term_title">主机信息</div>
                                        <div class="term_info">主机名称：{{ nodeInfo.host_name || '-' }}</div>
                                        <!-- <div class="term_info">唯一标识：{{ nodeInfo.name || '-' }}</div> -->
                                        <div class="term_info">IP地址：{{ nodeInfo.host_address || '-' }}</div>
                                    </div>
                                </div>
                            </div>
                        </a-spin>
                    </a-tab-pane>
                    <a-tab-pane
                        v-if="linkType == 'host'"
                        key="2"
                        tab="文件传输"
                        class="file_trans"
                        :disabled="!file_manager"
                    >
                        <a-spin :spinning="fileLoading">
                            <div style="height: 100%; overflow: hidden">
                                <div class="top_btns">
                                    <a-tooltip placement="top" v-for="item in btnList" :key="item.key">
                                        <template slot="title">
                                            <span>{{ item.disabled ? item.disabledHelp : item.text }}</span>
                                        </template>
                                        <a-button
                                            :icon="item.icon"
                                            type="link"
                                            :disabled="item.disabled"
                                            @click="clickBtnChild(item)"
                                            v-if="item.icon != 'upload'"
                                        ></a-button>
                                        <a-upload
                                            v-else
                                            name="file"
                                            :multiple="false"
                                            :showUploadList="false"
                                            :withCredentials="true"
                                            :customRequest="handleUpload"
                                            :disabled="uploadLoading"
                                        >
                                            <a-button
                                                :icon="item.icon"
                                                type="link"
                                                :disabled="item.disabled"
                                                @click="clickBtnChild(item)"
                                            ></a-button>
                                        </a-upload>
                                    </a-tooltip>
                                </div>
                                <div class="bread_box">
                                    <a-breadcrumb class="breadcrumb_box">
                                        <a-breadcrumb-item
                                            v-for="(item, index) in breadCrumbList"
                                            :key="index"
                                            @click.native="clickBread(item, index)"
                                            class="breadcrumb"
                                            :title="item.name"
                                            :style="breadcrumbStyle"
                                        >
                                            {{ item.name }}
                                        </a-breadcrumb-item>
                                    </a-breadcrumb>
                                </div>
                                <div v-if="tableData.length" class="file_box">
                                    <div
                                        v-for="(item, index) in tableData"
                                        :key="index"
                                        :class="{ isCheck: item.isCheck }"
                                    >
                                        <span :title="item.name" @click="clickFileName(item)">
                                            <a-icon :type="item.type" style="padding-right: 2px"></a-icon>
                                            <a-tooltip placement="topLeft" :mouseLeaveDelay="0.05">
                                                <template slot="title">
                                                    <span>{{ item.name }}</span>
                                                </template>
                                                <span>{{ item.name }}</span>
                                            </a-tooltip>
                                        </span>
                                        <a-tooltip placement="top">
                                            <template slot="title">
                                                <span>删除</span>
                                            </template>
                                            <a-icon type="delete" class="del_icon" @click="rightDelFile(item)"></a-icon>
                                        </a-tooltip>
                                    </div>
                                </div>
                                <a-empty v-else style="margin-top: 200px"></a-empty>
                            </div>
                        </a-spin>
                    </a-tab-pane>
                </a-tabs>
                <div class="term_info_buttonbox" v-if="showRight">
                    <a-button v-if="tabs_key == 1" class="term_info_button" type="primary" @click="closeRemote"
                        >关闭/结束会话</a-button
                    >
                </div>
            </div>
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
import uploadModal from './components/uploadModal'
import ControlFontSize from './components/ControlFontSize.vue'
import { stringifyUrl } from '@/utils/util'
import { getLinkCheck } from '@/api/link-check'
import { getLinuxFileInfo, downLoadFile, uploadLinuxFile, delLinuxFile } from '@/api/linuxfile'
Zmodem.Browser.send_files = Browser
export default {
    components: { uploadModal, ControlFontSize },
    data() {
        return {
            host_token: undefined,
            term: {},
            socket: null,
            fitAddon: null,
            zsentry: null,
            timer: null,
            nodeInfo: {},
            xtemLoading: false,
            fileLoading: false,
            url: '',
            urlParams: {},
            tabs_key: '1',
            tableData: [],
            current_path: '', //当前目录
            breadCrumbList: [], //面包屑列表
            uploadLoading: false,
            copy_tool: false, //是否可以复制
            file_download: false, //是否可下载
            file_upload: false, //是否可上传
            file_manager: false, //是否可看文件管理
            showRight: true, //是否展示右侧
            fontSize: 14,
            linkType: 'host',
        }
    },
    methods: {
        //获取节点详情
        getAgentInfo() {
            const nodeDom = document.getElementById('xterm')
            const height = parseInt(nodeDom.clientHeight / 17)
            const width = parseInt((nodeDom.clientWidth - 20) / 9)
            const protocol = window.location.protocol == 'http:' ? 'ws' : 'wss'

            const isDev = process.env.NODE_ENV === 'development'
            const query = {
                token: this.host_token,
                width,
                height,
            }
            const apiKey = this.linkType == 'dataBase' ? 'databases' : 'terminalchannel'
            this.url = isDev
                ? `wss://dev.opsany.cn/ws/bastion/${apiKey}/${stringifyUrl(query)}`
                : `${protocol}://${window.location.host}/ws/bastion/${apiKey}/${stringifyUrl(query)}`

            this.xtemLoading = true
            getLinkCheck({ token: this.host_token, data_type: 'host' })
                .then((res) => {
                    this.nodeInfo = res.data
                })
                .finally(() => {
                    this.xtemLoading = false
                    this.initSocket()
                })
            getLinkCheck({ token: this.host_token, data_type: 'file_admin' })
                .then((res) => {
                    this.copy_tool = res.data.copy_tool
                    this.file_download = res.data.file_download
                    this.file_manager = res.data.file_manager
                    this.file_upload = res.data.file_upload
                })
                .finally(() => {})
        },

        //切换tabs
        changeTabs(key) {
            key == 2 && this.getLinuxFileInfo()
        },

        //获取文件详情
        getLinuxFileInfo(path = this.current_path) {
            this.fileLoading = true
            const params = {
                data_type: 'file_list',
                token: this.host_token,
                url: path,
            }
            getLinuxFileInfo(params)
                .then((res) => {
                    this.current_path = res.data.current_path
                    this.handleBreadCrumb()
                    const fileArr = []
                    const folderArr = []
                    res.data.data.file.forEach((item) => {
                        fileArr.push({
                            name: item,
                            type: 'file',
                            isCheck: false,
                        })
                    })
                    res.data.data.path.forEach((item) => {
                        folderArr.push({
                            name: item,
                            type: 'folder',
                            isCheck: false,
                        })
                    })
                    this.tableData = folderArr.concat(fileArr)
                })
                .finally(() => {
                    this.fileLoading = false
                })
        },

        //点击按钮
        clickBtnChild(item) {
            this[item.key] && this[item.key]()
        },

        //刷新
        refresh() {
            this.getLinuxFileInfo()
        },

        //右侧的下载
        rightdownLoadFile() {
            const node = this.tableData.find((item) => item.isCheck)
            if (!node) return this.$message.warning('请选择一个文件后下载')
            const path = this.current_path + '/' + node.name
            const params = {
                token: this.host_token,
                url: path,
                data_type: 'file',
            }
            window.open(downLoadFile(params)) //open新页面下载
            // window.location = downLoadFile(params) //不跳转页面下载
        },

        //右侧的上传
        handleUpload(info) {
            this.uploadLoading = true
            const hide = this.$message.loading('文件上传中...', 0)
            const params = new FormData()
            params.append(info.filename, info.file)
            params.append('token', this.host_token)
            params.append('url', this.current_path)
            uploadLinuxFile(params)
                .then((res) => {
                    this.$message.success(res.message)
                    this.getLinuxFileInfo()
                })
                .finally(() => {
                    hide()
                    this.uploadLoading = false
                })
        },

        //右侧的删除
        rightDelFile(item) {
            const path = this.current_path + '/' + item.name
            const params = {
                token: this.host_token,
                url: path,
            }
            this.$confirm({
                title: '删除确认',
                content: `请确认是否删除【${item.name}】${
                    item.type == 'file' ? '文件' : item.type == 'folder' ? '文件夹' : ''
                }?`,
                okType: 'danger',
                onOk: () => {
                    return delLinuxFile(params).then((res) => {
                        this.$message.success(res.message)
                        this.getLinuxFileInfo()
                    })
                },
            })
        },

        //处理文件传输的面包屑
        handleBreadCrumb() {
            const arr = this.current_path.slice(1).split('/')
            const breadList = []
            arr.forEach((item, index) => {
                const params = {
                    name: item,
                    path: arr.slice(0, index + 1).join('/'),
                }
                breadList.push(params)
            })
            if (breadList.length > 3) {
                breadList.splice(1, breadList.length - 3, { name: '...', path: null })
            }
            this.breadCrumbList = breadList
        },

        //点击某个文件或文件夹
        clickFileName(item) {
            const path = this.current_path + '/' + item.name
            if (item.type == 'folder') {
                this.getLinuxFileInfo(path)
            } else {
                this.tableData.forEach((it) => {
                    it.isCheck = false
                })
                item.isCheck = true
            }
        },

        //点击面包屑
        clickBread(item, index) {
            if (!item.path) return
            if (index == this.breadCrumbList.length - 1) return
            this.getLinuxFileInfo(item.path)
        },

        //初始化xterm
        initXterm() {
            let term = new Terminal({
                rendererType: 'canvas', //渲染类型
                rows: 30, //行数
                convertEol: true, //启用时，光标将设置为下一行的开头
                scrollback: 150000, //终端中的回滚量
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
                const nodeDom = document.getElementById('xterm')
                if (!nodeDom) return
                this.term.open(nodeDom)

                const rows = parseInt(nodeDom.clientHeight / 17)
                const cols = parseInt((nodeDom.clientWidth - 20) / 9)

                this.fitAddon = new FitAddon()
                this.initZmodem()
                this.term.loadAddon(this.fitAddon)
                // 支持输入与粘贴方法
                this.term.onData((key) => {
                    const stringKeys = JSON.stringify(key)
                    // if (this.linkType == 'dataBase') {
                    //     if (encodeURI(key) == '%03') {
                    //         return
                    //     }
                    // }
                    this.socket.onsend(stringKeys) //转换为字符串
                })

                this.send(JSON.stringify(['set_size', rows, cols, cols, rows]))

                this.$nextTick(() => {
                    this.fitAddon.fit()
                })
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
            const nodeDom = document.getElementById('xterm')
            this.$nextTick(() => {
                screenfull.toggle(nodeDom)
            })
        },

        //设置是否展示右侧信息栏
        handleShowRight() {
            this.showRight = !this.showRight
            this.resizeTerm()
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
                    { key: 8, errorMsg: '目前不支持该类型数据库。' },
                    { key: 9, errorMsg: '无法连接到代理服务器。' },
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
            const nodeDom = document.getElementById('xterm')
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
    mounted() {
        this.host_token = this.$route.query.host_token
        let linkType = this.$route.query.linkType || ''
        const typeList = ['host', 'dataBase']
        this.linkType = typeList.includes(linkType) ? linkType : typeList[0]
        this.getAgentInfo()
        const fn = this.debounce(this.resizeTerm, 100)
        window.addEventListener('resize', fn)
        this.$once('hook:beforeDestroy', () => {
            window.removeEventListener('resize', fn)
            this.timer && clearTimeout(this.timer)
        })

        const fontSize = this.$route.query.fontSize
        if (isNaN(fontSize)) {
            this.fontSize = 14
        } else {
            if (fontSize - 0 > 20 || fontSize - 0 < 14) {
                this.fontSize = 14
            } else {
                this.fontSize = fontSize - 0
            }
        }
    },
    beforeDestroy() {
        this.socket.onsend(JSON.stringify(['close']))
        this.socket.close()
    },
    beforeRouteLeave() {
        this.socket.onsend(JSON.stringify(['close']))
        this.socket.close()
    },
    computed: {
        btnList() {
            return [
                {
                    icon: 'upload',
                    key: 'upload',
                    text: '上传',
                    disabled: !this.file_upload,
                    disabledHelp: '因权限策略问题，暂时无法上传文件',
                },
                {
                    icon: 'download',
                    key: 'rightdownLoadFile',
                    text: '下载',
                    disabledHelp: '因权限策略问题或未选中文件，暂时无法下载文件',
                    disabled: !this.tableData.find((it) => it.isCheck) || !this.file_download,
                },
                {
                    icon: 'reload',
                    key: 'refresh',
                    text: '刷新',
                    disabled: !this.file_manager,
                    disabledHelp: '因权限策略问题，暂时无法查看文件',
                },
            ]
        },
        breadcrumbStyle() {
            const len = this.breadCrumbList.length
            return {
                maxWidth: len == 1 ? '100%' : len == 2 ? '50%' : len == 3 ? '33%' : '28%',
            }
        },
    },
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
    height: calc(100% - 45px);
    background: #060101;
    overflow: hidden;
}
.xterm_bottom {
    width: 100%;
    height: 45px;
    color: #eeeeee;
    display: flex;
    align-items: center;
    background: #131313;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 40px;
    > div {
        cursor: pointer;
        padding: 0 10px;
    }
}
.rightbox {
    /deep/ .ant-tabs-bar {
        text-align: center;
        margin: 0 0 10px 0;
    }
    .session_info {
        padding: 0 10px;
    }
    .term_info_box {
        &:not(:nth-child(1)) {
            padding-top: 40px;
        }
        .term_title {
            border-bottom: 1px solid #e8e8e8;
            padding-bottom: 5px;
        }
        .term_info {
            padding-top: 8px;
        }
    }
    .term_info_buttonbox {
        width: 320px;
        text-align: center;
        position: absolute;
        bottom: 20px;
        right: 0;
    }

    .file_trans {
        .top_btns {
            padding: 0 10px;
        }
        .bread_box {
            background: #eeeeee;
            margin: 10px 0;
            padding: 10px;
            .breadcrumb_box {
                display: flex;
                .breadcrumb {
                    display: flex;
                    /deep/ .ant-breadcrumb-link {
                        display: inline-block;
                        // max-width: 16%;
                        overflow: hidden;
                        white-space: nowrap;
                        text-overflow: ellipsis;
                    }
                    /deep/ .ant-breadcrumb-separator {
                        display: inline-block;
                        margin: 0 5px;
                    }
                }
                & > .breadcrumb:last-child /deep/.ant-breadcrumb-separator:last-child {
                    display: none;
                }
            }
            .breadcrumb:not(:last-child) {
                cursor: pointer;
            }
        }
        .file_box {
            // padding: 0 10px;
            overflow-y: scroll;
            max-height: calc(100vh - 170px);
            .isCheck {
                background: #0ba360;
                color: #ffffff;
            }
            .isCheck:hover .del_icon {
                color: #ffffff;
            }
            > div {
                padding: 5px 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                &:hover > .del_icon {
                    opacity: 1;
                }

                &:hover:not(.isCheck) {
                    background: #eeeeee;
                }
                > span {
                    cursor: pointer;
                    width: 100%;
                    display: inline-block;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    margin-right: 10px;
                }
                .del_icon {
                    cursor: pointer;
                    transition: all 0.3s;
                    opacity: 0;
                    color: #ff4f4f;
                }
            }
        }
    }
}
</style>