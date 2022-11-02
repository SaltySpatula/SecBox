<template>
  <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
  <div>
    {{this.healthy}}
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts"

export default {
  name: "CPUPercentages",
  props:{
    socket:Object
  },
  components: {
    apexchart: VueApexCharts,
  },

  created() {
    let ref = this
    this.socket.on("cpu_percentages_graph", function (data){



      console.log(data)
      if (data["infected_status"] === "healthy"){
            ref.healthy = data["data"];
          }
      if (data["infected_status"] === "infected"){
            ref.infected = data["data"];
          }
      console.log(ref.infected, ref.healthy)


      });
  },
  data: () => ({
    infected:[],
    healthy:[],
      chartOptions: {
        chart: {
          height: 350,
          type: 'line',
          zoom: {
            enabled: false
          }
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        }
      }
      ,
      series: [{
        name: "Desktops",
        data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
      }]


    })

}
</script>
import ApexCharts from "apexcharts"

<style scoped>

</style>