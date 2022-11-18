<template>
  <v-card class="bg-black" style="margin:10px">
    <v-card-title style="align:center">Read Write Count</v-card-title>
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
  name: "ReadWriteGraph",
  props:{
    socket:Object,
  },
  created() {
    //let ref = this
    this.socket.on("reads_vs_writes_graph", function (data){
      console.log(data)

      /* {'healthy': {'graph': {'reads': 0, 'writes': 0}}, 'infected': {'graph': {'reads': 0, 'writes': 0}}}}
      let updated_data = [
        {
          name: 'healthy',
          data: [data["healthy"]["reads"], data["healthy"]["writes"]]
      },
        {
          name: 'infected',
          data: [data["infected"]["reads"], data["infected"]["writes"]]
      }
      ]*/
      //ref.$refs.RWGraph.updateSeries(updated_data)
      });
  },
  data: function() {
    return {
      chartOptions: {
            tooltip: {
           enabled:false
         },
        chart: {
        type: 'bar',
          stacked:true,
          foreColor: '#ffffff',
          toolbar: {
                show: false
              },
      },
        xaxis: {
          categories: ['infected', 'healthy'],
        },
        colors:["#2fc964", "#644db4"],
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
        series: [{
          name: 'healthy',
          data: [0, 0 ]
        }, {
          name: 'infected',
          data: [0, 0]
        }]
    };
  },
}
</script>

<style scoped>

</style>