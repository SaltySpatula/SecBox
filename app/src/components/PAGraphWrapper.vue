<template>

  <div v-if="this.loading"
            style="text-align: center">
  <v-progress-circular

            indeterminate
            color="primary"
    ></v-progress-circular></div>
  <CPUMemoryGraph v-else-if="graph_title === 'CPU Usage'"
                  :graph_title="graph_title"
                  :data="this.data"
  ></CPUMemoryGraph>
    <NetworkLayerGraph v-else-if="graph_title === 'Network Layers'"
                  :graph_title="graph_title"
                  :data="this.data"
  ></NetworkLayerGraph>
  <IPFrequencyGraph v-else-if="graph_title === 'IP Addresses'"
                  :graph_title="graph_title"
                  :data="this.data">

  </IPFrequencyGraph>
  <ReadWriteGraph
      v-else-if="graph_title === 'IP Addresses'"
      :graph_title="graph_title"
      :data="this.data"
  ></ReadWriteGraph>
</template>

<script>
import CPUMemoryGraph from "@/components/postAnalysisGraphs/CPUMemoryGraph";
import NetworkLayerGraph from "@/components/postAnalysisGraphs/NetworkLayerGraph";
import IPFrequencyGraph from "@/components/postAnalysisGraphs/IPFrequencyGraph";
import ReadWriteGraph from "@/components/postAnalysisGraphs/ReadWriteGraph";
export default {
  name: "PAGraphWrapper",
  components:{CPUMemoryGraph, NetworkLayerGraph, IPFrequencyGraph, ReadWriteGraph},
  props:{socket: Object,graph_get:String, graph_title:String},
  created() {

    let ref = this
    this.socket.emit(this.graph_get, {
      "ID":this.$route.params.id
    })

    this.socket.on(this.graph_title, function (data) {
        let parsed_data = JSON.parse(data)
        if (ref.graph_title === "CPU Usage"){

          let healthy_data = ref.prepare_cpu_data(parsed_data["healthy"]["graph"])
          let infected_data = ref.prepare_cpu_data(parsed_data["infected"]["graph"])
          ref.data={
            "healthy" : healthy_data,
            "infected" : infected_data
          }
        }
        else if (ref.graph_title === "Network Layers"){
          ref.data = ref.prepare_network_layer_data(parsed_data)
        }
        else if (ref.graph_title === "IP Addresses"){
          ref.data = parsed_data
        }
        else if (ref.graph_title === "Read Write Counts"){
          ref.data = parsed_data
        }
        // change flag
        ref.loading = false
    })
  },
  methods:{
    prepare_cpu_data: function (new_data) {
      const a = []
      for (let i = 0; i < new_data.length; i++) {
            const time = new Date(new_data[i]["timestamp"])
            const tuple = [time, new_data[i]["cpu_percentage"]]
            a.push(tuple)
        }
      return a
    },
    prepare_network_layer_data: function (data) {

        const healthy = data["healthy"]["graph"]
        const infected = data["infected"]["graph"]
        const healthy_series = []
        const infected_series = []
        const labels = []
        for (const [key, value] of Object.entries(healthy)) {
          let combined = value + infected[key]
          let r1 = value/combined
          let r2 = infected[key]/combined
          healthy_series.push(r1)
          infected_series.push(r2)
          let key_string = String(key)
          let length = 10
          let trimmedString = key_string.length > length ? key_string.substring(0, length - 3) + "..." : key_string.substring(0, length)
          labels.push(trimmedString)
      }

      return {"labels":labels, "data":[{
          name: "healthy",
          data: healthy_series

      },
        {
          name: "infected",
          data: infected_series
        }]}
  }
  },
  data:function(){
    return{
      data : {},
      loading:true
    }
  }

}
</script>

<style scoped>

</style>