<template>
    <div style="height: 100%" class="container">
        <div ref="guacamole_box" class="guacamole_box">
            <div class="guacamole_box_visible">
                <div id="guacamole_box"></div>
            </div>
        </div>
        <button id="clipboard" hidden data-clipboard-text=""></button>
        <a-input :auto-focus="autofocus" ref="input" hidden></a-input>
        <div class="info" v-if="showRight">
            <div class="rightbox">
                <a-tabs v-model="tabs_key" @change="changeTabs">
                    <a-tab-pane key="1" tab="会话详情" class="session_info">
                        <a-spin :spinning="sessionLoading">
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
                    <a-tab-pane key="2" tab="文件传输" class="file_trans" :disabled="!file_manager">
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
                <a-button v-if="tabs_key == 1" class="term_info_button" type="primary" @click="closeRemote"
                    >关闭/结束会话</a-button
                >
            </div>
        </div>
    </div>
</template>
<script>
import Guacamole from 'guacamole-common-js'
import { stringifyUrl } from '@/utils/util'
import { getLinkCheck } from '@/api/link-check'
import { getWinFileInfo, downLoadWinFile, uploadWinFile, delWinFile } from '@/api/windowsfile'
import ClipboardJS from 'clipboard'
import Mousetrap from 'mousetrap'
import screenArr from '@/utils/screenArr'
export default {
    data() {
        return {
            wsurl: '',
            guac: null, //guacamole实例
            host_token: '',
            urlParams: {},
            nodeInfo: {},
            sessionLoading: false,
            fileLoading: false,
            uploadLoading: false,
            tabs_key: '1',
            tableData: [],
            breadCrumbList: [],
            current_path: '',
            autofocus: false,
            showRight: true,
            copy_tool: false, //是否可以复制
            file_download: false, //是否可下载
            file_upload: false, //是否可上传
            file_manager: false, //是否可看文件管理
            timer: null,
            scale: 1,
            dpi: 96,
            screenArr,
            activeScreen: {},
            winSizeKey: undefined,
        }
    },
    methods: {
        async initContent() {
            const protocol = window.location.protocol == 'http:' ? 'ws' : 'wss'
            this.wsurl =
                process.env.NODE_ENV === 'development'
                    ? 'wss://dev.opsany.cn/ws/bastion/'
                    : `${protocol}://${window.location.host}/ws/bastion/`
            let path = `${this.wsurl}guacamole/`
            this.guac = new Guacamole.Client(new Guacamole.WebSocketTunnel(path))

            this.getNodeInfo().then((res) => {
                this.handleMousetrap()
            })

            this.$nextTick(() => {
                const guacamoleEl = document.getElementById('guacamole_box')
                this.resizeCanvas()
                guacamoleEl.appendChild(this.guac.getDisplay().getElement())

                const params = {
                    token: this.host_token,
                    width: this.activeScreen.width,
                    height: this.activeScreen.height,
                    dpi: this.dpi,
                }
                // Connect
                this.guac.connect(stringifyUrl(params).replace('?', ''))

                // Error handler
                this.guac.onerror = (error) => {
                    const msg =
                        error.message == 'Disconnected by other connection.'
                            ? '另一用户已连接到此远程计算机，因此您的连接已失效。'
                            : 'Windows堡垒机连接失败，请检查机器状态或联系管理员处理。'
                    this.$notification.open({
                        message: '提示',
                        description: msg,
                        icon: <a-icon type="frown" style="color: #FF4D4F" />,
                    })
                }

                //当远程客户端的剪贴板更改时触发。
                this.guac.onclipboard = (stream, mimetype) => {
                    if (/^text\//.test(mimetype)) {
                        var stringReader = new Guacamole.StringReader(stream)
                        var res = ''
                        stringReader.ontext = function ontext(text) {
                            res += text
                        }
                        stringReader.onend = function () {
                            if (res.length <= 65535) {
                                const dom = document.getElementById('clipboard')
                                dom.setAttribute('data-clipboard-text', res)
                                let clipboard = new ClipboardJS('#clipboard')
                                dom.click()
                                clipboard.destroy()
                            }
                        }
                    }
                }

                // Mouse
                let mouse = new Guacamole.Mouse(this.guac.getDisplay().getElement())
                const mouseEvent = (mouseState) => {
                    this.guac.sendMouseState(mouseState)
                }
                mouse.onmousedown = mouse.onmouseup = mouseEvent
                mouse.onmousemove = (state) => {
                    updateMouseState(state)
                }
                //处理鼠标坐标缩放
                let updateMouseState = (mouseState) => {
                    mouseState.y = mouseState.y / this.scale
                    mouseState.x = mouseState.x / this.scale
                    this.guac.sendMouseState(mouseState)
                }

                // Keyboard
                let keyboard = new Guacamole.Keyboard(document)
                keyboard.onkeydown = (keysym) => {
                    this.guac.sendKeyEvent(1, keysym)
                }
                keyboard.onkeyup = (keysym) => {
                    this.guac.sendKeyEvent(0, keysym)
                }
            })
        },

        //粘贴事件 监听ctrl+v
        handleMousetrap(keys = ['ctrl+v', 'command+v']) {
            if (!this.copy_tool) return
            Mousetrap.bind(keys, (e) => {
                this.$refs.input.focus()
                navigator.clipboard?.readText().then((data) => {
                    const stream = this.guac.createClipboardStream('text/plain')
                    const writer = new Guacamole.StringWriter(stream)
                    // Send text chunks
                    for (let i = 0; i < data.length; i += 4096) {
                        writer.sendText(data.substring(i, i + 4096))
                    }
                    writer.onack = (state) => {
                        console.log(state)
                    }
                    // Close stream
                    writer.sendEnd()
                })
            })
        },

        //获取主机详情
        getNodeInfo() {
            this.sessionLoading = true
            getLinkCheck({ token: this.host_token, data_type: 'host' })
                .then((res) => {
                    this.nodeInfo = res.data
                })
                .finally(() => {
                    this.sessionLoading = false
                })
            return new Promise((resolve, reject) => {
                getLinkCheck({ token: this.host_token, data_type: 'file_admin' })
                    .then((res) => {
                        this.copy_tool = res.data.copy_tool
                        this.file_download = res.data.file_download
                        this.file_manager = res.data.file_manager
                        this.file_upload = res.data.file_upload
                    })
                    .finally(() => {
                        return resolve()
                    })
            })
        },

        changeTabs(key) {
            key == 2 && this.getWinFileInfo()
        },

        //点击按钮
        clickBtnChild(item) {
            this[item.key] && this[item.key]()
        },
        //刷新
        refresh() {
            this.getWinFileInfo()
        },

        //获取文件传输文件
        getWinFileInfo(path = this.current_path) {
            this.fileLoading = true
            const params = {
                data_type: 'file_list',
                token: this.host_token,
                url: path,
            }
            getWinFileInfo(params)
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

        //处理文件传输的面包屑
        handleBreadCrumb() {
            const arr = (this.current_path && this.current_path.split('/')) || []
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

        //点击面包屑
        clickBread(item, index) {
            if (!item.path) return
            if (index == this.breadCrumbList.length - 1) return
            this.getWinFileInfo(item.path)
        },

        //点击某个文件或文件夹
        clickFileName(item) {
            const path = this.current_path + '/' + item.name
            if (item.type == 'folder') {
                this.getWinFileInfo(path)
            } else {
                this.tableData.forEach((it) => {
                    it.isCheck = false
                })
                item.isCheck = true
            }
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
            window.open(downLoadWinFile(params)) //open新页面下载
            // window.location = downLoadWinFile(params) //不跳转页面下载
        },

        //右侧的上传
        handleUpload(info) {
            this.uploadLoading = true
            const hide = this.$message.loading('文件上传中...', 0)
            const params = new FormData()
            params.append(info.filename, info.file)
            params.append('token', this.host_token)
            params.append('url', this.current_path)
            uploadWinFile(params)
                .then((res) => {
                    this.$message.success(res.message)
                    this.getWinFileInfo()
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
                    return delWinFile(params).then((res) => {
                        this.$message.success('删除成功')
                        this.getWinFileInfo()
                    })
                },
            })
        },

        closeRemote() {
            window.close()
        },

        debounce(fn, wait = 50) {
            this.timer = null
            return () => {
                if (this.timer) {
                    clearTimeout(this.timer)
                }
                this.timer = setTimeout(fn, wait)
            }
        },

        resizeCanvas() {
            this.activeScreen = this.screenArr.find((it) => it.key == this.winSizeKey) || {
                width: window.screen.width * window.devicePixelRatio,
                height: window.screen.height * window.devicePixelRatio,
            }
            const guacamole_box_el = this.$refs.guacamole_box
            let width = Math.floor(guacamole_box_el.getBoundingClientRect().width) //guacamole_box盒子的宽
            let height = window.innerHeight //guacamole_box盒子的高
            const display = this.guac.getDisplay()

            //获取屏幕分辨率。.
            let origWidth = this.activeScreen.width //屏幕分辨率 width
            let origHeigth = this.activeScreen.height //屏幕分辨率 height

            const xscale = width / origWidth
            const yscale = height / origHeigth
            //这样做是为了处理X和Y轴间距
            this.scale = Math.min(xscale, yscale)
            //添加 10% 以进行缩放，因为窗口总是小于屏幕分辨率
            // this.scale += this.scale / 10
            display.scale(this.scale)
        },
    },

    mounted() {
        this.host_token = this.$route.query.host_token
        this.winSizeKey = this.$route.query.winSize
        this.initContent()
        const fn = this.debounce(this.resizeCanvas)
        window.addEventListener('resize', fn)
        this.$once('hook:beforeDestroy', () => {
            window.removeEventListener('resize', fn)
            this.timer && clearTimeout(this.timer)
        })
        navigator.clipboard
            ?.readText()
            .then(() => {})
            .catch((err) => {
                if (err.message == 'Read permission denied.') {
                    this.$message.info('剪贴板读取权限被禁止,为了您的正常使用,请重新打开剪贴板权限。')
                }
            })
    },
    beforeDestroy() {
        // Disconnect on close
        this.guac && this.guac.disconnect()
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
.container {
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    justify-content: space-around;
}
.info {
    width: 320px;
    height: 100%;
    position: relative;
    background: #ffffff;
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
        .term_info_button {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
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
}
.guacamole_box {
    width: calc(100vw - 320px);
    height: 100%;
    overflow: hidden;
    background: #333;
    position: relative;
    z-index: 0;
    margin: 0 auto;
    text-align: center;
    line-height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-around;
    box-sizing: border-box;
}
#guacamole_box {
    background: transparent;
    cursor: none;
    // width: 1200px;
    // height: 800px;
    // box-sizing: content-box;
    // overflow: hidden;
}
</style>


