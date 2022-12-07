<template>
    <apexchart
        ref="RWGraph"
        :options="chartOptions"
        :series="series"
        :height="300"
    ></apexchart>
</template>

<script>
export default {
  name: "RWGraph",
  props: {graph_title: String, data: Object,},
  created() {
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