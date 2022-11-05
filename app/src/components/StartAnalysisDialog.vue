<template>
  <div class="text-center">
    <v-btn
      @click="dialog = !dialog"
    >
      <v-icon >
        mdi-plus
      </v-icon>
    </v-btn>

     <v-dialog
      v-model="dialog"
      hide-overlay
      persistent
      width="800"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5">Start Analysis Process</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-select
                  :items="oss"
                  label="Select OS"
                  v-model="picked_os"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-table>
                  <thead>
                    <tr>
                      <th>
                        Select
                      </th>
                      <th class="text-left">
                        Name
                      </th>
                      <th class="text-left">
                        Type
                      </th>
                      <th class="text-left">
                        Url
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="item in malwares"
                      :key="item.name"
                    >
                      <td>
                        <input type="radio" color="purple" :id="item.hash" :value=item.hash v-model="picked_malware" />
                        <label :for=item.hash></label>
                      </td>
                      <td >{{ item.name }}</td>
                      <td>{{ item.type }}</td>
                      <td ><a :href="item.url" target="_blank"><v-icon color="black">mdi-link-box-variant</v-icon></a></td>
                    </tr>
                  </tbody>
                </v-table>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="purple"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="purple"
            text
            :disabled="sent_request"
            @click="start()"
          >
            Start Sandbox
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script>
import io from "socket.io-client";
import router from "@/router";

export default {
  name: "StartAnalysisDialog",
  props:{
    oss:Array,
    malwares:Array
  },
  data: () => ({
      dialog: false,
      processId:"",
      mwData:{},
      osData:[],
      picked_malware:null,
      picked_os:null,
      reports:null,
      sent_request:false
    }),

  methods:{
    start: async function(){
      if  (this.picked_malware == null || this.picked_os == null){
        console.error("Validation Error")
      }
      else {
        this.socket = io("ws://localhost:5000/start");
        const response = {"SHA256": this.picked_malware, "OS": this.picked_os};
        this.socket.emit('start request', response);
        this.sent_request = true;
        this.dialog=false;
        this.socket.on('start feedback', function(data){
            if (data){
              data = JSON.parse(data)
              let analysis_id = data.ID;
              this.dialog=false;
              router.push({path: `/live/${analysis_id}`});
            }
        });
      }
    }
  },
}

</script>

<style scoped>

</style>