<template>
  <div class="my-2 ma-auto">
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
        { tabName: "Search", tabRouter: "/skill/", scopes: ["skill:view"] },
        {
          tabName: "Reports",
          tabRouter: "/skill/reports",
          scopes: ["skill_report:view"],
        },
        {
          tabName: "Level",
          tabRouter: "/skill/levels",
          scopes: ["skill_level:view"],
        },
        {
          tabName: "Skill Definition",
          tabRouter: "/skill/definitions",
          scopes: ["skill_definition:view"],
        },
        {
          tabName: "Position's Skill",
          tabRouter: "/skill/position",
          scopes: ["title_skill:view"],
        },
      ],
    };
  },
  components: {
    TabBar,
  },
};
</script>
