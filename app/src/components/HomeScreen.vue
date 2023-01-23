<template>
  <div>
    <v-container fluid>
      <v-row align="center" class="ma-2">
        <v-col cols="12" md="4" lg="4" xl="4">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem">
            <v-card-text style="color:black">
            <h1 class="pa-md-4" align="center"> Project Description </h1>
            <p class="text-justify">
              SecBox is a light-weight, container-based sandbox for malware analysis.
              It uses Google's <a href="https://gvisor.dev/">gVisor</a> technology to create a secure and isolate environment.
              In this environment, users can securely execute malware and compare it to a baseline container in which no such malware is executed.
              This comparison enables analysts to notice differences in resource usage and system call between systems.
              Furthermore, it allows for interaction with both systems to elicit malicious behavior.
              If such behavior appears, a report can be generated where users can visualize different metrics.
              This report can then be collaboratively analyzed and converted into a PDF file, which contains the analysts' comments and graphics.
            </p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4" lg="4" xl="4" fill-height align="center"
      justify="center" style="

background: linear-gradient(0deg,rgba(121,86,150,0) 0%, rgba(179,136,255,0.7) 5%, rgba(225,234,236,0) 50%);">
              <v-img :src="require('@/static/logo.png')" alt="SecBox Logo: An impossible cube"/>
        </v-col>
        <v-col cols="12" md="4" lg="4" xl="4">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem" >
            <v-card-text style="color:black">
            <h1 class="pa-md-4" align="center"> Latest Reports </h1>
            <v-row align="center" class="ma-2">
              <v-col justify="center" cols="4"  md="12" sm="12"
                v-for="report in reports"
                :key="report.title">
                <v-card class="bg-purple-darken-4" @click="goToReport(report.ID)">
                  <v-card-title v-text="report.title"></v-card-title>
                  <v-card-subtitle>{{report.date}}</v-card-subtitle>
                  <v-card-actions >
                    <div v-for="tag in report.tags" :key="tag" style="padding-right:10px">
                        <v-btn flat variant="outlined">
                                {{tag}}
                        </v-btn>
                      </div>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
              </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>


<script>


import router from "@/router";

export default {

  name: 'HomeScreen',
  components: {
  },
  data: () => ({
      reports:[]
  }),
  created: async function(){
        const gResponse = await fetch("http://"+process.env.VUE_APP_ROOT+"/getReports");
        const reports = await gResponse.json();
        this.reports = reports["reports"]
    },
  methods:{
    goToReport:function(id){
      router.replace({path: '/report/' + id})
    }
  }
}
</script>
