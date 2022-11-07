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
  name: "EvaluationTemplateManage",
  data() {
    return {
      tabList: [
        {
          tabName: "Evaluation Form Template",
          tabRouter: "/evaluation-form-templates",
          scopes: ["evaluation_template:view"],
        },
        {
          tabName: "Evaluation Type",
          tabRouter: "/evaluation-form-templates/evaluation-templates-types",
          scopes: ["evaluation_template:view"],
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
