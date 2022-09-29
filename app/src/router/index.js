import { createWebHistory, createRouter } from "vue-router";
import HomeScreen from "@/components/HomeScreen.vue"
import ReportDashboard from "@/components/ReportDashboard.vue";

const routes = [
  {
    path: "/",
    name: "HomeScreen",
    component: HomeScreen,
  },
  {
    path: "/reports",
    name: "ReportDashboard",
    component: ReportDashboard,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;