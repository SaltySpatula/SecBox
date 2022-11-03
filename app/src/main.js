import { createApp } from 'vue/dist/vue.esm-bundler';
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import VueApexCharts from "vue3-apexcharts";

loadFonts()

createApp(App)
    .use(vuetify)
    .use(router)
    .use(VueApexCharts)
    .mount('#app')
