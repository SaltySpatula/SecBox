<template>
  <div>
    <v-container fluid>
      <v-row align="center" class="ma-2">
        <v-col justify="center" cols="4" offset="2" md="8" sm="4"
          v-for="report in reports"
          :key="report.title">
          <v-card class="bg-deep-purple-accent-1">
            <v-card-title v-text="report.title"></v-card-title>
            <v-card-actions >
              <div v-for="tag in report.tags" :key="tag" style="padding-right:10px">
                  <v-btn flat color="bg deep-purple-accent-1" variant="outlined">
                          {{tag}}
                  </v-btn>
                </div>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "ReportDashboard.vue",
  data: () => ({
      reports:[]
  }),
  created: async function(){
        const gResponse = await fetch("http://localhost:5000/getReports");
        const gObject = await gResponse.json();
        this.reports = JSON.parse(gObject.reports);
        console.log(this.reports);

    }
}
</script>

<style scoped>



</style>