<template>
      <v-navigation-drawer
        floating
        permanent
        width="400"
        class="bg-deep-purple-darken-2"
      ><v-list v-model:opened="open">
      <v-list-group value="System Calls">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-console-network"
            title="System Calls"
          ></v-list-item>
        </template>
          <v-list-item
            v-for="item in syscall_graphs"
            :key="item.title"
            :title="item.title"
            :prepend-icon="item.icon"
            :value="item.title"
            :disabled="item.disabled"
            @click="createGraph(item.title, syscall_graphs)"
          ></v-list-item>
      </v-list-group>
    </v-list>
        <v-list v-model:opened="open">
      <v-list-group value="Network">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-wan"
            title="Network"
          ></v-list-item>
        </template>
          <v-list-item
            v-for="item in network_graphs"
            :key="item.title"
            :title="item.title"
            :prepend-icon="item.icon"
            :value="item.title"
            :disabled="item.disabled"
            @click="createGraph(item.title, network_graphs)"
          ></v-list-item>
      </v-list-group>
        </v-list>
        <v-list v-model:opened="open">
        <v-list-group value="Performance">
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            prepend-icon="mdi-poll"
            title="Performance"
          ></v-list-item>
        </template>
          <v-list-item
            v-for="item in performance_graphs"
            :key="item.title"
            :title="item.title"
            :prepend-icon="item.icon"
            :value="item.title"
            :disabled="item.disabled"
            @click="createGraph(item.title, performance_graphs)"
          ></v-list-item>
      </v-list-group>
        </v-list>
      </v-navigation-drawer>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="4" v-for="title in selected_graphs">
        <v-card  class="bg-deep-purple-accent-1">
          <v-card-title >{{ title }}</v-card-title>
          <v-card-actions>
            <div class="my-2">
            <v-btn class="bg-red" @click="deleteGraph(item.title, performance_graphs)">
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
export default {
  name: "PostAnalysis.vue",
  data: () => ({
      open: [],
      selected_graphs:[],
      network_graphs: [
        {"title":'Packet Ratio', "icon":'mdi-nas', "disabled":false},
        {"title":'IP addresses',"icon":'mdi-map-marker', "disabled":false},
      ],
      syscall_graphs: [
        {"title":'Rule violations', "icon":'mdi-alert-octagon', "disabled":false},
        {"title":'Direct Comparison',"icon": 'mdi-ab-testing', "disabled":false},
      ],
      performance_graphs: [
        {"title":'CPU Memory',"icon": 'mdi-cpu-64-bit', "disabled":false},
        {"title":'RAM', "icon":'mdi-memory', "disabled":false},
      ],
    }),
  methods:{
    createGraph: function(graphTitle, source){
      this.selected_graphs.push(graphTitle)
      for (const g of source){
        if (g.title === graphTitle){
          g.disabled = true
        }
      }
    },
    deleteGraph: function(graphTitle, source){
      this.selected_graphs.push(graphTitle)
      for (const g of source){
        if (g.title === graphTitle){
          g.disabled = true
        }
      }
    },
  }
}
</script>

<style scoped>
.v-list-item-title{
  font-size:1em
}
</style>