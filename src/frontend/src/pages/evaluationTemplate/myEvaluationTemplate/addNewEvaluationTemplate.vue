<template>
  <div>
    <el-card>
      <el-row type="flex" class="row-bg" justify="space-between">
        <h2 class="mb-4">Evaluation Template Builder</h2>
        <div>
          <el-button
            id="btn-submit"
            type="primary"
            size="medium"
            plain
            @click="submitForm('formEvaluationTemplate')"
            >Save</el-button
          >
          <el-button
            id="btn-discard"
            type="default"
            size="medium"
            @click="closeAddEvaluationTemplate"
            plain
            >Discard</el-button
          >
        </div>
      </el-row>
      <el-form
        :label-position="'left'"
        label-width="60px"
        :model="formEvaluationTemplate"
        status-icon
        :rules="rules"
        ref="formEvaluationTemplate"
        hide-required-asterisk
        size="small"
      >
        <el-row>
          <el-col :span="18">
            <el-form-item label="Name" prop="name">
              <el-input v-model="formEvaluationTemplate.name"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="18">
            <el-form-item label="Office" prop="office">
              <el-select
                class="max-width"
                v-model="formEvaluationTemplate.office"
                placeholder="Office"
              >
                <el-option
                  v-for="office in offices"
                  :key="office.id"
                  :label="office.name"
                  :value="office.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="18">
            <el-form-item label="Type" prop="type">
              <el-select
                class="max-width"
                v-model="formEvaluationTemplate.type"
                placeholder="Type"
              >
                <el-option
                  v-for="type in templateTypes"
                  :key="type.id"
                  :label="type.type_name"
                  :value="type.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <h4 class="title">Competencies:</h4>
        <div class="mb-3">
          <CriteriaItem
            :criterias="formEvaluationTemplate.competencies"
            :isAdd="true"
            :type_item="'competencies'"
          ></CriteriaItem>
        </div>

        <el-row type="flex" justify="center">
          <el-button
            class="btn-icon"
            type="success"
            size="small"
            icon="el-icon-plus"
            @click="addCriteria('competence')"
          ></el-button>
        </el-row>

        <h4 class="title">Overall comments:</h4>
        <div class="mb-3">
          <CriteriaItem
            :criterias="formEvaluationTemplate.overall_comments"
            :isAdd="false"
            :type_item="'overall_comments'"
          ></CriteriaItem>
        </div>

        <el-row type="flex" justify="center">
          <el-button
            class="btn-icon"
            type="success"
            size="small"
            icon="el-icon-plus"
            @click="addCriteria('overall_comment')"
          ></el-button>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import CriteriaItem from "@/pages/evaluationTemplate/myEvaluationTemplate/criteriaItemComponent";
import probationService from "@/services/probation/probation";
import { mapState, mapActions } from "vuex";

export default {
  name: "AddNewEvaluationTemplate",
  components: {
    CriteriaItem,
  },
  created() {
    this.fetchTypes();
    this.fetchOffices();
    this.fetchTitles();
  },
  computed: {
    ...mapState("probation", ["offices", "templateTypes"]),
  },
  data() {
    return {
      value: 0,
      formEvaluationTemplate: {
        name: "",
        office: "",
        type: "",
        competencies: [
          {
            competence: "",
            assessor_roles: [
              {
                assessor_role: "Self-evaluation",
              },
            ],
          },
        ],
        overall_comments: [
          {
            term: "",
            assessor_roles: [
              {
                overall_comment_role: "Self-evaluation",
              },
            ],
          },
        ],
      },
      rules: {
        name: [
          {
            required: true,
            message: "Please input Evaluation Template name!",
            trigger: "change",
          },
        ],
        office: [
          {
            required: true,
            message: "Please select Office!",
            trigger: "change",
          },
        ],
        type: [
          {
            required: true,
            message: "Please select Type!",
            trigger: "change",
          },
        ],
      },
    };
  },
  methods: {
    ...mapActions("probation", ["fetchOffices", "fetchTitles", "fetchTypes"]),

    hasDuplicates(array) {
      return new Set(array).size !== array.length;
    },

    async submitForm(formName) {
      this.value = 1;
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          let list_competence = this.formEvaluationTemplate.competencies.map(
            (data) => data.competence.trim()
          );
          let list_overall_comment =
            this.formEvaluationTemplate.overall_comments.map((data) =>
              data.term.trim()
            );
          if (this.hasDuplicates(list_competence)) {
            this.$toast.error(
              "Your evaluation template was duplicated competence"
            );
            return;
          }
          if (this.hasDuplicates(list_overall_comment)) {
            this.$toast.error(
              "Your evaluation template was duplicated overall comment"
            );
            return;
          }
          for (let competence of this.formEvaluationTemplate.competencies) {
            let list_value = competence.assessor_roles.map(
              (data) => data.assessor_role
            );
            if (this.hasDuplicates(list_value)) {
              this.$toast.error(
                "Your evaluation template was duplicated assessor"
              );
              return;
            }
          }
          let res = await probationService.createEvaluationTemplate(
            this.formEvaluationTemplate
          );
          if (res.status === 201) {
            this.$nextTick(() => {
              this.$toast.success(
                "Your evaluation template was created successfully"
              );
            });
            this.$router.push("/evaluation-form-templates");
          } else {
            let msg = "Your evaluation template was created error";
            if (res.data.error[0]) {
              msg = res.data.error[0];
            }
            this.$toast.error(msg);
          }
        } else {
          return false;
        }
      });
    },
    addCriteria(criteria) {
      if (criteria === "competence") {
        this.formEvaluationTemplate.competencies.push({
          competence: "",
          assessor_roles: [{ assessor_role: "Self-evaluation" }],
        });
      } else if (criteria === "overall_comment") {
        this.formEvaluationTemplate.overall_comments.push({
          term: "",
          assessor_roles: [{ overall_comment_role: "Self-evaluation" }],
        });
      }
    },
    closeAddEvaluationTemplate() {
      window.location.href = "/evaluation-form-templates";
    },
  },
};
</script>

<style lang="scss" scoped>
.el-card {
  margin: 12px;
  padding: 20px;
  color: #333;
  h4.title {
    font-weight: 600;
    padding-bottom: 10px;
    border-bottom: #ccc solid 1.5px;
    margin-bottom: 10px;
  }
  .el-select.max-width {
    width: 100%;
  }
}
</style>
