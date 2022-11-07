<template>
  <div class="my-2">
    <div class="bg-light">
      <TabBar :tab-list="tabList"></TabBar>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import TabBar from "@/components/TabBar";

export default {
  name: "LeaveReport",
  data() {
    return {
      tabList: [
        {
          tabName: "My Report",
          tabRouter: "/leave-reports",
          scopes: ["statistic_dateoff:user"],
        },
        {
          tabName: "My Team",
          tabRouter: "/leave-reports/my-team",
          scopes: ["statistic_dateoff:team"],
        },
        {
          tabName: "Office",
          tabRouter: "/leave-reports/offices",
          scopes: ["statistic_dateoff:office"],
        },
      ],
    };
  },
  components: {
    TabBar,
  },
};
</script>

<style scoped></style>
