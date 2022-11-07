<template>
  <div>
    We've detected the template for roles of competences and overall comments:
    <br />
    <br />
    <h4>Template Probation you selected:</h4>
    <div>
      <el-row :gutter="20">
        <el-col :span="7" class="mt-2"
          >Competencies have {{ competenceRoles.length }} roles:</el-col
        >
        <el-col :span="6"> </el-col>
        <el-col :span="11">
          <div class="cols">
            <div v-for="(col, index) in competenceRoles" :key="index">
              {{ col }}
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div>
      <el-row :gutter="20">
        <el-col :span="7" class="mt-2"
          >Overall comments have {{ overallRoles.length }} roles:</el-col
        >
        <el-col :span="6"> </el-col>
        <el-col :span="11">
          <div class="cols">
            <div v-for="(col, index) in overallRoles" :key="index">
              {{ col }}
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <h4>Form Excel you imported:</h4>
    <div>
      <el-row :gutter="20">
        <el-col :span="7" class="mt-2"
          >Competencies have {{ roleCompetenceLength }} roles:</el-col
        >
        <el-col :span="6">
          <el-select v-model="competenceValue">
            <el-option
              v-for="item in options"
              :key="item"
              :label="item + 1"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="11">
          <div class="cols">
            <div v-for="(col, index) in competence" :key="index">
              {{ col }}
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div>
      <el-row :gutter="20">
        <el-col :span="7" class="mt-2"
          >Overall comments have {{ roleOverallLength }} roles:</el-col
        >
        <el-col :span="6">
          <el-select v-model="overallValue">
            <el-option
              v-for="item in options"
              :key="item"
              :label="item + 1"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="11">
          <div class="cols">
            <div v-for="(col, index) in overall" :key="index">
              {{ col }}
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <br />
    The selected template
    <span style="color: blue"
      >{{ isCheckTemplate ? "" : "doesn't" }} match</span
    >
    with the imported excel.
    <i
      >Select ok if it is correct, if not, choose cancel then import it again.
    </i>
  </div>
</template>
<script>
import _ from "lodash";

export default {
  props: ["headers", "competenceRoles", "overallRoles"],
  data() {
    return {
      competenceValue: 0,
      overallValue: 0,
      outcomeValue: 0,
      roleCompetenceLength: 0,
      roleOverallLength: 0,
      roleOverallColIndex: 0,
      assessorOverallColIndex: 0,
      detectCompetenceRoles: [],
      detectOverallRoles: [],
      isCheckCompetence: false,
      isCheckOverall: false,
    };
  },
  computed: {
    competence() {
      const competence = this.headers[this.competenceValue]?.slice(1);
      this.checkCompetence(competence);
      return competence;
    },
    overall() {
      const overall = this.headers
        .slice(this.overallValue + 1, this.outcomeValue)
        .map((item) => item[this.roleOverallColIndex]);
      this.checkOverall(overall);
      return overall;
    },
    outcome() {
      return this.headers[this.outcomeValue];
    },
    options() {
      let result = [];
      let removeEmptyResult = [];
      for (let index = 0; index < this.headers.length; index++) {
        this.getIndexOption(this.headers[index], index);
        result.push(index);
        removeEmptyResult.push(_.compact(this.headers[index]));
      }
      this.$emit("removeEmptyExcelData", removeEmptyResult);
      return result;
    },
    isCheckTemplate() {
      this.$emit(
        "checkTemplate",
        this.isCheckOverall && this.isCheckCompetence
      );
      return this.isCheckOverall && this.isCheckCompetence;
    },
  },
  watch: {
    competenceValue() {
      this.$emit("inputCompetence", this.competenceValue);
    },
    overallValue() {
      this.$emit("inputOverall", this.overallValue);
    },
  },
  created() {},
  methods: {
    checkHeader(array, name) {
      return array?.some((item) => String(item)?.includes(name));
    },
    findColIndex(array, name) {
      return array.findIndex((item) => item?.includes(name));
    },
    getIndexOption(row, rowIndex) {
      if (!this.competenceValue && this.checkHeader(row, "Competencies"))
        this.competenceValue = rowIndex - 2;
      else if (!this.overallValue && this.checkHeader(row, "Overall")) {
        this.overallValue = rowIndex;
        this.assessorOverallColIndex = this.findColIndex(row, "Assessor");
        this.roleOverallColIndex = this.assessorOverallColIndex + 5;
        this.$emit("assessorOverallColIndex", this.assessorOverallColIndex);
        this.$emit("roleOverallColIndex", this.roleOverallColIndex);
      } else if (!this.outcomeValue && this.checkHeader(row, "Outcome"))
        this.outcomeValue = rowIndex;
    },
    isSameTwoArray(firstArr, secondArr) {
      return (
        _.isEmpty(_.xor(firstArr, secondArr)) &&
        firstArr.length === secondArr.length
      );
    },
    checkCompetence(competence) {
      const cleanCompetence = _.compact(competence);
      this.roleCompetenceLength = cleanCompetence.length;
      this.$emit("excelCompetenceRoles", cleanCompetence);
      this.isCheckCompetence = this.isSameTwoArray(
        cleanCompetence,
        this.competenceRoles
      );
    },
    checkOverall(overall) {
      const cleanOverall = _.compact(overall);
      //overall role is duplicate
      this.roleOverallLength = cleanOverall.length;
      this.$emit("roleOverallColLength", cleanOverall.length);
      this.isCheckOverall = this.isSameTwoArray(
        cleanOverall,
        this.overallRoles
      );
    },
  },
};
</script>
<style lang="scss" scoped>
.cols {
  padding-bottom: 10px;
  width: 400px;
  display: flex;
  overflow-y: auto;
  &::-webkit-scrollbar {
    height: 10px;
  }
  /* Track */
  &::-webkit-scrollbar-track {
    background: white;
    border-radius: 50rem;
    outline: 1px solid #cbcddc;
  }
  /* Handle */
  &::-webkit-scrollbar-thumb {
    border: 2px solid white;
    background: #cbcddc;
    border-radius: 50rem;
  }
  & > div {
    padding: 0.5rem 1rem;
    white-space: nowrap;
    border: 2px solid #cbcddc;
    border-right: none;
    &:last-child {
      border-right: 2px solid #cbcddc;
    }
  }
}
</style>
