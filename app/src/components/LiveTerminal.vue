<template>
 <v-container fluid class="ma-0 pa-0">
            <v-row align="center" class="ma-2">
              <TerminalInterface ref="infected_terminal" type="infected" color="#13d3b6" :lines=this.infected_lines></TerminalInterface>
              <TerminalInterface ref="healthy_terminal" type="healthy" color="#d917bf" :lines=this.clean_lines></TerminalInterface>
              <v-col v-if="this.combined_cli" class="pa-1 " cols="12" md="12">
                <v-text-field
                              v-if="this.combined_cli"
                              ref="CLI_text_field"
                              style="border:1px solid white;font-family:'Courier New'"
                              class="bg-black rounded-0 "
                              hint="Enter a command to interact with the sandboxes"
                              label="Enter Cmd"
                              single-line
                              v-model="cli_text"
                              v-on:keyup.enter="onEnter"
                ></v-text-field>
                <p v-if="!this.can_send_cmd_healthy || !this.can_send_cmd_infected" style="color:red">Please wait for the response</p>
            </v-col>
            <v-col v-if="!this.combined_cli" class="pa-1 " cols="12" md="6">
                <v-text-field
                    v-if="!this.combined_cli"
                ref="CLI_text_field_infected"
                style="border:1px solid white;font-family:'Courier New'"
                class="bg-black rounded-0 "
                hint="Send to infected sandbox"
                label="Enter Cmd"
                single-line
                v-model="cli_text_infected"
                v-on:keyup.enter="onEnter"
          ></v-text-field>
            </v-col>
              <v-col v-if="!this.combined_cli" class="pa-1" cols="12" md="6">
                <v-text-field
                    v-if="!this.combined_cli"
                ref="CLI_text_field_clean"
                style="border:1px solid white;font-family:'Courier New'"
                class="bg-black rounded-0 "
                hint="Send to clean sandbox"
                label="Enter Cmd"
                single-line
                v-model="cli_text_clean"
                v-on:keyup.enter="onEnter"
          ></v-text-field>
            </v-col>
              <v-col align="center">
              <v-btn
              icon

              color="black"
               @click="this.combined_cli = !this.combined_cli"
            >
              <v-icon>mdi-cached</v-icon>
            </v-btn>
                </v-col>
            </v-row>
          </v-container>
</template>

<script>
import TerminalInterface from "@/components/TerminalInterface";
//import io from "socket.io-client";


export default {
  name: "LiveTerminal",
    components: {TerminalInterface},
  props:{
    current_id: String,
    socket: Object,
  },
  data: () =>({
    ref : this,
    cli_text:"",
    cli_text_infected:"",
    cli_text_clean:"",
    infected_lines:[],
    clean_lines:[],
    can_send_cmd_healthy:true,
    can_send_cmd_infected:true,
    combined_cli : true,
      }),
  created() {
   let ref = this
    this.socket.on("terminalOutput", function (data){
      ref.add_feedback(JSON.parse(data))
    });
  },

  methods:{
    sendMessage: function(message){
      //sending to server
      console.log(message)
      this.socket.emit('my event', { data: message });

  },
  onEnter:function(){
      if (this.combined_cli && (this.can_send_cmd_healthy && this.can_send_cmd_infected)){
        this.can_send_cmd_healthy = false;
        this.can_send_cmd_infected = false;

        this.socket.emit('cli command', { "room":this.current_id, "healthy_cmd": this.cli_text, "infected_cmd": this.cli_text});
        this.$refs.CLI_text_field.reset("");
      }
      else if (!this.combined_cli){
        if(this.cli_text_clean && this.can_send_cmd_healthy){
          this.clean_lines.push(this.cli_text_clean);
          this.socket.emit('cli command', { "room":this.current_id, "healthy_cmd": this.cli_text_clean, "infected_cmd": ""});
          this.$refs.CLI_text_field_clean.reset("");
        }
        if(this.cli_text_infected && this.can_send_cmd_infected){
          this.infected_lines.push(this.cli_text_infected)
          this.socket.emit('cli command', { "room":this.current_id, "healthy_cmd": "", "infected_cmd": this.cli_text_infected});
          this.$refs.CLI_text_field_infected.reset("");
        }
      }
  },
    add_feedback(data){
      if (data["infectedStatus"] === "infected") {
        this.infected_lines.push(data["cmdOut"]);
        if (data["isLast"]){
          this.can_send_cmd_infected = true;
        }
        //time out to let everything render
        setTimeout(() => {this.$refs.infected_terminal.scrollToElement();}, 10);
      }
      else if (data["infectedStatus"] === "healthy") {
        this.clean_lines.push(data["cmdOut"]);
         if (data["isLast"]){
          this.can_send_cmd_healthy = true;
        }
        setTimeout(() => {this.$refs.healthy_terminal.scrollToElement();}, 10);
      }
    }
  },
  beforeUnmount: function() {
    this.socket.emit("leave room", {"room": this.current_id})
  }
}
</script>

<style scoped>

</style>