import { createWebHistory, createRouter } from "vue-router";
import HomeScreen from "@/components/HomeScreen.vue"
import ReportDashboard from "@/components/ReportDashboard.vue";
import LiveAnalysis from "@/components/LiveAnalysis.vue";
import PostAnalysis from "@/components/PostAnalysis";
import LoginPage from "@/components/LoginPage"
import ReportPage from "@/components/ReportPage"

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
    path: "/analysis/:id",
    name: "PostAnalysis",
    component: PostAnalysis,
  },
  {
    path: '/live/:id',
    component: LiveAnalysis
  },
  {
    path:'/report/:id',
    component: ReportPage
  },
  {
    path:'/login',
    component: LoginPage
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;