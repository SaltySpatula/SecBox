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
                  :items="['Ubuntu']"
                  label="Select OS*"
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
                      v-for="item in this.mwData"
                      :key="item.name"
                    >
                      <td>
                        <input type="radio" :id="item.hash" :value=item.hash v-model="picked_malware" />
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
            color="blue darken-1"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="loading = true;dialog=false;start()"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="loading"
      hide-overlay
      persistent
      width="300"
    >
      <v-card
        color="primary"
        dark
      >
        <v-card-text>
          Please stand by
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "StartAnalysisDialog",
  data: () => ({
      dialog: false,
      loading:false,
      processId:"",
      mwData:null,
      picked_malware:null,
      reports:null,
    }),
  created: async function(){
      const gResponse = await fetch("http://localhost:5000/getAvailableMalwares");
      const gObject = await gResponse.json();
      this.mwData = JSON.parse(gObject.malwares);
      console.log(this.mwData);
  },
  methods:{
    start: async function(){
        const gResponse = await fetch("http://localhost:5000/start");
        const gObject = await gResponse.json();
        this.processId = gObject.processId;
        console.log(this.picked_malware)
    }
  }
}

</script>

<style scoped>

</style>