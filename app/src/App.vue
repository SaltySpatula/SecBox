<template>

  <v-app class="bg-grey-darken-4">
    <v-app-bar
      absolute
      color="deep-purple darken-2"
      dark
      shrink-on-scroll
      prominent
      scroll-target="#scrolling-techniques"
    >

      <v-btn icon>
        <v-icon >mdi-home</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon >mdi-view-dashboard</v-icon>
      </v-btn>

      <StartAnalysisDialog/>

      <v-app-bar-title>
        <p>{{ greeting }}</p>
         <p>{{ flaskGreeting }}</p>
      </v-app-bar-title>

      <v-spacer></v-spacer>

    </v-app-bar>

    <v-main>
      <HelloWorld/>
    </v-main>
  </v-app>

</template>

<style>
v-app {
  color: darkslategrey;
}
</style>

<script>
import HelloWorld from './components/HomeScreen.vue'
import StartAnalysisDialog from "@/components/StartAnalysisDialog";

export default {
  name: 'App',

  components: {
    StartAnalysisDialog,
    HelloWorld,
  },

  data: () => ({
      greeting: 'Hello, Vue!',
      flaskGreeting: ''
  }),
  created: async function(){
        const gResponse = await fetch("http://localhost:5000/greeting");
        const gObject = await gResponse.json();
        this.flaskGreeting = gObject.greeting;
    }
}
</script>
