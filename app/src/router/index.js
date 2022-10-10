import { createWebHistory, createRouter } from "vue-router";
import HomeScreen from "@/components/HomeScreen.vue"
import ReportDashboard from "@/components/ReportDashboard.vue";
import LiveAnalysis from "@/components/LiveAnalysis.vue";
import PostAnalysis from "@/components/PostAnalysis";

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
  {
    path: "/live",
    name: "LiveAnalysis",
    component: LiveAnalysis,
  },
  {
    path: "/post",
    name: "PostAnalysis",
    component: PostAnalysis,
  },
  {
    path: '/live/:id',
    component: LiveAnalysis
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;