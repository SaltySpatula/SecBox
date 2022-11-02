<template>
<v-container fluid>
      <v-row align="center" class="ma-2 bg-deep-purple-accent-1" style="margin:0">
        <v-col cols="12" md="8">
            <h1 style="font-family:'Courier New';font-size:2em">Live Analysis</h1>
        </v-col>
        <v-col cols="12" md="2">
            <v-btn
              block
              color="red"
              dark
              tile
            >
              <v-icon              >
                mdi-delete
              </v-icon>
              Delete & Quit
            </v-btn>
        </v-col>
        <v-col cols="12" md="2">
            <v-btn
                block
              large
              color="primary"
              dark
              @click="postAnalyze"
            >
              <v-icon              >
                mdi-content-save
              </v-icon>
              Save & Exit
            </v-btn>
        </v-col>
        </v-row>
        <v-row style="margin:0">
        <v-col cols="12" md="3">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem">
              <CPUPercentages :socket="this.socket"/>
          </v-card>
        </v-col>
        <v-col cols="12" md="6"  >
          <v-card class="pa-0 bg-deep-purple-accent-1">
          <LiveTerminal :current_id="this.$route.params.id" :socket="this.socket"></LiveTerminal>
            </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem">

          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
import LiveTerminal from "@/components/LiveTerminal";
import router from  "@/router/index";
import CPUPercentages from "@/components/graphs/CPUPercentages";
import io from "socket.io-client";
export default {
  name: "LiveAnalysis",
  components: {LiveTerminal, CPUPercentages},
  data: () => ({
    healthy_cpu_data:[],
    infected_cpu_data:[]
  }),
  props:{

  },
  created(){
        // joining room
    this.socket = io("ws://localhost:5000/live");

    this.socket.emit('join room', {"room":this.$route.params.id}, function(){
        // console.log("joined ", data);
    });


  },
  methods:{
  postAnalyze:function(){
     const current_id = this.$route.params.id
     router.replace({ path: '/analysis/' +current_id}, )
  },
  },

}
</script>

<style scoped>
.v-card-title{
    font-family: "Courier New";
    font-weight: bold;
}
</style>