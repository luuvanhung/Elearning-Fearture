<template>
  <div>
    <el-row
      v-for="(criteria, _idx) in criterias"
      :key="_idx"
      class="mb-2"
      type="flex"
      align="middle"
      :gutter="10"
    >
      <el-col class="criteria-item" :span="23">
        <el-col :span="10">
          <div>
            <el-form-item
              v-if="type_item === 'competencies'"
              label-width="0px"
              class="name"
              :prop="'competencies.' + _idx + '.competence'"
              :rules="[
                {
                  required: true,
                  message: 'Please input competencies name!',
                  trigger: 'change',
                },
              ]"
            >
              <el-input
                placeholder="Enter the competencies name"
                v-model="criteria.competence"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item
              v-else
              label-width="0px"
              class="name"
              :prop="'overall_comments.' + _idx + '.term'"
              :rules="[
                {
                  required: true,
                  message: 'Please input overall comment name!',
                  trigger: 'change',
                },
              ]"
            >
              <el-input
                placeholder="Enter the overall comment name"
                v-model="criteria.term"
                size="small"
              ></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col class="assessors" :span="14">
          <span>Assessor: </span>
          <template v-for="(assessor, index) in criteria.assessor_roles">
            <el-select
              v-if="type_item === 'competencies'"
              v-model="criteria.assessor_roles[index]['assessor_role']"
              size="small"
              class="mb-1"
              :key="index"
            >
              <el-option
                v-for="item in getListAssessor(_idx)"
                :key="item"
                :value="item"
              >
              </el-option>
            </el-select>
            <el-select
              v-else
              v-model="criteria.assessor_roles[index]['overall_comment_role']"
              size="small"
              class="mb-1"
              :key="index"
            >
              <el-option
                v-for="item in getListAssessor(_idx)"
                :key="item"
                :value="item"
              >
              </el-option>
            </el-select>
            <el-button
              v-if="isAdd"
              :key="'B' + index"
              class="btn-remove"
              type="danger"
              icon="el-icon-close"
              round
              size="mini"
              @click="deleteAssessor(_idx, index)"
            ></el-button>
          </template>
          <el-button
            v-if="isAdd"
            class="btn-icon ml-3"
            icon="el-icon-plus"
            size="small"
            plain
            @click="addAssessor(_idx)"
          ></el-button>
        </el-col>
      </el-col>

      <el-col :span="1">
        <el-button
          class="btn-icon"
          type="danger"
          size="small"
          icon="el-icon-close"
          @click="deleteCriteria(_idx)"
        ></el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "CriteriaItem",
  props: {
    criterias: Array,
    isAdd: Boolean,
    type_item: String,
  },
  computed: {
    ...mapGetters("probation", ["titles"]),
  },
  data() {
    return {};
  },
  methods: {
    deleteCriteria(index) {
      if (this.criterias.length >= 2) {
        this.criterias.splice(index, 1);
      }
    },
    addAssessor(_idx) {
      if (this.type_item === "competencies") {
        if (
          this.criterias[_idx].assessor_roles.length ===
          this.titles.length + 2
        ) {
          this.$nextTick(() => {
            this.$toast.warning("Can not add assessor role");
          });
        } else {
          var assessor = "Self-evaluation";
          if (
            this.criterias[_idx].assessor_roles.some(
              (e) => e.assessor_role === "Self-evaluation"
            )
          ) {
            if (
              this.criterias[_idx].assessor_roles.some(
                (e) => e.assessor_role === "Line Manager"
              )
            ) {
              for (let title of this.titles) {
                if (
                  !this.criterias[_idx].assessor_roles.some(
                    (e) => e.assessor_role === title
                  )
                ) {
                  assessor = title;
                  break;
                }
              }
            } else {
              assessor = "Line Manager";
            }
          }
          this.criterias[_idx].assessor_roles.push({
            assessor_role: assessor,
          });
        }
      } else {
        this.criterias[_idx].assessor_roles.push({
          overall_comment_role: "Self-evaluation",
        });
      }
    },
    deleteAssessor(_idx, index) {
      if (this.criterias[_idx].assessor_roles.length >= 2) {
        this.criterias[_idx].assessor_roles.splice(index, 1);
      }
    },
    getListAssessor(_idx) {
      let ls_select = ["Self-evaluation", "Line Manager", ...this.titles];
      let ls = this.criterias[_idx].assessor_roles.map(
        ({ assessor_role }) => assessor_role
      );
      let res = ls_select.filter((t) => !ls.includes(t));
      return res;
    },
  },
};
</script>
<style lang="scss" scoped>
.el-col.criteria-item {
  background-color: #eee;
  border: 1px solid #333;
  padding: 4px 0px 0px;
}

.el-col.assessors {
  span {
    font-size: 14px;
    height: 100%;
  }
  .el-select {
    width: 140px;
    margin-left: 8px;
  }
  .btn-remove {
    margin: 0px;
    padding: 2px;
  }
}
.el-button.btn-icon {
  padding: 6px;
  margin: 0 6px;
}
</style>
