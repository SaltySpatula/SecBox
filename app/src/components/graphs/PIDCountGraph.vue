<template>
  <v-card class="bg-black" style="margin:10px">
    <v-card-title style="align:center">Process Counts</v-card-title>
  <apexchart
      ref="PIDGraph"
      :options="chartOptions"
      :series="series"
      :height="300"
    ></apexchart>
  </v-card>
</template>

<script>
export default {
  name: "PacketGraph",
  props:{
    socket:Object,
  },
  created() {
    let ref = this
    this.socket.on("pid_graph", function (data){
      if (data["infected_status"] === "healthy"){
          ref.pid_count[0] = data["data"]["pid_count"]["pid_count"];

      }
      else if (data["infected_status"] === "infected"){
        ref.pid_count[1] = data["data"]["pid_count"]["pid_count"];
      }

      ref.$refs.PIDGraph.updateSeries(ref.pid_count)

      });


  },
  data: function() {
    return {
      pid_count : [0, 0],
      pid_count_old : [0, 0],
      chartOptions: {
               chart: {
        labels:["healthy", "infected"],


        type: 'donut',
          foreColor: '#ffffff',
          toolbar: {
                show: false
              },
      },
        legend: {position: "bottom"},
        colors:["#207f10", "#d31313"],
      },
        series: [0, 0]
    };
  },
}
</script>

<style scoped>

</style>