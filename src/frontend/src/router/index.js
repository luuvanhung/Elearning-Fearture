import Vue from "vue";
import VueRouter from "vue-router";
import { routes } from "./routes";
import {
  checkAccessMiddleware,
  setPageTitleMiddleware,
  responsiveMiddleware,
} from "./middlewares";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes,
});
router.beforeEach(checkAccessMiddleware);
router.beforeEach(setPageTitleMiddleware);
// router.beforeEach(initCurrentUserStateMiddleware);
router.beforeEach(responsiveMiddleware);

export default router;
