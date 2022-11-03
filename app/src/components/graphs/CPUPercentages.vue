<template>
  <v-card class="bg-black" style="margin:10px">
    <v-card-title style="align:center">CPU Usage</v-card-title>
      <apexchart
      type="line"
      ref="cpuChartHealthy"
      :options="chartOptions"
      :series="series"
      :background="background"
      :height="300"
    ></apexchart>
    </v-card>
</template>

<script>

export default {
  name: "CPUPercentages",
  props:{
    socket:Object,

  },
  created() {
    let ref = this;
    this.socket.on("cpu_percentages_graph", function (data){
      if (data["infected_status"] === "healthy"){
          let healthy_data = data["data"];
          ref.$refs.cpuChartHealthy.updateOptions({
                xaxis: {
                  categories: healthy_data["timestamps"], //ie ["a","b","c","d"]
                  tickAmount: 15,
                },
            series:[{
            name: 'healthy',
            data: healthy_data["percentages"] //ie [1,2,3,4]
          },{
                  name:"infected",
                  data:ref.infected_cpu_data
            },],

                colors:["#207f10", "#d31313"],
          })
        ref.healthy_cpu_data = data["data"]["percentages"]
          }
      else if (data["infected_status"] === "infected"){
        let infected_data = data["data"];
          ref.$refs.cpuChartHealthy.updateOptions({
                xaxis: {
                  categories: infected_data["timestamps"], //ie ["a","b","c","d"]
                  tickAmount: 15,
                },
            series:[{
            name: 'healthy',
            data: ref.healthy_cpu_data //ie [1,2,3,4]
          },{
                  name:"infected",
                  data:infected_data["percentages"]
            },],

                colors:["#207f10", "#d31313"],
          })
        ref.infected_cpu_data = data["data"]["percentages"]
          }
      });

  },
  data: function() {
    return {
      background:"#000000",
      infected_cpu_data:[],
      healthy_cpu_data:[],
      chartOptions: {
        chart: {
                      foreColor: '#ffffff',
              animations: {
                enabled: false,

              },
              toolbar: {
                show: false
              },
              zoom: {
                enabled: false
              },
            },
        xaxis: {

          categories: [],
        },
      },
      series: [
        {
          name: "healthy",
          data: [],
        },
      ],

    };
  },
}
</script>

<style scoped>

</style>