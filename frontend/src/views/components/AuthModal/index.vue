<template>
    <a-modal :visible="visible" @cancel="handleCancel" :footer="null">
        <div class="content">
            <img src="~@/assets/no-auth.png" alt="" />
            <div>
                您没有权限访问或操作此资源，请联系管理员申请权限。<a-button size="small" type="link" @click="pushRouter"
                    >去申请</a-button
                >
            </div>
        </div>
    </a-modal>
</template>
<script>
import { getPageAuth as getAuth } from '@/api/page-auth'

export default {
    data() {
        return {
            visible: false,
        }
    },
    methods: {
        show() {
            this.visible = true
        },
        handleAuth(action_id) {
            return new Promise((resolve, reject) => {
                return getAuth({ action_id })
                    .then((res) => {
                        !res.data && this.show()
                        return res.data ? resolve(true) : reject(false)
                    })
                    .catch((err) => {
                        return reject(false)
                    })
            })
        },
        handleCancel() {
            this.visible = false
        },
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
    margin: 0 auto;
    text-align: center;
    img {
        width: 250px;
        height: 250px;
    }
    div {
        font-weight: bold;
        margin-bottom: 30px;
    }
}
</style>