<template>
  <div v-if="this.loading"
            style="text-align: center">
  <v-progress-circular

            indeterminate
            color="primary"
    ></v-progress-circular></div>
  <CPUMemoryGraph v-else-if="graph_title === 'CPU Memory'"

                  :socket="this.socket"
                  :graph_title="graph_title"
                  :data="this.data"
  ></CPUMemoryGraph>
</template>

<script>
import CPUMemoryGraph from "@/components/postAnalysisGraphs/CPUMemoryGraph";

export default {
  name: "PAGraphWrapper",
  components:{CPUMemoryGraph},
  props:{socket: Object, graph_title:String},
  created() {

    console.log("get " + this.graph_title)
    let ref = this
    this.socket.emit("get " + this.graph_title, {
      "ID":this.$route.params.id
    })
    this.socket.on(this.graph_title, function (data) {
        let parsed_data = JSON.parse(data)

        if (ref.graph_title === "CPU Memory"){
          let healthy_data = ref.prepare_cpu_data(parsed_data["data"]["healthy"]["graph"])
          let infected_data = ref.prepare_cpu_data(parsed_data["data"]["infected"]["graph"])
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
    prepare_cpu_data: function (new_data) {
      const a = []
      for (let i = 0; i < new_data.length; i++) {
            const time = new Date(new_data[i]["timestamp"])
            const tuple = [time, new_data[i]["cpu_percentage"]]
            a.push(tuple)
        }
      return a
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