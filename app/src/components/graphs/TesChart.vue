<template>
  <div>
    <VuePlotly :data="data" :layout="layout" :display-mode-bar="false"></VuePlotly>
  </div>
</template>

<script>
import { VuePlotly } from 'vue3-plotly'

export default {
  components: {
    VuePlotly
  },
  data() {
    return {
      data:[{
        x: [1,2,3,4],
        y: [10,15,13,17],
        type:"scatter"
      }],
      layout:{
        title: "My graph"
      }
    }
  }
}
</script>

<style scoped>

</style>