<template>
<v-container fluid>
      <v-row align="center" class="ma-2">
        <v-col cols="12" md="12">
          <v-card class="bg-deep-purple-accent-1">
            <v-card-title style="font-family:'Courier New';font-size:2em">Live Analysis</v-card-title>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem">
              <button v-on:click="sendMessage('hello')">Send Message</button>
          </v-card>
        </v-col>
        <v-col cols="12" md="6" class="pa-0 bg-deep-purple-accent-1" >
          <LiveTerminal></LiveTerminal>
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
export default {
  name: "LiveAnalysis",
  components: {LiveTerminal},
}
</script>

<style scoped>
.v-card-title{
    font-family: "Courier New";
    font-weight: bold;
}

</style>