<template>
  <div>
      <apexchart
      type="line"
      ref="cpuChart"
      :options="chartOptions"
      :series="series"
      :background="background"
    ></apexchart>{{this.healthy}}
    </div>
</template>

<script>

export default {
  name: "CPUPercentages",
  props:{
    socket:Object,

  },
  created() {
    this.healthy = {"timestamps":[],"percentages":[]}
    let ref = this;
    this.socket.on("cpu_percentages_graph", function (data){
      if (data["infected_status"] === "healthy"){
            let healthy_data = data["data"];
            ref.$refs.cpuChart.updateSeries([{
      name: 'Series 1',
      data: healthy_data["percentages"] //ie [1,2,3,4]
          }])

          ref.$refs.cpuChart.updateOptions({
                xaxis: {
                  categories: healthy_data["timestamps"] //ie ["a","b","c","d"]
                }
          })
          }
      else if (data["infected_status"] === "infected"){
            ref.infected = data["data"];
          }

      });

  },
  data: function() {
    return {
      background:"#000000",
      infected:{},
      chartOptions: {
        chart: {
              animations: {
                enabled: true,
                easing: 'linear',
                dynamicAnimation: {
                  speed: 1000
                }
              },
              toolbar: {
                show: false
              },
              zoom: {
                enabled: false
              }
            },
        xaxis: {
          categories: [],
        },
        colors:['#207f10'],

      },

      series: [
        {
          name: "series-1",
          data: [],
        },
      ],

    };
  },
}
</script>

<style scoped>

</style>