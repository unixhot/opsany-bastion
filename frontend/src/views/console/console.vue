<template>
    <div class="container">
        <div class="container_box">
            <div class="container_box_left" :style="{ width: leftBoxWidth }">
                <a-spin :spinning="treeLoading" style="height: 100%; width: 100%; margin-top:120%"> </a-spin>
                <a-tree
                    v-if="treeList.length"
                    default-expand-all
                    :treeData="treeList"
                    :replaceFields="replaceFields"
                    class="container_box_left_tree"
                >
                    <template slot="title" slot-scope="row">
                        <a-dropdown :trigger="['contextmenu', 'click']">
                            <span :title="row.name + `(${row.host_address})`" class="action_title">
                                <a-icon
                                    :type="row.type == 'group' ? (row.expanded ? 'folder-open' : 'folder') : 'database'"
                                ></a-icon>
                                {{ row.type == 'group' ? row.name : row.name }}</span
                            >
                            <template #overlay v-if="row.type == 'host'">
                                <a-menu
                                    @click="({ key: menuKey }) => onContextMenuClick(row, menuKey)"
                                    style="width: 100px; text-align: center"
                                >
                                    <a-menu-item key="1"
                                        >打开{{ row.system_type == 'Windows' ? '(新窗口)' : '' }}</a-menu-item
                                    >
                                </a-menu>
                            </template>
                        </a-dropdown>
                    </template>
                </a-tree>
            </div>
            <div class="container_box_center" :style="{ width: `calc(100% - ${leftBoxWidth} - ${rightBoxWidth})` }">
                <a-tabs v-model="activeKey" type="editable-card" @edit="deleteCard" hideAdd @change="changeTabs">
                    <a-tab-pane v-for="item in tabList" :key="item.index" :closable="item.closable" forceRender>
                        <template #tab>
                            <a-dropdown :trigger="['contextmenu']">
                                <span :title="item.name + `(${item.host_address})`"> {{ item.name }}</span>
                                <template #overlay v-if="item.system_type == 'Linux'">
                                    <a-menu
                                        style="width: 80px; text-align: center"
                                        @click="({ key: menuKey }) => copySession(item, menuKey)"
                                    >
                                        <a-menu-item key="1">复制会话</a-menu-item>
                                    </a-menu>
                                </template>
                            </a-dropdown>
                        </template>
                    </a-tab-pane>
                </a-tabs>

                <div class="container_box_center_content">
                    <div
                        v-for="item in tabList"
                        :key="item.index"
                        :style="{ height: item.index == activeKey ? '100%' : '0px' }"
                    >
                        <Linux
                            :ref="item.index + '_Linux'"
                            v-show="item.index == activeKey && item.system_type == 'Linux'"
                            :hostParams="item"
                        ></Linux>
                    </div>
                </div>
                <div class="container_box_center_bottom">
                    <div @click="$refs.ControlFontSize.show()"><a-icon type="font-size" /> 字体大小</div>
                    <div @click="handleScreenFull"><a-icon type="fullscreen" /> 全屏</div>
                </div>
                <div class="container_box_center_leftdot" @click="clickLeftDot">
                    <img :src="showRight ? require('@/assets/left_open.png') : require('@/assets/left_close.png')" />
                </div>
                <div class="container_box_center_rightdot" @click="clickRightDot">
                    <img :src="showRight ? require('@/assets/right_open.png') : require('@/assets/right_close.png')" />
                </div>
            </div>
            <div class="container_box_right" :style="{ width: rightBoxWidth }">
                <FileSend ref="FileSend"></FileSend>
            </div>
            <LoginHostModal ref="LoginHostModal" @getHostToken="getHostToken"></LoginHostModal>
            <ControlFontSize ref="ControlFontSize" @setFontSize="setFontSize"></ControlFontSize>
        </div>
    </div>
</template>
<script>
import { getHostGroupList } from '@/api/host-group-console'
import Linux from './components/Linux'
import LoginHostModal from '@/views/resources/modal/LoginHostModal.vue'
import { v4 as uuidv4 } from 'uuid'
import ControlFontSize from './components/ControlFontSize.vue'
import FileSend from './components/FileSend.vue'
export default {
    components: { Linux, LoginHostModal, ControlFontSize, FileSend },
    data() {
        return {
            treeList: [],
            replaceFields: {
                children: 'children',
                title: 'name',
                key: 'key',
            },
            tabList: [],
            activeKey: undefined,
            showLeft: true,
            showRight: true,
            timer: null,
            activeHostToken: undefined,
            treeLoading: false,
        }
    },
    methods: {
        //获取左侧树列表
        getHostGroupList() {
            this.treeLoading = true
            getHostGroupList()
                .then((res) => {
                    this.treeList = res.data
                })
                .finally(() => {
                    this.treeLoading = false
                })
        },
        //删除一个标签页
        deleteCard(key) {
            const index = this.tabList.findIndex((item) => item.index == key)
            this.tabList.splice(index, 1)
            if (this.tabList.length == 0) {
                this.activeKey = undefined
                this.activeHostToken = undefined
                this.$refs.FileSend.resetData()
                return
            }
            this.activeKey = this.tabList[this.tabList.length - 1].index
            this.activeHostToken = this.tabList[this.tabList.length - 1].host_token
            this.$refs.FileSend.getData(this.activeHostToken)
            this.resizeLinux()
        },
        //点击展开或者关闭左侧
        clickLeftDot() {
            this.showLeft = !this.showLeft
            this.resizeLinux()
        },
        //点击展开或者关闭右侧
        clickRightDot() {
            this.showRight = !this.showRight
            this.resizeLinux()
        },
        //Linux堡垒机的resize
        resizeLinux() {
            if (!this.activeKey) return
            const activeComponent = this.$refs[this.activeKey + '_Linux'][0]
            if (activeComponent) {
                setTimeout(() => {
                    activeComponent.resizeTerm()
                }, 120)
            }
        },
        //点击左侧树的菜单
        onContextMenuClick(row, menuKey) {
            if (menuKey == 1) {
                const activeTab = this.tabList.find((item) => item.key == row.key)
                if (activeTab) {
                    return this.copySession(activeTab)
                }
                this.$refs.LoginHostModal.showModal(row, true)
            }
        },
        //复制会话
        copySession(row, menuKey) {
            const index = uuidv4()
            const activeTab = { ...row, index }
            this.tabList.push(activeTab)
            this.activeKey = index
            this.activeHostToken = row.host_token
            this.$refs.FileSend.getData(this.activeHostToken)
            this.resizeLinux()
        },
        //登录弹窗回调
        getHostToken(params, hostInfo) {
            if (hostInfo.system_type == 'Windows') {
                const isDev = process.env.NODE_ENV == 'development'
                const url = isDev
                    ? `https://dev.opsany.cn/t/bastion/#/console/webWindows?host_token=${params.host_token}&winSize=${params.winSize}`
                    : `${window.API_ROOT.replace('/bastion', '')}bastion/#/console/webWindows?host_token=${
                          params.host_token
                      }&winSize=${params.winSize}`
                window.open(url)
                return
            }
            this.activeHostToken = params.host_token
            const index = uuidv4()
            const activeTab = { ...hostInfo, ...params, index }
            this.tabList.push(activeTab)
            this.activeKey = index
            this.$refs.FileSend.getData(this.activeHostToken)
        },
        //设置字体大小
        setFontSize(fontSize) {
            if (!this.activeKey) return
            const activeComponent = this.$refs[this.activeKey + '_Linux'][0]
            if (activeComponent) {
                activeComponent.setFontSize(fontSize)
            }
        },
        //设置全屏
        handleScreenFull() {
            if (!this.activeKey) return
            const activeComponent = this.$refs[this.activeKey + '_Linux'][0]
            if (activeComponent) {
                activeComponent.handleScreenFull()
            }
        },
        //切换标签页触发
        changeTabs(key) {
            const activeItem = this.tabList.find((it) => it.index == key)
            this.activeHostToken = activeItem.host_token
            this.$refs.FileSend.getData(this.activeHostToken)
            this.resizeLinux()
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
    computed: {
        leftBoxWidth() {
            return this.showLeft ? '230px' : '0px'
        },
        rightBoxWidth() {
            return this.showRight ? '320px' : '0px'
        },
    },
    mounted() {
        this.getHostGroupList()

        const resizeLinux = this.debounce(this.resizeLinux, 100)
        window.addEventListener('resize', resizeLinux)
        this.$once('hook:beforeDestroy', () => {
            window.removeEventListener('resize', resizeLinux)
            this.timer && clearTimeout(this.timer)
        })
    },
}
</script>
<style scoped lang='less'>
.container {
    background: transparent;
    height: 100%;
    &_box {
        display: flex;
        height: 100%;
        &_left {
            // width: 230px;
            background: #1f1b1b;
            color: #ffffff;
            transition: width 0.1s;
            &_tree,
            /deep/.ant-tree {
                color: #ffffff;
                height: 100%;
                overflow-y: scroll;
                overflow-x: hidden;

                &::-webkit-scrollbar-thumb {
                    border-radius: 10px;
                    -webkit-box-shadow: inset 0 0 5px #474747;
                    box-shadow: inset 0 0 5px #474747;
                    background: rgba(74, 69, 69, 0.8);

                    &:hover {
                        background: #4a4545;
                    }
                }

                &::-webkit-scrollbar-track {
                    -webkit-box-shadow: inset 0 0 5px #474747;
                    box-shadow: inset 0 0 5px #474747;
                    border-radius: 0;
                }

                &::-webkit-scrollbar {
                    width: 8px;
                    background: #1f1b1b;
                }
                .action_title {
                    display: inline-block;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }
            }
            /deep/ .ant-tree-node-content-wrapper,
            .ant-tree-node-content-wrapper-open {
                color: #ffffff;
            }
            /deep/ .ant-tree li .ant-tree-node-content-wrapper:hover {
                background: rgba(11, 163, 96, 0.6);
            }
            /deep/ .ant-tree li .ant-tree-node-content-wrapper.ant-tree-node-selected {
                background: #0ba360 !important;
            }
        }
        &_center {
            width: calc(100% - 230px - 320px);
            background: #060101;
            color: #ffffff;
            position: relative;
            transition: width 0.1s;

            /deep/ .ant-tabs {
                height: 40px;
            }
            /deep/ .ant-tabs-bar {
                border-bottom: 1px solid #131313;
                background: #131313;
            }
            /deep/ .ant-tabs.ant-tabs-card .ant-tabs-card-bar .ant-tabs-tab {
                background: #131313;
                color: #ffffff;
                border: none;
                border-bottom: 1px solid #131313;
                border-right: 0.5px solid #2f2f2f;
                padding: 0 10px;
                span {
                    display: inline-block;
                    height: 40px;
                }
                i {
                    display: inline-block;
                    height: 40px;
                    color: #ffffff;
                    padding-left: 10px;
                    padding-right: 10px;
                    margin-right: 2px;
                    line-height: 40px;
                }
            }
            /deep/ .ant-tabs.ant-tabs-card .ant-tabs-card-bar .ant-tabs-tab-active {
                border-bottom: 1px solid #0ba360;
            }
            /deep/ .ant-tabs-tab-prev.ant-tabs-tab-arrow-show,
            /deep/.ant-tabs-tab-next.ant-tabs-tab-arrow-show {
                i {
                    color: #ffffff;
                }
            }
            &_content {
                padding: 10px 15px;
                height: calc(100% - 40px - 45px);
            }
            &_bottom {
                height: 45px;
                width: 100%;
                background: #131313;
                position: absolute;
                bottom: 0;
                left: 0;
                color: #eeeeee;
                display: flex;
                align-items: center;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                padding-right: 40px;
                > div {
                    cursor: pointer;
                    padding: 0 10px;
                }
            }

            &_leftdot {
                position: absolute;
                left: 0;
                top: 50%;
                cursor: pointer;
            }
            &_rightdot {
                position: absolute;
                right: 0;
                top: 50%;
                cursor: pointer;
            }
        }
        &_right {
            // width: 320px;
            background: #ffffff;
            color: #333333;
            transition: width 0.1s;
            overflow: hidden;
        }
    }
}
</style>