<template>
    <v-overlay :model-value="loading" class="align-center justify-center">
      <v-progress-circular
        indeterminate
        size="64"
        color="primary"
        persistent
        opacity="0.75"
      ></v-progress-circular>
    </v-overlay>
<v-navigation-drawer
        floating
        permanent
        width="300"
        class="bg-deep-purple-lighten-1"
      >
  <v-btn
        style="margin-top: 1em"
                block
              large
              color="primary"
              dark
        @click="this.saveGraph()"
            >
              <v-icon              >
                mdi-content-save
              </v-icon>
              Save & Exit
       </v-btn>
</v-navigation-drawer>
  <v-container align="left" class="bg-deep-purple-lighten-4" >
    <v-text-field
            v-model="this.title"
            label="Enter a title"
            filled
            style="font-size:2em;max-height:4em;"
          ></v-text-field>
    <v-row v-if="this.selected_graphs">
      <v-col cols="12" md="6" v-for="graph in this.selected_graphs" v-bind:key="graph.title">
        <v-card class="bg-deep-purple-lighten-5">
        <v-card-title>{{ graph.title }}</v-card-title>
          <PAGraphWrapper :render_healthy="this.render_healthy" :render_both="true" :socket="this.socket_analysis" :graph_title="graph.title" :graph_get="graph.get"/>
           <v-textarea
          v-model="graph.comment"/>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import io from "socket.io-client";
import PAGraphWrapper from "@/components/PAGraphWrapper";

export default {
  name: "ReportPage",
  components:{PAGraphWrapper},
  created(){
    this.socket = io("ws://localhost:5000/report");
    const ref = this
    this.socket.emit('get report', {"ID": this.$route.params.id})
    this.socket.on("send report", function (data){
          data = JSON.parse(data)
          ref.selected_graphs = data["selected_graphs"]
          ref.title = data["title"]
          ref.loading = false
        })

    this.socket_analysis = io("ws://localhost:5000/analysis");
    this.socket_analysis.emit('join analysis room', {"room": this.$route.params.id}, function () {});
  },
  data: () => ({
      render_healthy : true,
    loading : true,
    selected_graphs : [],
    title:""
  }),
  methods: {
    getDate:function (){
      const date = new Date();

      let day = date.getDate();
      let month = date.getMonth() + 1;
      let year = date.getFullYear();
      console.log(day, month, year)
    },
    saveGraph:function(){
      //console.log("updating", this.title, this.selected_graphs)
      this.socket.emit("update report", {ID: this.$route.params.id, title:this.title, selected_graphs:this.selected_graphs})
    }
  }

}
</script>

<style scoped>
.v-text-field input {
  font-size:1.2em
}
</style>