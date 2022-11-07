<template>
  <div>
    <el-tabs
      v-model="currentPath"
      @tab-click="linkRouter"
      style="font-size: 1.4rem"
    >
      <el-tab-pane
        :label="tab.name"
        :name="tab.router"
        v-for="(tab, index) in tabList"
        :key="index"
      >
      </el-tab-pane>
    </el-tabs>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "TabNav",
  prop: {
    scopes: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      currentPath: "",
      general_prop: {
        name: "General",
        router: "/profile/",
        scopes: ["user:view_public_user_information_list"],
      },
    };
  },
  props: {
    tabList: Array,
  },
  computed: {
    ...mapGetters({
      tokenInfo: "scope/tokenInfo",
    }),
  },
  created() {
    this.currentPath = this.$route.path;
    if (this.tabList.find((value) => value.name === "General")) {
      if (
        this.tokenInfo.sub !== this.$route.params.id &&
        this.tokenInfo.scope.indexOf(
          "user:view_private_user_information_list"
        ) === -1
      ) {
        this.tabList = [this.general_prop];
      }
    }
  },
  methods: {
    //Jump Routing and Set Currently Active Labels
    linkRouter(tab, event) {
      if (tab.name === this.$route.path) {
        return false;
      }
      this.$router.push({ path: tab.name });
    },
  },
};
</script>

<style scoped>
/deep/.el-tabs__item {
  font-size: 1.4rem !important;
}
</style>
