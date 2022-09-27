<template>
  <v-app>
    <v-app-bar
      absolute
      color="indigo darken-2"
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

      <v-app-bar-title>Secbox</v-app-bar-title>

      <v-spacer></v-spacer>

    </v-app-bar>
    <v-main>
      <HelloWorld/>
    </v-main>
  </v-app>


</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    //
  }),
}
</script>
