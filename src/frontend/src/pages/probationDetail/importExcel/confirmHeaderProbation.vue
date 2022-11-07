<template>
  <div>
    The header is locate at row
    <div>
      <el-row :gutter="20">
        <el-col :span="5" class="mt-2">General Information:</el-col>
        <el-col :span="6">
          <el-select v-model="infoValue">
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
            <div v-for="(col, index) in info" :key="index">
              {{ col }}
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    <div>
      <el-row :gutter="20">
        <el-col :span="5" class="mt-2">Competencies:</el-col>
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
        <el-col :span="5" class="mt-2">Overall comments:</el-col>
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
    <div>
      <el-row :gutter="20">
        <el-col :span="5" class="mt-2">Outcome:</el-col>
        <el-col :span="6">
          <el-select v-model="outcomeValue">
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
            <div v-for="(col, index) in outcome" :key="index">
              {{ col }}
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
import _ from "lodash";
export default {
  props: ["headers"],
  data() {
    return {
      infoValue: "",
      competenceValue: "",
      overallValue: "",
      outcomeValue: "",
    };
  },
  computed: {
    info() {
      return this.headers[this.infoValue];
    },
    competence() {
      return this.headers[this.competenceValue];
    },
    overall() {
      return this.headers[this.overallValue];
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
      this.$emit("newExcelData", removeEmptyResult);
      return result;
    },
  },
  watch: {
    infoValue() {
      this.$emit("inputInfo", this.infoValue);
    },
    competenceValue() {
      this.$emit("inputCompetence", this.competenceValue);
    },
    overallValue() {
      this.$emit("inputOverall", this.overallValue);
    },
    outcomeValue() {
      this.$emit("inputOutcome", this.outcomeValue);
    },
  },
  created() {
    this.infoValue = this.options[1];
  },
  methods: {
    checkHeader(array, name) {
      return array.some((item) => String(item)?.includes(name));
    },

    getIndexOption(row, index) {
      if (!this.competenceValue && this.checkHeader(row, "Competencies"))
        this.competenceValue = index;
      else if (!this.overallValue && this.checkHeader(row, "Overall"))
        this.overallValue = index;
      else if (!this.outcomeValue && this.checkHeader(row, "Outcome"))
        this.outcomeValue = index;
    },

    findColIndex(array, name) {
      return array.findIndex((item) => item?.includes(name));
    },
  },
};
</script>
<style lang="scss" scoped>
.form-item {
  white-space: nowrap;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}
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
