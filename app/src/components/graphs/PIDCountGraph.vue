<template>
  <div></div>
</template>

<script>
export default {
  name: "PacketGraph",
  props:{
    socket:Object,
  },
  created() {

    this.socket.on("pid_graph", function (data){
          console.log(data)
      });


  },
  data: function() {
    return {

    };
  },
}
</script>

<style scoped>

</style>