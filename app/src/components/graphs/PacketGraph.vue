<template>
  <v-card class="bg-black" style="margin:10px">
    <v-card-title style="align:center">Packets Transmitted</v-card-title>
    <apexchart
        v-if="this.packets_sent && this.packets_received"
        ref="packetGraph"
        :options="chartOptions"
        :series="series"
        :height="300"
    ></apexchart>
  </v-card>
</template>

<script>

export default {
  name: "PacketGraph",
  props: {
    socket: Object,
  },
  created() {
    let ref = this
    this.socket.on("packet_graph", function (data) {
      if (data["infected_status"] === "healthy") {
        let healthy_data = data["data"]["packets"][0];
        ref.packets_received[1] = healthy_data["received_packages"]
        ref.packets_sent[1] = healthy_data["transmitted_packages"]
      } else if (data["infected_status"] === "infected") {
        let healthy_data = data["data"]["packets"][0];
        ref.packets_received[0] = healthy_data["received_packages"]
        ref.packets_sent[0] = healthy_data["transmitted_packages"]
      }
      ref.$refs.packetGraph.updateSeries(
          [{
            name: 'Packets sent',
            data: ref.packets_sent
          }, {
            name: 'Packets received',
            data: ref.packets_received
          }]
      )
    });


  },
  data: function () {
    return {
      packets_received: [],
      packets_sent: [],
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
          categories: ['infected', 'healthy'],
        },
        colors: ["#2fc964", "#644db4"]
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