<template>
  <div>
    <v-container fluid>
      <v-row align="center" class="ma-2" v-if="this.reports">
        <v-col justify="center" cols="4" offset="2" md="8" sm="4"
          v-for="report in this.reports"
          :key="report.title">
          <v-card class="bg-deep-purple-lighten-4">
            <v-card-title >{{report.title}}</v-card-title>
            <v-card-subtitle>{{report.date}}</v-card-subtitle>
            <v-card-actions>

            <v-btn
        color="primary"
        variant="text"
        @click="goToReport(report.ID)"
      >
        Show Report
      </v-btn>

      <v-btn
          style="margin-left:auto;margin-right:0;"
        :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'"
        @click="show = !show"
      ></v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="show">
        <MalwareCard :malware="report.malware"></MalwareCard>
      </div>
    </v-expand-transition>
          </v-card>


        </v-col>

      </v-row>
    </v-container>
  </div>
</template>

<script>
import MalwareCard from "@/components/MalwareCard";
import router from "@/router";
export default {
  name: "ReportDashboard.vue",
  components:{MalwareCard:MalwareCard},
  data: () => ({
      reports:null,
    malware:null,
    show:false
  }),
  created: async function(){
        const gResponse = await fetch("http://localhost:5000/getReports");
        const obj  = await gResponse.json();
        this.reports = obj["reports"]
        for (let i=0; i<this.reports.length;i++){
          this.reports[i].malware = JSON.parse(this.reports[i].malware)
        }
    },
  methods:{
    goToReport:function(id){
      router.replace({path: '/report/' + id})
    }
  }
}
</script>

<style scoped>



</style>