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
  name: "WFHManage",
  data() {
    return {
      tabList: [
        {
          tabName: "My Request",
          tabRouter: "/workfromhome",
          scopes: ["user:access_personal"],
        },
        {
          tabName: "Office",
          tabRouter: "/workfromhome/wfh-office-requests",
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
