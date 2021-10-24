<template>
    <div>
        <div class="content">
            <img src="~@/assets/no-auth.png" alt="" />
            <div>
                您没有权限访问或操作此资源，请联系管理员申请权限。<a-button type="link" @click="pushRouter"
                    >去申请</a-button
                >
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {}
    },
    methods: {
        pushRouter() {
            const origin = window.location.origin
            window.open(origin + '/o/bk_iam/apply-join-user-group')
        },
    },
    mounted() {},
}
</script>
<style scoped lang='less'>
.content {
    padding-top: 80px;
    margin: 0 auto;
    text-align: center;
    img {
        width: 340px;
        height: 340px;
    }
    div {
        padding-left: 50px;
    }
}
</style>