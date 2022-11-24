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
  name: "ProtocolGraph",
  props: {
    socket: Object,
  },
  created() {
    let ref = this
    const id = ref.$route.params.id
    this.socket.on("layer_counts_graph", function (data) {

      const hd = data[id]["healthy"]["graph"]
      const infd = data[id]["infected"]["graph"]

      const updated_series = []

      for (const [key, value] of Object.entries(hd)) {
        if (key === "TCP" || key === "UDP" || key === "SCTP"){
          updated_series.push({name: key, data:[value, infd[key]]})
          }
      }
      ref.$refs.RWGraph.updateSeries(updated_series)
    });
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
      name: 'TCP',
      data: [0, 0]
    },
      {
      name: 'UDP',
      data: [0, 0]
    }]
    };
  },
}
</script>

<style scoped>

</style>