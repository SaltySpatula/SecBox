<template>
  <div>
    <v-container fluid>
      <v-row align="center" class="ma-2">
        <v-col justify="center" cols="12" md="12"
          v-for="report in reports"
          :key="report.title"

        >
          <v-card class="bg-deep-purple-accent-1">
            <v-card-title v-text="report.name"></v-card-title>
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
      reports:{}
  }),
  created: async function(){
        const gResponse = await fetch("http://localhost:5000/getReports");
        const gObject = await gResponse.json();
        this.reports = gObject.reports;
        console.log(this.reports);
    }
}
</script>

<style scoped>



</style>