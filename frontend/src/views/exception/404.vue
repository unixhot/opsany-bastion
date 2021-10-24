<template>
    <!-- <exception-page type="404" /> -->
    <div class="center">
        <img src="@/assets/image/function_not_authorized.png" alt="">
        <p>您暂未授权此功能，请联系管理员授权</p>
    </div>

</template>

<script>
import { ExceptionPage } from '@/components'

export default {
    components: {
        ExceptionPage
    }
}
</script>

<style scoped>
.center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}
img {
    width: 360px;
    height: 360px;
    margin: -100px 0 50px 0;
}
p {
    font-size: 24px;
    color: #333;
}
</style>
