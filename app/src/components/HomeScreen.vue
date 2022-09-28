<template>
  <div>
    <v-container fluid>
      <v-row align="center" class="ma-2">
        <v-col cols="12" md="4">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem">
            <v-card-text >
            <h1 class="pa-md-4"> Project Description </h1>
            <p class="pa-md-4">
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
        <v-col cols="12" md="4" fill-height>
          <v-card class="bg-purple-darken-4" style="overflow-y: auto; height:10rem">
              <v-card-title class="align-center pa-md-4">Analyze a new File</v-card-title>
              <v-card-actions class="justify-center align-center" >
                <StartAnalysisDialog></StartAnalysisDialog>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="bg-deep-purple-accent-1" style="overflow-y: auto; height:50rem">
            Plot 2 goes here
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>



import StartAnalysisDialog from "@/components/StartAnalysisDialog";
export default {
  name: 'HomeScreen',
  components: {StartAnalysisDialog},

  data: () => ({
    processId:""
  }),
}
</script>
