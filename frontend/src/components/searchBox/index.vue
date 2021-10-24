<template>
    <div class="content">
        <div v-show="visible" :class="visible ? 'active' : 'primary'">
            <slot></slot>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        visible: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {}
    },
    methods: {},
    mounted() {},
}
</script>
<style scoped lang="less">
.content {
    background: #f9f9f9;
    transition: all 0.3s;
    border-radius: 5px;
}
.active {
    height: auto;
    padding: 18px;
}
.primary {
    height: 0;
}
</style>