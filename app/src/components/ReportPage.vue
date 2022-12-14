<template>
    <v-overlay :model-value="loading" class="align-center justify-center">
      <v-progress-circular
        indeterminate
        size="64"
        color="primary"
        persistent
        opacity="0.75"
      ></v-progress-circular>
    </v-overlay>
<v-navigation-drawer
        floating
        permanent
        width="300"
        class="bg-deep-purple-lighten-1"
      >

  <v-card class="bg-deep-purple-lighten-2" style="padding:10px">
    <v-card-title>Download Files</v-card-title>
     <v-switch
      v-model="download_files"
      color="primary"
      label="PCAP Healthy"
      value="PCAP Healthy"
      hide-details
    ></v-switch>
    <v-switch
      v-model="download_files"
      color="primary"
      label="PCAP Infected"
      value="PCAP Infected"
      hide-details
    ></v-switch>
        <v-switch
      v-model="download_files"
      color="primary"
      label="SysCalls Healthy"
      value="SysCalls Healthy"
      hide-details
    ></v-switch>
            <v-switch
      v-model="download_files"
      color="primary"
      label="SysCalls Infected"
      value="SysCalls Infected"
      hide-details
    ></v-switch>
    <v-btn
        style="margin-top: 1em"
                block
              large
              color="primary"
              dark
        :disabled="this.download_files.length === 0"
        @click="this.downloadManager()"
            >
              <v-icon              >
                mdi-download
              </v-icon>
              Download Files
       </v-btn>
    </v-card>
  <v-btn
        style="margin-top: 1em"
                block
              large
              color="primary"
              dark
        @click="this.saveGraph()"
            >
              <v-icon              >
                mdi-content-save
              </v-icon>
              Save & Exit
       </v-btn>
  <div style="position: absolute;
                bottom: 0;width:300px">
  <MalwareCard
          v-if="this.malware"
          :malware="this.malware"
      ></MalwareCard>
    </div>
</v-navigation-drawer>
  <v-container align="left" class="bg-deep-purple-lighten-4" >
    <v-text-field
            v-model="this.title"
            label="Enter a title"
            filled
            style="font-size:2em;max-height:4em;"
          ></v-text-field>
    <v-row v-if="this.selected_graphs">
      <v-col cols="12" md="6" v-for="graph in this.selected_graphs" v-bind:key="graph.title">
        <v-card class="bg-deep-purple-lighten-5">
        <v-card-title>{{ graph.title }}</v-card-title>
          <PAGraphWrapper :render_healthy="this.render_healthy" :render_both="true" :socket="this.socket_analysis" :graph_title="graph.title" :graph_get="graph.get"/>
           <v-textarea
          v-model="graph.comment"/>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import io from "socket.io-client";
import PAGraphWrapper from "@/components/PAGraphWrapper";
import download from "downloadjs"
import MalwareCard from "@/components/MalwareCard";
export default {
  name: "ReportPage",
  components:{PAGraphWrapper, MalwareCard},
  created(){
    this.socket = io("ws://localhost:5000/report");
    const ref = this
    this.socket.emit('get report', {"ID": this.$route.params.id})
    this.socket.on("send report", function (data){
          data = JSON.parse(data)
          ref.selected_graphs = data["selected_graphs"]
          ref.title = data["title"]
          ref.loading = false
          ref.malware = data.malware
        })

    this.socket_analysis = io("ws://localhost:5000/analysis");
    this.socket_analysis.emit('join analysis room', {"room": this.$route.params.id}, function () {});
  },
  data: () => ({
    download_files : [],
      render_healthy : true,
    loading : true,
    selected_graphs : [],
    malware : null,
    title:""
  }),
  methods: {
    saveGraph:function(){
      //console.log("updating", this.title, this.selected_graphs)
      this.socket.emit("update report", {ID: this.$route.params.id, title:this.title, selected_graphs:this.selected_graphs})
    },
    downloadManager:function(){
      if (this.download_files){
      for (let i=0;i<this.download_files.length;i++){
        if (this.download_files[i] === "SysCalls Infected"){
          this.downloadSyscalls("infected")
        }
        else if (this.download_files[i] === "SysCalls Healthy"){
          this.downloadSyscalls("healthy")
        }
        else if (this.download_files[i] === "PCAP Healthy"){
          this.downloadPCAP("healthy")
        }
        else if (this.download_files[i] === "PCAP Infected"){
          this.downloadPCAP("infected")
        }
      }
      }
    },
    downloadPCAP: function(infected_status){
      let id = this.$route.params.id
      fetch("http://localhost:5000/report/download_pcap/"+id+"/"+infected_status)
          .then(res=>{
            return res.blob();
        }).then(blob=>{
            download(blob, "PCAP_"+infected_status+"_"+ id+".pcap")
        }).catch(err=>console.log(err));
    },
    downloadSyscalls: function(infected_status){
      let id = this.$route.params.id
      fetch("http://localhost:5000/report/download_syscalls/"+id+"/"+infected_status)
          .then(res=>{
            return res.blob();
        }).then(blob=>{
            download(blob, "syscalls_"+infected_status+"_"+ id+".csv")
        }).catch(err=>console.log(err));
  }
  }

}
</script>

<style scoped>
.v-text-field input {
  font-size:1.2em
}
</style>