<template>
        <v-col class="pa-1" cols="6" md="6">
          <v-card class="bg-black rounded-0" style="overflow-y: auto; height:40rem; border:1px solid white;">
            <v-card-title :style="{color:color}" >{{type}}</v-card-title>
            <p
              v-for="line in lines"
              :key="line"
            >$ {{ line }}<br></p>
          </v-card>
        </v-col>
</template>

<script>
export default {
  name: "TerminalInterface",
  props: ['type', 'color', 'lines'],
}

</script>

<style scoped>
.v-card-title{
    font-family: "Courier New";
    font-weight: bold;
}
p{
  font-family: "Courier New";
  margin-left: 10px;
}
</style>