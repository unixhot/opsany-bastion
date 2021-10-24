<template>
    <div>
        <a-select
            default-value="平台导航"
            style="width: 120px"
            :dropdownMatchSelectWidth="false"
            :dropdownMenuStyle="{ width: '100%' }"
            @dropdownVisibleChange="changeSelect"
            class="select"
        >
            <a-icon slot="suffixIcon" type="caret-down" style="color: #fff" />
            <div slot="dropdownRender" class="content" v-show="!loading" @mousedown="(e) => e.preventDefault()">
                <!-- //我的收藏 -->
                <div class="collect">
                    <div class="collect_title">我的收藏</div>
                    <div class="collect_content">
                        <div v-for="item in user_collection" :key="item.id" class="collect_content_box">
                            <div style="cursor: pointer">
                                <a-avatar shape="square" :src="config.baseUrlOfImg + item.nav_icon.icon_url"></a-avatar>
                                <a class="link_style" :href="item.nav_url">{{ item.nav_name }}</a>
                            </div>
                            <div @mousedown="(e) => e.preventDefault()">
                                <a-icon class="icon icon_bg" @click="handleCollect(item.id)" type="star"></a-icon>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- 用户定义的导航 -->
                <div class="usernav">
                    <div v-for="group in navInfo" :key="group.id" class="usernav_box">
                        <div class="usernav_box_title">
                            {{ group.group_name }}
                        </div>
                        <div v-for="item in group.nav_list" :key="item.id">
                            <div class="usernav_box_item">
                                <div style="cursor: pointer">
                                    <a-avatar
                                        shape="square"
                                        :src="config.baseUrlOfImg + item.nav_icon.icon_url"
                                    ></a-avatar>
                                    <a class="link_style" :href="item.nav_url">{{ item.nav_name }}</a>
                                </div>
                                <div @mousedown="(e) => e.preventDefault()">
                                    <a-icon
                                        class="icon"
                                        @click="handleCollect(item.id)"
                                        :class="{ icon_bg: item.is_collection }"
                                        type="star"
                                    ></a-icon>
                                </div>
                            </div>
                            <div class="usernav_box_desc" :title="item.describe">
                                {{ item.describe || '暂无描述' }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </a-select>
    </div>
</template>
<script>
import { getNavList, collection } from '@/api/navSetting'
import config from '@/config/defaultSettings'
export default {
    data() {
        return {
            user_collection: [],
            navInfo: [],
            config: {},
            loading: false,
        }
    },
    methods: {
        getNavList() {
            this.loading = true
            getNavList()
                .then((res) => {
                    const {
                        data: { user_collection, nav_info },
                    } = res
                    this.navInfo = nav_info
                    this.user_collection = user_collection
                })
                .finally(() => {
                    this.loading = false
                })
        },
        handleCollect(id) {
            collection({ nav_id: id }).then((res) => {
                this.getNavList()
            })
        },
        changeSelect(isOpen) {
            isOpen && this.getNavList()
        },
        hrefWindowUrl(url) {
            window.open(url)
        },
    },
    mounted() {
        this.config = config
        this.getNavList()
    },
}
</script>
<style scoped lang="less">
/deep/.select,
.ant-select {
    background: @primary-color;
       .ant-select-selection {
        background: #0d9257;
        border-radius: 25px;
        border-color: @primary-color;
        color: #fff;
    }
}
.content {
    width: 100%;
    height: 100%;
    min-height: 300px;
    margin-bottom: 10px;
    display: flex;
    .collect {
        width: 230px;
        height: auto;
        min-height: 300px;
        border-right: 2px solid #eeeeee;
        &_title {
            padding: 30px 10px 10px 20px;
            border-bottom: 1px solid #eeeeee;
            font-weight: bold;
        }
        &_content {
            &_box {
                padding: 15px 20px 0px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
        }
    }
    .usernav {
        width: auto;
        height: 100%;
        display: flex;
        max-width: 720px;
        flex-wrap: wrap;
        &_box {
            display: flex;
            flex-flow: column;
            flex-wrap: wrap;
            min-width: 200px;
            margin: 0 20px;
            &_title {
                padding: 30px 10px 10px 0px;
                border-bottom: 1px solid #eeeeee;
                font-weight: bold;
            }
            &_item {
                display: flex;
                justify-content: space-between;
                padding: 15px 10px 0 0;
                align-items: center;
            }
            &_desc {
                width: 200px;
                color: gray;
                padding-top: 10px;
                padding-bottom: 10px;
                line-height: 20px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
        }
    }
    .icon {
        cursor: pointer;
    }
    .icon_bg {
        color: #ff9600;
    }
}
.link_style {
    font-weight: 600;
    padding-left: 10px;
    color: #333333;
    &:hover {
        color: #0ba360;
    }
}
</style>