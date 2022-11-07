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
import { SCOPES } from "@/const/scopes";

export default {
  name: "BonusLeavesMain",
  data() {
    return {
      tabList: [
        {
          tabName: "Bonus Leave",
          tabRouter: "/bonus-leaves",
          scopes: [SCOPES["BonusLeaveView"], SCOPES["BonusLeaveEdit"]],
        },
        {
          tabName: "Bonus Leave Types",
          tabRouter: "/bonus-leaves/bonus-types",
          scopes: [SCOPES["BonusLeaveView"], SCOPES["BonusLeaveEdit"]],
        },
      ],
    };
  },
  components: {
    TabBar,
  },
};
</script>
