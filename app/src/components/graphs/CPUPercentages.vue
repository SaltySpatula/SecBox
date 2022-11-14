<template>
  <v-card class="bg-black" style="margin:10px">
    <v-card-title  style="align:center">CPU Usage</v-card-title>
      <apexchart
          v-if="this.healthy_cpu_data && this.infected_cpu_data"
      type="area"
      ref="cpuChartHealthy"
      :options="chartOptions"
      :series="series"
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
        ref.healthy_cpu_data = data["data"]
          }
      else if (data["infected_status"] === "infected"){
        ref.infected_cpu_data = data["data"]
          }
                ref.$refs.cpuChartHealthy.updateOptions({
                xaxis: {
                  categories: data["data"]["timestamps"], //ie ["a","b","c","d"]
                  tickAmount: 15,
                },
            series:[{
            name: 'healthy',
            data: ref.healthy_cpu_data["percentages"] //ie [1,2,3,4]
          },{
                  name:"infected",
                  data:ref.infected_cpu_data["percentages"]
            },],

                colors:["#d917bf", "#13d3b6"],
          })
      });

  },
  data: function() {
    return {
      infected_cpu_data:[],
      healthy_cpu_data:[],
      chartOptions: {
         tooltip: {
           enabled:false
         },
        dataLabels: {
          enabled: false
        },
        chart: {
           type: 'area',
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
        colors:["#d917bf", "#13d3b6"],
        xaxis: {

          categories: [],
        },
        yaxis:{
           labels: {
             formatter: (value) => {
               return value.toFixed(2) + "%"
             },
           }
        }
      },
      series: [{
          data: []
        }]

    };
  },
}
</script>

<style scoped>

</style>