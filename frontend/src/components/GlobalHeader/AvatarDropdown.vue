<template>
    <a-dropdown class="drop">
        <span class="action ant-dropdown-link user-dropdown-menu">
            <span class="ch_name"
                >{{ userInfo.username || 'Anonymous' }} <a-icon type="down" style="color: #fff"
            /></span>
        </span>
        <a-menu slot="overlay" class="user-dropdown-menu-wrapper">
            <a-menu-item key="3">
                <a :href="url + '/accounts/logout/'">
                    <a-icon type="logout" />
                    <span> 退出登录</span>
                </a>
            </a-menu-item>
        </a-menu>
    </a-dropdown>
</template>

<script>
import { getUserInfo } from '@/api/user'
import config from '@/config/defaultSettings'
export default {
    name: 'UserMenu',
    data() {
        return {
            url: window.API_ROOT.split('/')[0],
            otherAppUrl: window.API_ROOT.replace('/bastion', ''),
            userInfo: {},
        }
    },
    methods: {
        getUserInfo() {
            getUserInfo().then((res) => {
                this.userInfo = res.data
                this.userInfo.icon_url = config.baseUrlOfImg + res.data.icon_url
            })
        },
    },
    mounted() {
        this.getUserInfo()
    },
}
</script>
<style lang="less" scoped>
.drop {
    min-width: 80px;
    text-align: center;
}
.ant-pro-drop-down {
    /deep/ .action {
        margin-right: 8px;
    }
    /deep/ .ant-dropdown-menu-item {
        min-width: 160px;
    }
}
.ch_name {
    padding-left: 5px;
    position: relative;
    top: 2px;
    color: #fff;
}
</style>
