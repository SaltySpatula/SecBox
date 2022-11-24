<template>
 <div></div>
</template>

<script>
export default {
  name: "IPFrequencyGraph",
  props: {graph_title: String, data: Object, colors: Object},
  created() {
    console.log("IPF ", this.data)
  },
  data: function () {
    return {



    }

  },
  methods: {},
}
</script>

<style scoped>

</style>