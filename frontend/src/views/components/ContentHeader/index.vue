<template>
    <a-card class="card" :bodyStyle="{ padding: '18px' }">
        <div>
            <span class="title">{{ mainTitle1||mainTitle }}</span>
            <span class="breadcrumb">
                <a-breadcrumb-item
                    separator=">"
                    @click.native="clickParentRoute"
                    :style="{ cursor: parentRouteName && 'pointer' }"
                    >{{ parentTitleShow }}</a-breadcrumb-item
                >
                <a-breadcrumb-item separator>{{ mainTitle }}</a-breadcrumb-item>
            </span>
            <span class="docs">
                <slot name="docs"></slot>
            </span>
        </div>
        <div class="card_right">
            <slot name="right"></slot>
        </div>
    </a-card>
</template>
<script>
import { mapState } from 'vuex'
export default {
    props: {
        parentTitle: {
            type: String,
            default: '',
            required: false,
        },
    },
    data() {
        return {
            mainTitle: '',
            parentRouteName: undefined,
            mainTitle1:undefined,
        }
    },
    methods: {
        expandMenu() {
            const arr = []
            const expand = (list = this.asyncMenuList) => {
                list.forEach((item) => {
                    arr.push(item)
                    if (item.children?.length) {
                        expand(item.children)
                    }
                })
            }
            expand()
            return arr
        },
        clickParentRoute() {
            this.parentRouteName && this.$router.push({ name: this.parentRouteName })
        },
    },
    mounted() {
        const meta = this.$route.meta || {}
        this.mainTitle = (Object.keys(meta).length && meta.title) || '--'
    },
    computed: {
        ...mapState({
            asyncMenuList: (state) => state.app.asyncMenuList,
        }),
        parentTitleShow() {
            if (this.parentTitle) return this.parentTitle
            else {
                const meta = this.$route.meta || {}
                this.mainTitle = (Object.keys(meta).length && meta.title) || '--'
                const RouterList = this.expandMenu()
                const asyncActiveRoute = RouterList.find((item) => item.menu_code == this.$route.name) || {}
                const parentRoute = RouterList.find((item) => item.id == asyncActiveRoute.parent_id)
                //如果后端返回的数据中找不到父级路由
                //那么可能是详情页，详情页的父级路由name名称在meta中
                if (!parentRoute) {
                    const childPageParentRoute = RouterList.find((item) => item.menu_code == meta.parentRouteName) || {}
                    this.parentRouteName = childPageParentRoute.menu_code
                    return childPageParentRoute.menu_name || '父级导航'
                }
                this.parentRouteName = undefined
                return parentRoute.menu_name
            }
        },
    },
}
</script>
<style scoped lang="less">
.card {
    width: 100%;
    /deep/ .ant-card-body {
        align-items: center;
        display: flex;
        justify-content: space-between;
        align-items: center;
        &::before {
            content: none;
        }
        &::after {
            content: none;
        }
    }
    .title {
        font-size: 22px;
        font-weight: bold;
    }
    .breadcrumb {
        margin-left: 30px;
    }
    .docs {
        display: inline-block;
        margin-left: 40px;
        color: #00ac63;
    }
}
</style>