<template>
  <v-card class="bg-black" style="margin:10px">
    <v-card-title style="align:center">Protocol Comparison</v-card-title>
    <apexchart
        ref="RWGraph"
        :options="chartOptions"
        :series="series"
        :height="300"
    ></apexchart>
  </v-card>
</template>

<script>
export default {
  name: "RWGraph",
  props: {graph_title: String, data: Object,},
  created() {
    console.log(this.data)
  },
  data: function () {
    return {
      chartOptions: {
        tooltip: {
          enabled: false
        },
        chart: {
          type: 'bar',
          stacked: true,
          foreColor: '#ffffff',
          toolbar: {
            show: false
          },
        },
        xaxis: {
          categories: ['healthy', 'infected'],
        },
        colors: ["#2fc964", "#644db4", "#d09c3f"],
        plotOptions: {
          bar: {
            horizontal: true,
            dataLabels: {
              total: {
                enabled: true,
                offsetX: 0,
                style: {
                  fontSize: '13px',
                  fontWeight: 900
                }
              }
            }
          },
        },
      },
      series: [
    {
      name: 'Reads',
      data: [this.data.healthy.graph.reads, this.data.infected.graph.reads]
    },
      {
      name: 'Writes',
      data: [this.data.healthy.graph.writes, this.data.infected.graph.writes]
    }]
    };
  },
}
</script>

<style scoped>

</style>