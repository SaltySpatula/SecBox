<template>
  <apexchart
      type="area"
      ref="CPUMemoryGraph"
      :options="chartOptions"
      :series="series"
      :height="300"
  ></apexchart>
</template>

<script>
export default {
  name: "CPUMemoryGraph",
  props: {socket: Object, graph_title: String, data: Object, },
  created() {

  },
  data: function () {
    return {
      loading: true,
      series: [{
        name: 'Healthy Data',
        data: this.data["healthy"]
      }, {
        name: 'Infected Data',
        data: this.data["infected"]
      }],
      chartOptions: {
        chart: {
          zoom: {
            autoScaleYaxis: true
          },
          type: "area",

          height: 300,
          foreColor: "#111111",
          stacked: false,
          dropShadow: {
            enabled: true,
            enabledSeries: [0],
            top: -2,
            left: 2,
            blur: 5,
            opacity: 0.06
          },
        },
        xaxis: {
          type: "datetime",
          min: Math.min(this.data["healthy"][0][0], this.data["infected"][0][0]),
          labels: {
            datetimeFormatter: {
              year: 'yyyy',
              month: "MMM 'yy",
              day: 'dd MMM',
              hour: 'HH:mm',
            },
          },
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: true
          }
        },
        colors: ['#00E396', '#ff0084'],
        stroke: {
          curve: "smooth",
          width: 3
        },
        dataLabels: {
          enabled: false
        },
        yaxis: {
          labels: {
            formatter: (value) => {
              return value.toFixed(2) + "%"
            },
          },
          tooltip: {
            enabled: false
          }
        },
        grid: {
          padding: {
            left: -5,
            right: 5
          }
        },
        tooltip: {
          shared: true,
          x: {
            format: "dd MMM yyyy hh:mm:ss"
          },
        },
        legend: {
          position: 'bottom',
          horizontalAlign: 'left'
        },


      }

    }
  },
  methods:{
/*
        beforeZoom : (e, {xaxis}) => {
            let maindifference = Math.min(this.data["healthy"][0][0], this.data["infected"][0][0]) - Math.max(this.data["healthy"][(this.data["healthy"].length()-1)][0], this.data["infected"][this.data["infected"].length()-1][0])
            let zoomdifference =   xaxis.max - xaxis.min ;
            if( zoomdifference > maindifference )
            return  {
                xaxis: {
                    min: Math.min(this.data["healthy"][0][0], this.data["infected"][0][0]),
                    max: Math.max(this.data["healthy"][(this.data["healthy"].length()-1)][0], this.data["infected"][this.data["infected"].length()-1][0])
                }
            };
            else {
                return {
                    // keep on zooming
                    xaxis: {
                        min: xaxis.min,
                        max: xaxis.max
                    }
                }
            }
        }
*/
  },
}
</script>

<style scoped>

</style>