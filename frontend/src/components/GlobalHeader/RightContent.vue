<template>
    <div :class="wrpCls" class="right_content">
        <!-- <NavMenu class="abso_left" /> -->
        <btn-group :class="prefixCls" class="btn_group" />
        <!-- i18 lang; if you dont need it ,you can remove it -->
        <!-- <select-lang :class="prefixCls" />  -->
        <avatar-dropdown :menu="showMenu" :current-user="currentUser" :class="prefixCls" />
    </div>
</template>

<script>
import AvatarDropdown from './AvatarDropdown'
import BtnGroup from './BtnGroup'
import NavMenu from './NavMenu'
import SelectLang from '@/components/SelectLang'

export default {
    name: 'RightContent',
    components: {
        AvatarDropdown,
        BtnGroup,
        SelectLang,
        NavMenu,
    },
    props: {
        prefixCls: {
            type: String,
            default: 'ant-pro-global-header-index-action',
        },
        isMobile: {
            type: Boolean,
            default: () => false,
        },
        topMenu: {
            type: Boolean,
            required: true,
        },
        theme: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            showMenu: true,
            currentUser: {},
        }
    },
    computed: {
        wrpCls() {
            return {
                'ant-pro-global-header-index-right': true,
                [`ant-pro-global-header-index-${this.isMobile || !this.topMenu ? 'light' : this.theme}`]: true,
            }
        },
    },
    mounted() {
        setTimeout(() => {
            this.currentUser = {
                name: 'Serati Ma',
            }
        }, 1500)
    },
}
</script>
<style lang="less" scoped>
.right_content {
    color: #fff;
}
.abso_left {
    position: absolute;
    left: 70px;
    top: 0;
}
.btn_group:hover {
    background-color: transparent !important;
}
</style>