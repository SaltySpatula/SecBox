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
<router-link to="/">
      <v-btn icon color="white">

          <v-icon >mdi-home</v-icon>

      </v-btn>
  </router-link>

      <router-link to="/reports">

      <v-btn icon color="white">
        <v-icon >mdi-view-dashboard</v-icon>
      </v-btn>
      </router-link>

      <StartAnalysisDialog/>

      <v-app-bar-title>
        <p>{{ greeting }} - {{ flaskGreeting }}</p>
         <p></p>
      </v-app-bar-title>

      <v-spacer></v-spacer>

    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>

</template>

<style>
v-app {
  color: darkslategrey;
}
a { text-decoration: none; }
</style>

<script>
import StartAnalysisDialog from "@/components/StartAnalysisDialog";

export default {
  name: 'App',

  components: {
    StartAnalysisDialog,

  },

  data: () => ({
      greeting: 'SecBox',
      flaskGreeting: ''
  }),
  created: async function(){
        const gResponse = await fetch("http://localhost:5000/greeting");
        const gObject = await gResponse.json();
        this.flaskGreeting = gObject.greeting;
    }
}
</script>
