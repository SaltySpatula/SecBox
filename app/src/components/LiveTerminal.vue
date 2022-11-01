<template>
 <v-container fluid class="ma-0 pa-0">
            <v-row align="center" class="ma-2">
              <TerminalInterface ref="infected_terminal" type="infected" color="red" :lines=this.infected_lines></TerminalInterface>
              <TerminalInterface type="clean" color="green" :lines=this.clean_lines></TerminalInterface>
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
    cli_text:"",
    cli_text_infected:"",
    cli_text_clean:"",
    infected_lines:[],
    clean_lines:[],
    combined_cli : true,
      }),
  created() {
   let ref = this
    this.socket.on("cli feedback", function (data){
      ref.add_feedback(data)
    });
  },

  methods:{
    sendMessage: function(message){
      //sending to server
      console.log(message)
      this.socket.emit('my event', { data: message });

  },
  onEnter:function(){
      console.log(this.socket)
      if (this.combined_cli){
        this.clean_lines.push("$ " + this.cli_text);
        this.infected_lines.push("$ " +this.cli_text);

        this.socket.emit('cli command', { "room":this.current_id, "clean_cmd": this.cli_text, "infected_cmd": this.cli_text});
        this.$refs.CLI_text_field.reset();
      }
      else{
        console.log(this.cli_text_clean, this.cli_text_infected)
        if(this.cli_text_clean){
          this.clean_lines.push(this.cli_text_clean);
        }
        if(this.cli_text_infected){
          this.infected_lines.push(this.cli_text_infected)
        }
        this.socket.emit('cli command', { "room":this.current_id, "clean_cmd": this.cli_text_clean, "infected_cmd": this.cli_text_infected});
        this.$refs.CLI_text_field_clean.reset("");
        this.$refs.CLI_text_field_infected.reset("");
      }
  },
    add_feedback(data){
      this.clean_lines.push(data["clean_cmd"])
      this.infected_lines.push(data["infected_cmd"])
    }
  },
  beforeUnmount: function() {
    this.socket.emit("leave room", {"room": this.current_id})
  }
}
</script>

<style scoped>

</style>