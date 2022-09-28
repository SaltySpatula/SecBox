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
              <v-col
                cols="12"
              >
               <v-select
                  :items="['Mirai', 'Gafgyt']"
                  label="Select Malware*"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-select
                  :items="['Ubuntu']"
                  label="Select OS*"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="Password*"
                  type="password"
                  required
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                <v-select
                  :items="['0-17', '18-29', '30-54', '54+']"
                  label="Age*"
                  required
                ></v-select>
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                <v-autocomplete
                  :items="['Skiing', 'Ice hockey', 'Soccer', 'Basketball', 'Hockey', 'Reading', 'Writing', 'Coding', 'Basejump']"
                  label="Interests"
                  multiple
                ></v-autocomplete>
              </v-col>
            </v-row>
          </v-container>
          <small>{{processId}}</small>
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
      processId:""
    }),
  watch: {
      loading () {
        if (this.processId){
          this.loading = false
        }
      },
    },
  methods:{
    start: async function(){
        const gResponse = await fetch("http://localhost:5000/start");
        const gObject = await gResponse.json();
        this.processId = gObject.processId;
    }
    }
}

</script>

<style scoped>

</style>