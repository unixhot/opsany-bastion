<template>
  <global-footer class="footer custom-render">
    <template v-slot:links></template>
    <template v-slot:copyright>Copyright © 2019-2020 OpsAny. All Rights Reserved</template>
  </global-footer>
</template>

<script>
import { GlobalFooter } from '@ant-design-vue/pro-layout'

export default {
    name: 'ProGlobalFooter',
    components: {
        GlobalFooter
    }
}
</script>
