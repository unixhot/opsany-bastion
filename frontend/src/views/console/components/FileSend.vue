<template>
    <div>
        <div style="height: 100%" class="content-right">
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
                <!-- <div class="term_info_buttonbox">
                    <a-button v-if="tabs_key == 1" class="term_info_button" type="primary" @click="closeRemote"
                        >关闭/结束会话</a-button
                    >
                </div> -->
            </div>
        </div>
    </div>
</template>
<script>
import { getLinuxFileInfo, downLoadFile, uploadLinuxFile, delLinuxFile } from '@/api/linuxfile'
import { getLinkCheck } from '@/api/link-check'

export default {
    data() {
        return {
            host_token: undefined,
            nodeInfo: {},
            xtemLoading: false,
            fileLoading: false,
            tabs_key: '1',
            tableData: [],
            copy_tool: false, //是否可以复制
            file_download: false, //是否可下载
            file_upload: false, //是否可上传
            file_manager: false, //是否可看文件管理
            current_path: '', //当前目录
            breadCrumbList: [], //面包屑列表
            uploadLoading: false,
        }
    },
    methods: {
        getData(host_token) {
            if (host_token) this.host_token = host_token
            this.getHostInfo()
            this.getHostAuth()
            if (this.tabs_key == 2) this.getLinuxFileInfo()
        },
        resetData() {
            this.nodeInfo = {}
            this.tableData = []
            this.copy_tool = false
            this.file_download = false
            this.file_upload = false
            this.file_manager = false
            this.current_path = ''
            this.breadCrumbList = []
        },
        //获取主机详情
        getHostInfo() {
            this.xtemLoading = true
            getLinkCheck({ token: this.host_token, data_type: 'host' })
                .then((res) => {
                    this.nodeInfo = res.data
                })
                .finally(() => {
                    this.xtemLoading = false
                })
        },
        //获取主机权限
        getHostAuth() {
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
        //上传文件
        uploadFile(zsession) {
            this.$refs.uploadModal.show(zsession)
        },
    },
    mounted() {},
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
<style scoped lang='less'>
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