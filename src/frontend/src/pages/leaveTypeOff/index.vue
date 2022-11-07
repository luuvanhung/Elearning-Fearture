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
  name: "LeaveTypesMain",
  data() {
    return {
      tabList: [
        {
          tabName: "Leave Types",
          tabRouter: "/leave-types",
          scopes: ["type_off:view"],
        },
        {
          tabName: "Leave Type Groups",
          tabRouter: "/leave-types/leave-type-groups",
          scopes: ["type_pay:view"],
        },
      ],
    };
  },
  components: {
    TabBar,
  },
};
</script>
