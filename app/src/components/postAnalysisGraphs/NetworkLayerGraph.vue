<template>
  <apexchart
      type="radar"
      ref="NetworkLayerGraph"
      :options="chartOptions"
      :series="series"
      :height="300"
  ></apexchart>
</template>

<script>
export default {
  name: "NetworkLayerGraph",
  props: {graph_title: String, data: Object, colors: Object},
  created() {
  },
  data: function () {
    let ref = this
    return {
      series: ref.data["data"],
      chartOptions: {
        plotOptions: {
          radar: {
            size: 100,
            polygons: {
              strokeColors: "#595454",
              connectorColors: "#595454"
            }
          }
        },

        chart: {
          height: 350,
          type: 'radar',
          dropShadow: {
            enabled: true,
            blur: 1,
            left: 1,
            top: 1
          }
        },
        dataLabels: {

          formatter: function (val) {
            return String(Math.round(val * 100)) + "%"
          },
          enabled: true,
          background: {
            enabled: true,
            borderRadius: 2,
          }
        },

        yaxis: {
          tickAmount: 4,
          labels: {
            formatter: function () {
              return ""
            }
          }
        },
        title: {
          text: 'Comparison of activity in network layers'
        },
        stroke: {
          width: 2,
        },
        fill: {
          opacity: 0.1,
        },
        markers: {
          size: 0,
        },
        xaxis: {
          categories: ref.data["labels"],
          labels: {
            show: true,
            style: {
              colors: ["#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000"],
            },
          }
        },
        colors: ['#00E396', '#ff0084']
      },


    }

  },
  methods: {},
}
</script>

<style scoped>

</style>