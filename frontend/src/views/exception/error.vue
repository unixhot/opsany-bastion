<template>
    <div>

        <div v-if="$route.query.state==2" class="block">
            <img src="@/assets/image/authorization_expired.png" alt="">
            <div class="block_right">
                <p>产品授权已过期，请前往重新授权</p>
                <a-button @click="gotorbac" type="primary" style="width:120px;">立即授权</a-button>
            </div>
        </div>

        <div v-else-if="$route.query.state==1||$route.query.state==3" class="block">
            <img src="@/assets/image/not_authorized.png" alt="">
            <div class="block_right">
                <p>产品暂未授权，请前往授权</p>
                <a-button @click="gotorbac" type="primary" style="width:120px;">立即授权</a-button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        gotorbac() {
            let url = window.API_ROOT.replace('/monitor', '')
            window.location.href = url + "rbac/#/setting/productAuthorization"
        }
    }
}
</script>

<style lang="less" scoped>
.block {
    display: flex;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    img {
        width: 360px;
        height: 360px;
    }
    .block_right {
        margin: 0 0 0 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        p {
            margin: 0 0 30px 0;
            color:#333;
            font-size: 24px;
        }
    }
}
</style>