<template>
    <div class="content">
        <a :href="otherAppUrl + 'console/console'" target="_blank">
            <a-button type="link" class="a-button"><a-icon class="icon-color" type="desktop"></a-icon>控制台</a-button>
        </a>
        <a :href="origin + 'console/'" target="_blank">
            <a-button type="link" class="a-button"><a-icon class="icon-color" type="home"></a-icon>工作台</a-button>
        </a>
        <a href="https://docs.opsany.com/" target="_blank" style="margin-left: -8px">
            <a-button type="link" class="a-button"><a-icon class="icon-color" type="file-text"></a-icon>文档</a-button>
        </a>
    </div>
</template>
<script>
export default {
    data() {
        return {
            otherAppUrl: window.location.origin + window.location.pathname + '#/',
            showMore: false,
            loading: false,
            msgList: [],
            count: 0,
            origin: window.location.origin + '/',
        }
    },
    methods: {},
    mounted() {},
}
</script>
<style scoped lang="less">
.content {
    color: #fff;
    button {
        border: none !important;
        color: #fff;
    }
    .icon-color {
        color: #fff;
    }
    .message {
        display: inline-block;
        position: relative;
        min-width: 80px;
        text-align: center;
        .message_icon {
            transform: translateY(-1px);
        }
    }
    .badge {
        display: inline-block;
        padding: 1px 2px;
        min-width: 16px;
        min-height: 15px;
        line-height: 15px;
        text-align: center;
        background-color: #ff9900;
        color: #ffffff;
        border-radius: 50%;
        position: absolute;
        top: 4px;
        right: 0px;
        font-size: 10px;
    }
}

.message_content {
    width: 250px;
    min-height: 100px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #eeeeee;
        background: #fafafa;
        &_title {
            font-weight: bold;
        }
        &_right {
            color: #0099ff;
            cursor: pointer;
        }
    }
    .desc {
        width: 100%;
        padding: 8px 10px;
        cursor: pointer;
        &:hover {
            background-color: #eeeeee;
        }
        div {
            overflow: hidden;
            word-break: break-all;
            white-space: nowrap;
            text-overflow: ellipsis;
        }
        &_title {
            color: #333333;
        }
        &_time {
            font-size: 14px;
            color: #666666;
        }
        &:not(:last-child) {
            border-bottom: 1px solid #eeeeee;
        }
    }
    .more {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 10px;
        color: @primary-color;
    }
}
</style>