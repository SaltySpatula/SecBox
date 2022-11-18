<template>
  <v-card class="bg-black" style="margin:10px">
    <v-card-title style="align:center">Number of Processes</v-card-title>
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
  name: "PIDGraph",
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
      chartOptions: {
        pie: {
        donut: {
          labels: {
            show: true,
            name: {
              show: true
            },
            value: {
              show:true
            }
          }
        }
      },
               chart: {
        labels:["healthy", "infected"],


        type: 'donut',
          foreColor: '#ffffff',
          toolbar: {
                show: false
              },
      },
        labels:["healthy", "infected"],
        legend: {position: "bottom"},
        colors:["#d917bf", "#13d3b6"],
      },
        series: [1, 1]
    };
  },
}
</script>

<style scoped>

</style>