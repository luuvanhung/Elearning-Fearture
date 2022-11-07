<template>
  <div>
    <div class="mb-3">
      We've detected info and assessors in account HRM. There may be some names
      you write in file excel that are not the same as in hrm.
      <br />
      Check and fix them with select box
    </div>
    <h4>General Information:</h4>
    <el-row class="d-flex align-items-center">
      <el-col :span="6"></el-col>
      <el-col :span="10"></el-col>
    </el-row>
    <div
      class="align-items-center"
      v-for="(info, index) in newInfos"
      :key="index"
    >
      <el-row class="d-flex align-items-center">
        <el-col :span="6">
          {{ info.title }}
        </el-col>
        <el-col :span="7">
          {{ info.value }}
        </el-col>
        <el-col :span="9" v-if="index === 0 || index === 3">
          <el-col v-if="info.check_employee_id"> Ok </el-col>
          <el-col v-else>
            No
            <el-select
              v-model="info.employee_id"
              class="ml-4"
              placeholder="Employee Name"
              style="width: 200px"
              @change="changeEmployee(info.employee_id, index)"
            >
              <el-option
                v-for="item in employeesData"
                :key="item.index"
                :label="item.profile.name"
                :value="item.id"
              >
              </el-option>
            </el-select>
          </el-col>
        </el-col>
      </el-row>
    </div>
    <el-row class="d-flex align-items-center">
      <el-col :span="6"></el-col>
      <el-col :span="4"></el-col>
      <el-col :span="4"></el-col>
      <el-col :span="7">Check name exists in hrm</el-col>
    </el-row>
    <br />
    <div
      class="align-items-center"
      v-for="(overall, index) in newOveralls"
      :key="index"
    >
      <el-row class="d-flex align-items-center">
        <el-col :span="6">
          {{ overall.overall }}
        </el-col>
        <el-col :span="4">
          {{ overall.assessor_name }}
        </el-col>
        <el-col :span="4">
          {{ overall.role }}
        </el-col>
        <el-col :span="3" v-if="overall.old_assessor"> Ok </el-col>
        <el-col :span="7" v-else>
          No
          <el-select
            v-model="overall.assessor"
            class="ml-4"
            placeholder="Employee Name"
            style="width: 200px"
            @change="changeAssessor(overall.assessor, index)"
          >
            <el-option
              v-for="item in employeesData"
              :key="item.index"
              :label="item.profile.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
export default {
  components: {},

  props: ["overalls", "employeesData", "infos"],
  data() {
    return {
      newOveralls: [],
      newInfos: [],
    };
  },
  methods: {
    changeAssessor(assessorId, index) {
      const newOverall = (this.newOveralls[index].assessor_name =
        this.employeesData.find(
          (item) => item.id === assessorId
        )?.profile.name);
      this.newOveralls.slice(index, 1, ...newOverall);
      this.$emit("newOveralls", this.newOveralls);
    },
    changeEmployee(employeeId, index) {
      const newInfos = (this.newInfos[index].employee_id =
        this.employeesData.find((item) => item.id === employeeId)?.id);
      this.newInfos.slice(index, 1, ...newInfos);
      this.$emit("newInfos", this.newInfos);
    },
  },
  created() {
    this.newOveralls = [...this.overalls];
    this.newInfos = [...this.infos];
  },
  watch: {
    newOveralls: {
      deep: true,
      handler: function (item) {
        this.$emit("newOveralls", this.newOveralls);
      },
    },
    newInfos: {
      deep: true,
      handler: function (item) {
        this.$emit("newInfos", this.newInfos);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
span {
  display: inline-block;
}
</style>
