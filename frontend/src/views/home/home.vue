<template>
    <div>
        <div class="top">
            <div class="box">
                <img width="100" src="../../assets/image/resources.png" alt="">
                <div class="box_right">
                    <h3>资源总数</h3>
                    <p>
                        <a v-if="role" @click="$router.push({path:'/resources/host'})">主机 {{number.host_count}}</a>
                        <span v-else>主机 {{number.host_count}}</span>
                    </p>
                </div>
            </div>
            <div class="box">
                <img width="100" src="../../assets/image/conversation.png" alt="">
                <div class="box_right">
                    <h3>会话统计</h3>
                    <p>
                        <a v-if="role" @click="$router.push({path:'/auditManagement/online'})">在线会话 {{number.session_unfinished_count}}</a>
                        <span v-else>在线会话 {{number.session_unfinished_count}}</span>
                        <a v-if="role" @click="$router.push({path:'/auditManagement/historical'})">历史会话 {{number.session_finished_count}}</a>
                        <span v-else>历史会话 {{number.session_finished_count}}</span>
                    </p>
                </div>
            </div>
            <div class="box">
                <img width="100" src="../../assets/image/strategy.png" alt="">
                <div class="box_right">
                    <h3>授权策略</h3>
                    <p>
                        <a v-if="role" @click="$router.push({path:'/accessPolicy/visitPolicy'})">访问策略 {{number.strategy_access_count}}</a>
                        <span v-else>访问策略 {{number.strategy_access_count}}</span>
                        <a v-if="role" @click="$router.push({path:'/accessPolicy/commandPolicy'})">命令策略 {{number.strategy_command_count}}</a>
                        <span v-else>命令策略 {{number.strategy_command_count}}</span>
                    </p>
                </div>
            </div>
            <div class="box">
                <img width="100" src="../../assets/image/voucher.png" alt="">
                <div class="box_right">
                    <h3>资源凭证</h3>
                    <p>
                        <a v-if="role" @click="$router.push({path:'/voucher/password'})">密码凭证 {{number.credential_password_count}}</a>
                        <span v-else>密码凭证 {{number.credential_password_count}}</span>
                        <a v-if="role" @click="$router.push({path:'/voucher/ssh'})">SSH密钥 {{number.credential_ssh_count}}</a>
                        <span v-else>SSH密钥 {{number.credential_ssh_count}}</span>
                    </p>
                </div>
            </div>
        </div>

        <div class="content">
            <div class="left">
                <a-card title="最近登录历史">
                    <a v-if="role" @click="$router.push({path:'/auditManagement/historical'})" slot="extra">
                        更多>>
                    </a>
                    <a-table :pagination="false" :loading="tableLoading" :columns="columns" :data-source="tableData">
                        <template slot="server" slot-scope="text,record">
                            {{`${record.login_name}@${record.host_address}`}}
                        </template>
                    </a-table>
                </a-card>
            </div>
            <div class="right">
                <a-card title="资源类型统计">
                    <div id="round1" style="height:400px;"></div>
                </a-card>
            </div>
        </div>
    </div>
</template>

<script>
import { getSessionLog } from '@/api/session'
import { getHome } from "@/api/home.js"
import * as echarts from 'echarts';
var moment = require('moment');
export default {
    data() {
        return {
            number: {},
            tableLoading: false,
            columns: [
                {
                    title: '登录用户',
                    dataIndex: 'user',
                    ellipsis: true,
                    width: 150,
                },
                {
                    title: '资源凭证',
                    dataIndex: 'server',
                    ellipsis: true,
                    scopedSlots: { customRender: 'server' },

                },
                {
                    title: '登录时间',
                    dataIndex: 'start_time',
                    ellipsis: true,

                },
                {
                    title: "执行时间",
                    dataIndex: "duration",
                    ellipsis: true,
                    width: 100,
                },
            ],
            tableData: [],
            option: {
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    bottom: '5%',
                    left: 'center'
                },
                title: {
                    text: "主机类型",
                    left: "center",
                    subtext: "",
                    top: "center"

                },
                color: ['#91CC75', '#FAC858', '#EE6666', '#5470C6',],
                series: [
                    {
                        name: '访问来源',
                        type: 'pie',
                        radius: ['40%', '60%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,

                        },

                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '40',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: []
                    }
                ]
            },
            role: 0,
        }
    },
    mounted() {
        this.getHomeData()
        this.getSessionLogData()
    },
    methods: {
        getHomeData() {
            getHome().then(res => {
                let data = res.data
                if (res.code == 200 && res.data) {
                    this.number = {
                        host_count: data.host_count,
                        session_count: data.session_count,
                        session_finished_count: data.session_finished_count,
                        session_unfinished_count: data.session_unfinished_count,
                        strategy_access_count: data.strategy_access_count,
                        strategy_command_count: data.strategy_command_count,
                        credential_password_count: data.credential_password_count,
                        credential_ssh_count: data.credential_ssh_count,
                    }
                }
                let arr = [], total = 0
                let hostList = data.resource.host
                for (var key in hostList) {
                    total += hostList[key]
                    arr.push({
                        name: key,
                        value: hostList[key],
                    })
                }
                this.option.series[0].data = arr
                this.option.title.subtext = "总数" + total
                var round1 = echarts.init(document.getElementById('round1'));
                round1.setOption(this.option);
                this.role = res.data.role
            })
        },
        // 获取审计历史数据
        getSessionLogData() {
            this.tableLoading = true
            let updata = {
                current: 1,
                pageSize: 7,
                finished: 1,
            }
            getSessionLog(updata).then(res => {
                if (res.code == 200 && res.data) {
                    res.data.data.map(item => {
                        item.key = item.id
                        let millisecond = (Date.parse(item.end_time) - Date.parse(item.start_time))
                        if (millisecond < 60000) {
                            item.duration = Math.ceil(millisecond / 1000) + "s"
                        } else {
                            item.duration = moment.duration(millisecond).humanize()
                        }
                    })
                    this.tableData = res.data.data
                } else {
                    this.tableData = []
                }
            }).finally(() => {
                this.tableLoading = false
            })
        }
    },

}
</script>
<style lang="less" scoped>
.top {
    display: flex;
    .box {
        flex: 0px 1 1;
        display: flex;
        align-items: center;
        background: #fff;
        margin: 0 0 0 16px;
        padding: 0 0 0 40px;
        height: 140px;
        // justify-content: center;
        &:nth-of-type(1) {
            margin: 0;
        }
        img {
            width: 64px;
        }
        .box_right {
            margin: 0 0 0 20px;
        }
        h3 {
            font-size: 22px;
        }
        p {
            font-size: 14px;
            margin: 0;
            a:nth-of-type(2) {
                margin: 0 0 0 10px;
            }
            span:nth-of-type(2){
                margin: 0 0 0 10px;
            }
        }
    }
}
.content {
    display: flex;
    margin: 16px 0 0 0;
    .left {
        background: #fff;
        flex: 0px 1 1;
    }
    .right {
        background: #fff;
        flex: 0px 1 1;
        margin: 0 0 0 16px;
    }
}
/deep/ .ant-table-tbody > tr > td {
    height: 53px;
}
.ant-card-bordered {
    border: none;
}
</style>