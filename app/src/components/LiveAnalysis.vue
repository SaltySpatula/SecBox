<template>
  <v-container fluid>

    <!--v-row align="center" class="ma-2 bg-deep-purple-accent-1" style="margin:0">
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
      </v-row-->
    <v-row style="margin:0">
      <v-col cols="12" md="3">
        <v-card class="bg-deep-purple-lighten-3" style="overflow-y: auto">
          <CPUPercentages :socket="this.socket"/>
          <PacketGraph :socket="this.socket"/>
          <v-btn
              block
              color="red darken-4"
              dark
              min-height="5em"
              style="position:relative;bottom:0"
            >
              <v-icon              >
                mdi-delete
              </v-icon>
              Delete & Quit
            </v-btn>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card class="pa-0 bg-deep-purple-lighten-3">
          <LiveTerminal :combined_cli="this.combined_cli" :current_id="this.$route.params.id"
                        :socket="this.socket"></LiveTerminal>
          <v-col align="center">
            <v-btn
                icon
                color="black"
                @click="this.combined_cli = !this.combined_cli"
            >
              <v-icon>mdi-cached</v-icon>
            </v-btn>

          </v-col>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="bg-deep-purple-lighten-3" style="overflow-y: auto; height:50rem">
          <PIDCountGraph :socket="this.socket"></PIDCountGraph>
          <PIDCountGraph :socket="this.socket"></PIDCountGraph>
          <v-btn
                block
              large
              color="deep-purple darken-4"
              dark
                min-height="5em"
                style="position:absolute;bottom:0"
              @click="postAnalyze"
            >
              <v-icon              >
                mdi-content-save
              </v-icon>
              Save & Exit
            </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LiveTerminal from "@/components/LiveTerminal";
import router from "@/router/index";
import CPUPercentages from "@/components/graphs/CPUPercentages";
import PacketGraph from "@/components/graphs/PacketGraph";
import PIDCountGraph from "@/components/graphs/PIDCountGraph";
import io from "socket.io-client";

export default {
  name: "LiveAnalysis",
  components: {LiveTerminal, PacketGraph, PIDCountGraph, CPUPercentages: CPUPercentages},
  data: () => ({
    combined_cli: true,
  }),
  props: {},
  created() {
    // joining room
    this.socket = io("ws://localhost:5000/live");

    this.socket.emit('join room', {"room": this.$route.params.id}, function () {
      // console.log("joined ", data);
    });


  },
  methods: {
    postAnalyze: function () {
      this.socket.emit("stop request", {"ID":this.$route.params.id})
      const current_id = this.$route.params.id
      router.replace({path: '/analysis/' + current_id})
    },
  },

}
</script>

<style scoped>
.v-card-title {
  font-family: "Courier New";
  font-weight: bold;
}
</style>