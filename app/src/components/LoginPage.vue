<template>
  <v-card>
    <v-btn @click="login">Login</v-btn>
  </v-card>
</template>

<script>
export default {
  name: "LoginPage",
  methods: {
    login: async function (data) {
      //sending to server
      data = {
        "username": "python",
        "password": "is-great!"
      }
      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
      }
      const gResponse = await fetch("http://localhost:5000/login", requestOptions)
      console.log(gResponse)


    },
  }
}
</script>

<style scoped>

</style>