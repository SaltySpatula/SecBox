<template>
        <v-col cols="6" md="6" class="pa-1 bg-black rounded-0" style="border:1px solid white;">
          <h2 :style="{color:color}"  >{{type}}</h2>
          <v-card id="to_be_scrolled" ref="scroller" class="bg-black rounded-0" style="overflow-y: auto; height:612px">
            <p
              v-for="line in lines"
              :key="line"
            >{{ line }}<br></p>
          </v-card>
        </v-col>
</template>

<script>
export default {
  name: "TerminalInterface",
  props: ['type', 'color', 'lines', 'sent_cmd'],
  methods:{
    scrollToElement(){
      let container = this.$el.querySelector("#to_be_scrolled");
      container.scrollTop = container.scrollHeight;
    }}
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
h2{
  text-align: center;
}

</style>