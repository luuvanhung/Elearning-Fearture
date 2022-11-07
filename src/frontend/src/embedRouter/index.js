import Vue from "vue";
import VueRouter from "vue-router";
import { embedRoutes } from "./embedRoutes";

Vue.use(VueRouter);

const embedRouter = new VueRouter({
  mode: "history",
  routes: embedRoutes,
});

export default embedRouter;
