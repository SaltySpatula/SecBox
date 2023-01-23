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
      v-else-if="graph_title === 'Read Write Counts'"
      :graph_title="graph_title"
      :data="this.data"

  ></ReadWriteGraph>
    <RAMGraph
      v-else-if="graph_title === 'RAM'"
      :graph_title="graph_title"
      :data="this.data"
  >
  </RAMGraph>
  <DirectoryGraph v-else-if="graph_title === 'Directory Graph'"
                  :graph_title="graph_title"
      :data="this.data"
      :render_healthy="this.render_healthy"
                  :render_both="this.render_both"
  >
  </DirectoryGraph>

</template>

<script>
import CPUMemoryGraph from "@/components/postAnalysisGraphs/CPUMemoryGraph";
import NetworkLayerGraph from "@/components/postAnalysisGraphs/NetworkLayerGraph";
import IPFrequencyGraph from "@/components/postAnalysisGraphs/IPFrequencyGraph";
import ReadWriteGraph from "@/components/postAnalysisGraphs/ReadWriteGraph";
import DirectoryGraph from "@/components/postAnalysisGraphs/DirectoryGraph";
import RAMGraph from "@/components/postAnalysisGraphs/RAMGraph";
export default {
  name: "PAGraphWrapper",
  components:{CPUMemoryGraph, NetworkLayerGraph, IPFrequencyGraph, ReadWriteGraph, DirectoryGraph, RAMGraph},
  props:{render_healthy:Boolean, render_both:Boolean, socket: Object,graph_get:String, graph_title:String},
  created() {

    let ref = this
    this.socket.emit(this.graph_get, {
      "ID":this.$route.params.id
    })

    this.socket.on(this.graph_title, function (data) {
        let parsed_data = JSON.parse(data)
        if (ref.graph_title === "CPU Usage"){

          let healthy_data = ref.prepare_cpu_data(parsed_data["healthy"]["graph"], "cpu_percentage")
          let infected_data = ref.prepare_cpu_data(parsed_data["infected"]["graph"], "cpu_percentage")
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
        else if (ref.graph_title === "Directory Graph"){
          let healthy_data = ref.process_data(parsed_data["healthy"]["graph"])
          let infected_data = ref.process_data(parsed_data["infected"]["graph"])

          ref.data={
            "healthy" : healthy_data,
            "infected" : infected_data
          }
        }
        else if (ref.graph_title === "RAM"){
          let healthy_data = ref.prepare_cpu_data(parsed_data["healthy"]["graph"], "ram_usage")
          let infected_data = ref.prepare_cpu_data(parsed_data["infected"]["graph"], "ram_usage")
          ref.data={
            "healthy" : healthy_data,
            "infected" : infected_data
          }
        }
        // change flag
        ref.loading = false
    })
  },
  methods:{
    prepare_cpu_data: function (new_data, key) {
      const a = []
      for (let i = 0; i < new_data.length; i++) {
            const time = new Date(new_data[i]["timestamp"])

            const tuple = [time, new_data[i][key]]
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
        for (const [key, value] of Object.entries(infected)) {
          if (!healthy[key]){
            healthy[key] = 0
          }
          let combined = value + healthy[key]
          let r1 = value/combined
          let r2 = healthy[key]/combined
          healthy_series.push(r2)
          infected_series.push(r1)
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
  },
    iterate_over_sd: function (key, obj,  labels, parents, values) {
      const sd = obj["sd"]
      if (sd.length > 0){
        for (let i = 0; i < sd.length; i++) {
          let l = Object.keys(sd[i])[0]
          let new_obj = sd[i][l]
          let p = key
          let v = new_obj["n"]
          labels.push(l)
          parents.push(p)
          values.push(v)
          this.iterate_over_sd(l, new_obj, labels, parents, values)
        }
      }

      return {labels:labels, parents:parents, values:values}
    },
    process_data: function (graph_data) {
      const labels = ["/"]
      const parents = [""]
      const values = [0]
      const to_iterate = graph_data["/"]
      let data = this.iterate_over_sd("/", to_iterate, labels, parents, values)
      data["root_value"] = graph_data["/"]["n"]
      return data
    },
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