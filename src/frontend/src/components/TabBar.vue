<template>
  <div class="tab-container">
    <template v-for="(tab, index) in tabList">
      <div v-if="tab.scopes.length > 0" :key="index">
        <restricted-view :scopes="tab.scopes">
          <template v-slot:default>
            <span
              class="tab-single"
              :class="{ 'tab-active': index === activeIndex }"
              :key="index"
              @click="linkRouter(tab.tabRouter, index)"
            >
              {{ tab.tabName }}
            </span>
          </template>
        </restricted-view>
      </div>
      <div v-else :key="tab.scopes">
        <span
          class="tab-single"
          :class="{ 'tab-active': index === activeIndex }"
          :key="index"
          @click="linkRouter(tab.tabRouter, index)"
        >
          {{ tab.tabName }}
        </span>
      </div>
    </template>
  </div>
</template>
<script>
import RestrictedView from "@/components/RestrictedView";
import { mapGetters } from "vuex";
export default {
  name: "TabBar",
  components: {
    RestrictedView,
  },
  prop: {
    scopes: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      // activeIndex: 0,
      general_prop: {
        tabName: "General",
        tabRouter: "/profile/",
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
    activeIndex: {
      get: function () {
        const currentIndex = this.tabList.findIndex(
          (tab) => tab.tabRouter === this.$route.path
        );
        return currentIndex >= 0 ? currentIndex : 0;
      },
      set: function () {
        /* TODO document why this method 'set' is empty */
      },
    },
  },
  created() {
    if (this.tabList.find((value) => value.tabName === "General")) {
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
    linkRouter(routerPath, index) {
      if (routerPath === this.$route.path) {
        return false;
      }
      this.$router.push({ path: routerPath });
      this.activeIndex = index;
    },
  },
};
</script>

<style scoped>
.tab-container {
  display: flex;
  justify-content: center;
  flex-direction: row;
  border-bottom: 2px solid #e4e7ed;
  height: 40px;
  cursor: default;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.tab-single {
  margin-right: 2rem;
  height: 100%;
  line-height: 40px;
  display: inline-block;
  list-style: none;
  font-size: 15px;
  font-weight: 500;
  color: #303133;
  white-space: nowrap;
  z-index: 1;
}

.tab-active {
  color: #25c9d0;
  border-bottom: 2px solid #25c9d0;
}
</style>
