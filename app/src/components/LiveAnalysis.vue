<template>
<v-container fluid>
      <v-row align="center" class="ma-2">
        <v-col cols="12" md="12">
          <v-card class="bg-deep-purple-accent-1">
            <v-card-title style="font-family:'Courier New'">Live Analysis</v-card-title>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem">
              <button v-on:click="sendMessage('hello')">Send Message</button>
          </v-card>
        </v-col>
                <v-col cols="12" md="6">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem">

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
import io from "socket.io-client";
export default {
  name: "LiveAnalysis",
  data: () =>({
    socket:null
      }),
  created() {
    // testing connection
    this.socket = io("ws://localhost:5000");
    this.socket.on('receive data', function(data){
    console.log(data);   //should output 'hello world'
});

  },
  methods:{
    sendMessage: function(message){
      //sending to server
       this.socket.emit('my event', { data: message });
  }}
}
</script>

<style scoped></style>