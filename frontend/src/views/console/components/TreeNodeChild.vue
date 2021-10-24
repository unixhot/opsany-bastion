<template>
    <a-directory-tree multiple defaultExpandAll>
        <a-tree-node :key="item.key" :title="item.name" :is-leaf="item.type == 'host'" v-for="item in treeList">
            <!-- <a-tree-node
                v-for="child in item.children"
                :key="child.key"
                :title="child.name"
                :is-leaf="child.type == 'host'"
            /> -->
            <TreeMenus v-if="item.children.length" :treeList="item.children"></TreeMenus>
        </a-tree-node>
    </a-directory-tree>
</template>
<script>
import { getHostGroupList } from '@/api/host-group-console'
export default {
    name: 'TreeMenus',
    props: {
        treeList: {
            type: Array,
            default() {
                return []
            },
        },
    },
    data() {
        return {}
    },
    methods: {
        getHostGroupList() {
            getHostGroupList().then((res) => {
                console.log(res.data)
                this.treeList = res.data
            })
        },
    },
    mounted() {
        // this.getHostGroupList()
    },
}
</script>
<style scoped lang='less'>
</style>