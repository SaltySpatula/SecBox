<template>
<v-navigation-drawer
        floating
        permanent
        width="300"
        class="bg-deep-purple-lighten-1"
      >
  <v-btn
        style="margin-top: 1em"
                block
              large
              color="primary"
              dark
            >
              <v-icon              >
                mdi-content-save
              </v-icon>
              Save & Exit
       </v-btn>
</v-navigation-drawer>
  <v-container align="left" class="bg-deep-purple-lighten-4" style="width:80em">
    <h1> SecBox Report</h1>

  </v-container>
</template>

<script>
export default {
  name: "ReportPage",
  data: () => ({

  }),
  methods: {
    getDate:function (){
      const date = new Date();

      let day = date.getDate();
      let month = date.getMonth() + 1;
      let year = date.getFullYear();
      console.log(day, month, year)
    }
  }

}
</script>

<style scoped>

</style>