<template>
  <Login v-if="checkLogin" />
  <div v-else class="container-fluid">
    <div class="row">
      <aside class="col d-none d-md-block bg-color-sidebar-primary vh-100 pr-0">
        <SideBar />
      </aside>
      <div class="col px-0 main-contain">
        <Navbar />
        <main class="container-fluid mt-5">
          <div class="row">
            <div class="offset-md-0 col-12 col-sm-12 col-md-12">
              <TitleBar :title="title" v-show="title"></TitleBar>
            </div>
          </div>
          <router-view></router-view>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import SideBar from "@/components/sideBar";
import Navbar from "@/components/Navbar.vue";
import TitleBar from "@/components/TitleBar.vue";
import Login from "@/pages/login/index.vue";
import { accessToken } from "@/helper/accessToken";

export default {
  head() {
    return {
      title: "Homepage",
    };
  },
  components: {
    SideBar,
    TitleBar,
    Navbar,
    Login,
  },

  methods: {
    ...mapActions("user", ["setAllUsersList", "setAllExistedAccounts"]),
    ...mapActions("elearning", ["fetchTopics", "fetchQuestionTypes"]),
  },

  computed: {
    ...mapGetters({
      isCollapse: "value",
    }),
    checkLogin() {
      const store = require("../store");
      let exp = store.default.getters["scope/tokenInfo"].exp || undefined;
      return !accessToken || !(exp && exp * 1000 - 10000 < Date.now())
        ? false
        : true;
    },
    title() {
      if (this.$route.meta.title) {
        return this.$route.meta.title;
      }
      return "";
    },
  },
  created() {
    this.setAllUsersList();
    this.setAllExistedAccounts();
    this.fetchTopics();
    this.fetchQuestionTypes();
  },
};
</script>
<style lang="scss">
@import "../assets/scss/main.scss";
</style>
<style lang="scss" scoped>
@import "../assets/scss/app.scss";
</style>
