<template>
  <div class="my-2">
    <div class="bg-light">
      <TabBar :path="$route.path" :tab-list="tabList"></TabBar>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import TabBar from "@/components/TabBar";

export default {
  name: "LeaveManage",
  data() {
    return {
      tabList: [
        {
          tabName: "My Request",
          tabRouter: "/leaves",
          scopes: ["user:access_personal"],
        },
        {
          tabName: "My Approvals",
          tabRouter: "/leaves/approvals",
          scopes: ["user:access_personal"],
        },
        {
          tabName: "Office Request",
          tabRouter: "/leaves/office-requests",
          scopes: ["request_off:admin"],
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
