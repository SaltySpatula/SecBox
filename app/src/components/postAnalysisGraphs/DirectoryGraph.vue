<template>
  <v-container v-if="this.render_both" style="padding:0">
     <v-row >
      <v-col cols="12" md="6">
    <VuePlotly :data="this.healthy_data" :layout="layout_healthy" :display-mode-bar="false"></VuePlotly>
      </v-col>
              <v-col cols="12" md="6">

    <VuePlotly :data="this.infected_data" :layout="layout_infected" :display-mode-bar="false"></VuePlotly>
      </v-col>
     </v-row>
  </v-container>
  <div v-else>
    <VuePlotly v-if="this.render_healthy" :data="healthy_data" :layout="layout_healthy" :display-mode-bar="false"></VuePlotly>
    <VuePlotly v-else  :data="infected_data" :layout="layout_infected" :display-mode-bar="false"></VuePlotly>
  </div>
</template>

<script>
import { VuePlotly } from 'vue3-plotly'

export default {
  name: "DirectoryGraph",
  components: {
    VuePlotly,
  },
  props: {render_healthy:Boolean, render_both:Boolean, graph_title: String, data: Object},
  created(){
  },
  methods: {


  },
  data() {
    return {
      healthy_data:[{
      type: "sunburst",
        hovertext:[this.data["infected"].root_value],
        hoverinfo:["label+text"],
      labels: this.data["healthy"].labels,
      parents: this.data["healthy"].parents,
      values:  this.data["healthy"].values,
      outsidetextfont: {size: 20, color: "#00E396"},
      leaf: {opacity: 0.9},
      marker: {line: {width: 2}},
}],infected_data:[{
      type: "sunburst",
        hovertext:[this.data["infected"].root_value],
        hoverinfo:["label+text"],
      labels: this.data["infected"].labels,
      parents: this.data["infected"].parents,
      values:  this.data["infected"].values,
      outsidetextfont: {size: 20, color: "#ff0084"},
      leaf: {opacity: 0.9},
      marker: {line: {width: 2}},
}],
      layout_healthy:{
  margin: {l: 0, r: 0, b: 0, t: 0},
  extendsunburstcolorway: true,
  height: 315,
        plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)',
        title: {text:"Healthy",y:0.1}
},
            layout_infected:{
  margin: {l: 0, r: 0, b: 0, t: 0},

  height: 315,
        plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)',
        title: {text:"Infected",y:0.1}
}

    }
  }
}
</script>

<style scoped>

</style>