<template>
  <div>
    <div class="chart mt-3 mb-3">
      <bar-chart
        v-if="loaded"
        :chartData="chartData"
        :uniqueLevels="uniqueLevels"
      />
    </div>
    <div class="chart">
      <pie-chart v-if="loaded" :skills="skills" :width="700" :height="700" />
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import BarChart from "./BarChart";
import PieChart from "./PieChart";
import SkillReports from "@/services/skill/report";

export default {
  name: "ChartContainer",
  components: { BarChart, PieChart },
  data: () => ({
    loaded: false,
    chartData: [],
    uniqueLevels: [],
    skills: [],
  }),
  created() {
    this.loaded = false;
    this.getData();
  },
  methods: {
    async getData() {
      try {
        let listData = await SkillReports.getAll();
        this.chartData = this.handleDataAPI(listData.data);
        this.handleSkillData(listData.data);
        this.loaded = true;
      } catch (e) {
        console.error(e);
      }
    },
    handleDataAPI(dataAPI) {
      const uniqueSkill = _.uniqBy(dataAPI, "skill_definition.skill.id");
      this.uniqueLevels = _.uniqBy(dataAPI, "skill_definition.level.id").map(
        (element) => element.skill_definition.level
      );
      return uniqueSkill.map((skillArray) => {
        const { id, name } = skillArray.skill_definition.skill;
        const newData = {
          id,
          name,
          level: {},
        };
        let arrayKey = [];
        dataAPI.forEach((item) => {
          const level = Object.assign({}, item.skill_definition.level);
          level.count = 1;
          const { name } = level;
          const levelId = level.id;
          if (item.skill_definition.skill.id === id) {
            if (arrayKey.includes(levelId)) {
              newData.level[name].count++;
            } else {
              arrayKey.push(levelId);
              newData.level[name] = level;
            }
          }
        });
        return newData;
      });
    },
    handleSkillData(dataAPI) {
      const uniqueSkill = _.uniqBy(dataAPI, "skill_definition.skill.id");
      this.skills = uniqueSkill.map((skill) => skill.skill_definition.skill);
      dataAPI.forEach((item) => {
        const skill = this.skills.find(
          (skill) => skill.name === item.skill_definition.skill.name
        );
        if (skill.count === undefined) {
          skill.count = 1;
        } else {
          skill.count++;
        }
      });
    },
  },
};
</script>

<style scoped>
.chart {
  box-shadow: 0 0 10px #c6c6c6;
}
</style>
