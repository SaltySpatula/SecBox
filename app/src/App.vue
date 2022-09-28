<template>

  <v-app class="bg-grey-darken-4">
    <body>
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

             <v-btn icon>
        <v-icon >mdi-plus-circle</v-icon>
      </v-btn>

      <v-app-bar-title>SecBox</v-app-bar-title>

      <v-spacer></v-spacer>

    </v-app-bar>

    <v-main>
      <HelloWorld/>
    </v-main>
  </body>
  </v-app>

</template>

<style>
v-app {
  color: darkslategrey;
}
</style>

<script>
import HelloWorld from './components/HomeScreen.vue'

export default {
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({


  }),
}
</script>
