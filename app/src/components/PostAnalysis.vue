<template>
  <v-navigation-drawer
      floating
      permanent
      width="400"
      class="bg-deep-purple-lighten-1"
  >
    <v-list v-model:opened="open"
            v-for="graph_group in this.graph_data"
            :key="graph_group.title"
    >
      <v-list-group :value="graph_group.title">
        <template v-slot:activator="{ props }">
          <v-list-item
              v-bind="props"
              :prepend-icon="graph_group.icon"
              :title="graph_group.title"
          ></v-list-item>
        </template>
        <v-list-item
            v-for="item in graph_group.graphs"
            :key="item.title"
            :title="item.title"
            :prepend-icon="item.icon"
            :value="item.title"
            :disabled="item.disabled"
            @click="createGraph(item)"
        ></v-list-item>
      </v-list-group>
    </v-list>
    <v-container fluid style="position: absolute;bottom:0;">
      <MalwareCard
          malwareName="test"
      ></MalwareCard>
      <v-btn
          style="margin-top: 1em"
          block
          large
          color="primary"
          dark
          @click="createReport()"
      >
        <v-icon>
          mdi-content-save
        </v-icon>
        Save & Exit
      </v-btn>

      <v-btn style="margin-top: 1em"
             block
             color="red"
             dark
             tile
      >
        <v-icon>
          mdi-delete
        </v-icon>
        Delete & Quit
      </v-btn>

    </v-container>
  </v-navigation-drawer>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="4" v-for="graph in selected_graphs" v-bind:key="graph.title">
        <v-card class="bg-deep-purple-lighten-5">
        <v-card-title>{{ graph.title }}</v-card-title>
          <PAGraphWrapper :socket="this.socket" :graph_title="graph.title"/>
          <v-card-actions>
            <div class="my-2">
              <v-btn class="bg-red" @click="deleteGraph(graph)">
                <v-icon>
                  mdi-delete
                </v-icon>
              </v-btn>
            </div>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MalwareCard from "@/components/MalwareCard";
import router from "@/router";
import io from "socket.io-client";
import PAGraphWrapper from "@/components/PAGraphWrapper";

export default {
  name: "PostAnalysis.vue",
  components: {MalwareCard, PAGraphWrapper},
  created() {
    // joining room
    this.socket = io("ws://localhost:5000/analysis");

    this.socket.emit('join analysis room', {"room": this.$route.params.id}, function () {
      // console.log("joined ", data);
    });
  },
  data: () => ({
    open: [],
    selected_graphs: [],
    graph_data: {
      "network_graphs": {
        "title": "Network",
        "icon": "mdi-wan",
        "graphs": [
          {"title": 'Network Layers', "icon": 'mdi-nas', "disabled": false},
          {"title": 'IP addresses', "icon": 'mdi-map-marker', "disabled": false},
        ]
      },
      "syscall_graphs": {
        "title": "System Calls",
        "icon": "mdi-console-network",
        "graphs": [
          {"title": 'Rule violations', "icon": 'mdi-alert-octagon', "disabled": false,},
          {"title": 'Direct Comparison', "icon": 'mdi-ab-testing', "disabled": false},
        ]
      },
      "performance_graphs": {
        "title": "Performance",
        "icon": "mdi-poll",
        "graphs": [
          {"title": 'CPU Usage', "icon": 'mdi-cpu-64-bit', "disabled": false},
          {"title": 'RAM', "icon": 'mdi-memory', "disabled": false},
        ]
      },
    }
  }),
  methods: {
    createGraph: function (graph) {
      this.selected_graphs.push(graph)
      graph.disabled = true;
    },
    deleteGraph: function (graph) {
      graph.disabled = false;
      for (let i = 0; i < this.selected_graphs.length; i++) {
        if (graph.title === this.selected_graphs[i].title) {
          this.selected_graphs.splice(i, 1)
        }
      }
    },
    createReport: function () {
      const current_id = this.$route.params.id
      router.replace({path: '/report/' + current_id},)
    },
  }
}
</script>

<style scoped>
.v-list-item-title {
  font-size: 1em
}
</style>