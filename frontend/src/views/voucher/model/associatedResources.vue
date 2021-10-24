<template>
    <div>
        <a-modal @ok="onSubmit" @cancel="onClose" :confirmLoading="btnLoading" width="900px" v-model="visible" title="添加凭据">
            <!-- <a-radio-group v-model="resource_type" @change="resourceTypeChange" button-style="solid">
                <a-radio-button value="host">
                    主机
                </a-radio-button>
                <a-radio-button value="app">
                    应用
                </a-radio-button>
            </a-radio-group> -->
            <a-transfer :operations="operations" :titles="titles" :list-style="listStyle" style="margin:20px 0 0 0" @change="handleChange" :dataSource="mockData" :targetKeys="targetKeys" show-search :render="item => item.title" />
        </a-modal>
    </div>
</template>

<script>
import { getHost } from "@/api/host"
import { editCredential } from "@/api/credential"
export default {
    data() {
        return {
            visible: false,
            btnLoading: false,
            resource_type: "host",
            // 整体数据
            mockData: [],
            // 右侧数据的key值
            targetKeys: [],

            //全部主机资源选项(穿梭框) 
            allhostList: [],
            // 展示的主机资源选项(编辑时已经绑定过的主机资源不显示)
            hostList: [],
            //被选中的主机(切换资源类型时进行记录) 
            selectedhostList: [],
            //全部应用资源选项(穿梭框) 
            allappList: [],
            // 展示的应用资源选项(编辑时已经绑定过的应用资源不显示)
            appList: [],
            //被选中的应用资源(切换资源类型时进行记录) 
            selectedappList: [],

            listStyle: {
                width: '330px',
                height: '420px',
            },
            titles: ['可选择的主机资源', '已选择的主机资源'],
            operations: ['加入右侧', '加入左侧'],
        }
    },
    mounted() {
        // this.getAllHost()
    },
    methods: {
        show(record) {
            this.visible = true
            this.getAllHost()
            this.activeVoucher = record

            let arr1 = []
            record.host_list.map(item => {
                arr1.push(item.id + "")
            })
            this.selectedhostList = arr1
            this.targetKeys = this.selectedhostList
        },
        onSubmit() {
            this.btnLoading = true
            let updata = this.activeVoucher
            if (this.resource_type == "host") {
                this.selectedhostList = this.targetKeys
            } else {
                this.selectedappList = this.targetKeys
            }
            updata.host_list = this.selectedhostList

            editCredential(updata).then(res => {
                if (res.code == 200) {
                    this.$message.success(res.message)
                    this.onClose()
                }
            }).finally(() => {
                this.btnLoading = false
            })
        },
        onClose() {
            this.visible = false
            this.targetKeys = []
            this.$emit("father")
            this.selectedhostList = []
            this.selectedappList = []
        },
        // 获取所有资源
        getAllHost() {
            getHost({ all_data: 1 }).then(res => {
                if (res.code == 200 && res.data) {
                    let arr = []
                    res.data.map(item => {
                        arr.push({
                            key: item.id + "",
                            title: item.host_name
                        })
                    })
                    this.allhostList = arr
                    this.hostList = this.allhostList
                    this.mockData = this.hostList
                }
            })
        },
        resourceTypeChange() {

        },
        // 穿梭框
        handleChange(nextTargetKeys, direction, moveKeys) {
            this.targetKeys = nextTargetKeys;
        },
    }
}
</script>

<style lang="less" scoped>
</style>