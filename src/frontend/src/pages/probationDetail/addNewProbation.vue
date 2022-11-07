<template>
  <div>
    <div class="row m-4">
      <div
        class="col-12 col-lg-6 col-xl-6 ml-auto justify-xl-end d-flex justify-content-end"
      >
        <el-button type="primary" @click="exportNewProbation">
          <font-awesome-icon :icon="['fas', 'file-export']" />
          <span class="ml-2">Export</span>
        </el-button>
        <el-button
          type="default"
          @click="$router.push({ path: `/evaluations/import` })"
        >
          <font-awesome-icon :icon="['fas', 'file-import']" />
          <span class="ml-2">Import</span>
        </el-button>
        <el-button type="warning" @click="saveData('newProbation')">
          <font-awesome-icon :icon="['fas', 'save']" />
          <span class="ml-2">Save</span>
        </el-button>
        <el-button type="danger" @click="back()">
          <font-awesome-icon :icon="['fas', 'step-backward']" />
          <span class="ml-2">Discard</span>
          <i class="fa-solid fa-arrow-left-long-to-line"></i>
        </el-button>
      </div>
    </div>
    <el-card>
      <div class="row mt-4">
        <div class="col-3 col-lg-3 col-xl-3 mt-5">
          <img
            style="margin-left: 55px; width: 77%; margin-top: 50px"
            src="@/static/images/paradoxRectangle.png"
          />
        </div>
        <div class="col-9 col-lg-9 col-xl-9 mt-2">
          <h3 class="ml-4">{{ templateTitle }}</h3>
          <el-form
            class="bg-white text-info m-4"
            label-position="left"
            label-height="10px"
            label-width="190px"
            :rules="rules"
            ref="newProbation"
            :model="newProbation"
            style="width: 80%"
          >
            <el-form-item label="Employee Name" prop="employeeId">
              <el-select
                v-model="newProbation.employeeId"
                filterable
                placeholder="Employee Name"
                @change="changeEmployee($event)"
              >
                <el-option
                  v-for="item in employeesData"
                  :key="item.index"
                  :label="item.profile.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Job title">
              <el-input
                :value="newProbation.jobTitleNames"
                placeholder="Job Title"
                disabled
              ></el-input>
            </el-form-item>
            <el-form-item label="Line manager">
              <el-select
                v-model="newProbation.probationLineManagerId"
                filterable
                placeholder="Employee Name"
                @change="changeLineManager($event)"
              >
                <el-option
                  v-for="item in filteredEmployeeExcludeUserData"
                  :key="item.index"
                  :label="item.profile.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Period of appraisal" prop="endDay">
              <div>
                From
                <flat-pickr
                  v-model="newProbation.startDay"
                  :config="{
                    altInput: true,
                    altFormat: 'd-m-Y',
                    minDate: newProbation.joinDate,
                    dateFormat: 'Y-m-d',
                  }"
                  class="mr-2 ml-2"
                  placeholder="Select date"
                  name="date"
                  @input="getMonths()"
                  disabled
                />To
                <flat-pickr
                  v-model="newProbation.endDay"
                  :config="{
                    altInput: true,
                    altFormat: 'd-m-Y',
                    dateFormat: 'Y-m-d',
                    minDate: newProbation.startDay,
                  }"
                  class="mr-2 ml-2"
                  placeholder="Select date"
                  name="date"
                  @input="getMonths()"
                />
              </div>
            </el-form-item>
            <el-form-item
              label="End date of self-evaluation"
              prop="selfEvaluationEndDate"
            >
              <div>
                <flat-pickr
                  v-model="newProbation.selfEvaluationEndDate"
                  :config="{
                    altInput: true,
                    altFormat: 'd-m-Y',
                    minDate: newProbation.startDay,
                    maxDate: newProbation.endDay,
                    dateFormat: 'Y-m-d',
                  }"
                  class="mr-2 ml-2"
                  placeholder="Select date"
                  name="date"
                  @input="getMonths()"
                />
              </div>
            </el-form-item>
            <el-form-item label="Choose Template" prop="evaluationTemplate">
              <el-select
                v-model="newProbation.evaluationTemplate"
                @change="changeTitle($event)"
                placeholder="Choose Template"
                style="width: 70%"
              >
                <div
                  v-for="templateType in listTemplateType"
                  :key="templateType.id"
                >
                  <div class="background">
                    <strong class="ml-3">{{ templateType.name }}</strong>
                  </div>

                  <el-option
                    v-for="templateTypeDetail in templateType.data"
                    :key="templateTypeDetail.index"
                    :label="templateTypeDetail.name"
                    :value="templateTypeDetail.id"
                  ></el-option>
                </div>
              </el-select>
            </el-form-item>
          </el-form>
        </div>
      </div>
      <el-table
        v-show="competenceData.length"
        :data="competenceData"
        :header-cell-style="cellStyle"
        border
        header-cell-class-name="bg-header-table"
        highlight-current-row
        style="width: 95%; margin: 0 auto"
      >
        <el-table-column
          class="competence-header"
          fixed
          label="Competencies"
          width="450"
        >
          <template slot-scope="scope">
            <span class="break-work">{{ scope.row.competence }}</span>
          </template>
        </el-table-column>
        <div
          v-for="(col, index) in competenceAssessorRoles"
          :key="index"
          class="d-none"
        >
          <el-table-column :prop="col" :label="col">
            <el-table-column
              :render-header="(h, obj) => renderHeader(h, obj, col)"
            >
              <el-table-column label="Score" align="center" width="240">
                <template slot-scope="scope">
                  <div v-if="scope.row.assessor_roles[col]">
                    <el-radio-group
                      v-model="scope.row.assessor_roles[col].score"
                      :disabled="
                        checkIsAdmin
                          ? !isEdit
                          : !(scope.row.assessor_roles[col].assessor === userId)
                      "
                    >
                      <el-radio class="custom-radio" :label="1"></el-radio>
                      <el-radio class="custom-radio" :label="2"></el-radio>
                      <el-radio class="custom-radio" :label="3"></el-radio>
                      <el-radio class="custom-radio" :label="4"></el-radio>
                      <el-radio class="custom-radio" :label="5"></el-radio>
                    </el-radio-group>
                  </div>
                </template>
              </el-table-column>
              <el-table-column
                prop="comment"
                label="Comments"
                width="340"
                align="center"
              >
                <template slot-scope="scope">
                  <div v-if="scope.row.assessor_roles[col]">
                    <el-input
                      type="textarea"
                      placeholder="Please input"
                      v-model="scope.row.assessor_roles[col].comments"
                      :disabled="
                        checkIsAdmin
                          ? !isEdit
                          : !(scope.row.assessor_roles[col].assessor === userId)
                      "
                      class="break-work"
                    ></el-input>
                  </div>
                </template>
              </el-table-column>
            </el-table-column>
          </el-table-column>
        </div>
      </el-table>
      <br />
      <br />
      <el-table
        v-show="overCmtData.length"
        :data="overCmtData"
        :header-cell-style="cellStyle"
        border
        header-cell-class-name="bg-header-table"
        highlight-current-row
        style="width: 85%; margin: 0 auto"
      >
        <el-table-column
          prop="overCmt"
          label="Overall comments"
          width="450"
          fixed
        >
          <template slot-scope="scope">
            <span style="word-break: break-word">{{
              scope.row.overall_comment.term
            }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Score" align="center" width="250">
          <template slot-scope="scope">
            <el-radio-group
              v-model="scope.row.score"
              :disabled="
                checkIsAdmin ? !isEdit : !(scope.row.assessor === userId)
              "
            >
              <el-radio class="custom-radio" :label="1"></el-radio>
              <el-radio class="custom-radio" :label="2"></el-radio>
              <el-radio class="custom-radio" :label="3"></el-radio>
              <el-radio class="custom-radio" :label="4"></el-radio>
              <el-radio class="custom-radio" :label="5"></el-radio>
            </el-radio-group>
          </template>
        </el-table-column>
        <el-table-column
          prop="comment"
          label="Comments"
          width="350"
          align="center"
        >
          <template slot-scope="scope">
            <el-input
              placeholder="Please input"
              type="textarea"
              v-model="scope.row.comments"
              :disabled="
                checkIsAdmin ? !isEdit : !(scope.row.assessor === userId)
              "
              class="break-work"
            ></el-input>
          </template>
        </el-table-column>
        <el-table-column
          prop="assessor"
          label="Assessor"
          width="350"
          align="center"
        >
          <template slot-scope="scope">
            <el-select v-model="scope.row.assessor" placeholder="Employee Name">
              <el-option
                v-for="item in filterEmployee(scope.row.overall_comment_role)"
                :key="item.index"
                :label="item.profile.name"
                :value="item.id"
              ></el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="Role" width="350" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="Please input"
              v-model="scope.row.overall_comment_role"
              disabled
            ></el-input>
          </template>
        </el-table-column>
      </el-table>
      <br />
      <br />
      <br />

      <div class="outcome" v-show="showOutCome">
        <el-row>
          <el-col :offset="1">
            <h3>Outcome</h3>
            <br />
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="5" :offset="1">
            <div class="mb-4 ml-2">
              <span>Signing official labor constract:</span>
            </div>
          </el-col>
          <el-col class="radio-block">
            <el-radio v-model="isSignedConstract" :label="true">Yes</el-radio>
          </el-col>
          <el-col class="radio-block">
            <el-radio v-model="isSignedConstract" :label="false">No</el-radio>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="5" :offset="1">
            <div class="mb-4 ml-2">
              <span class="mr-3">Labor contract term:</span>
            </div>
          </el-col>
          <el-col class="left-term-block">
            <el-row type="flex">
              <el-col :span="10">
                <el-radio v-model="newProbation.isCheckedTerm" :label="true"
                  >Definite Term</el-radio
                >
              </el-col>
              <el-col :span="15">
                <el-input
                  size="small"
                  placeholder="Term (months)"
                  v-model="newProbation.term"
                  class="term-input"
                  disabled
                ></el-input>
              </el-col>
            </el-row>
          </el-col>
          <el-col class="right-term-block">
            <el-radio v-model="newProbation.isCheckedTerm" :label="false"
              >Indefinite term</el-radio
            >
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="5" :offset="1">
            <div class="mb-4 ml-2">
              <span class="mr-3">Other actions and updates:</span>
            </div>
          </el-col>
          <el-col :span="5">
            <el-input
              size="small"
              placeholder="Please input text"
              width="60%"
              v-model="newProbation.otherUpdateAction"
            ></el-input>
          </el-col>
        </el-row>
        <el-row :gutter="10">
          <el-col :span="5" :offset="1">
            <div class="mb-4 ml-2">
              <span class="mr-3">Director's approval:</span>
            </div>
          </el-col>
          <el-col class="radio-block">
            <el-radio v-model="newProbation.approved" :label="true"
              >Approve</el-radio
            >
          </el-col>
          <el-col class="radio-block">
            <el-radio v-model="newProbation.approved" :label="false"
              >Disapprove</el-radio
            >
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import moment from "moment";
import "vue-cal/dist/vuecal.css";
import "flatpickr/dist/flatpickr.css";
import flatPickr from "vue-flatpickr-component";
import ProbationService from "@/services/probation_management/probation.service";
import GetUserService from "../../services/user/getUser";
import UserService from "../../services/user/user";
import _ from "lodash";
import { generateNewProbationForm } from "../../utils/excelNewProbation";
import { ASSESSOR_ROLE } from "@/const/probationDetail";
import { mapGetters } from "vuex";

export default {
  name: "NewProbation",
  components: {
    flatPickr,
  },
  data() {
    return {
      rules: {
        employeeId: [
          {
            required: true,
            message: "Please select Employee Name!",
            trigger: "change",
          },
        ],
        evaluationTemplate: [
          {
            required: true,
            message: "Please select Evaluation Template!",
            trigger: "change",
          },
        ],
        endDay: [
          {
            required: true,
            message: "Please choose day",
            trigger: "change",
          },
        ],
      },
      newProbation: {
        employeeId: "",
        employeeName: "",
        jobTitleNames: "",
        evaluationTemplate: "",
        endDay: null,
        startDay: null,
        templateId: null,
        joinDate: null,
        selfEvaluationEndDate: null,
        probationLineManagerId: null,
        probationLineManagerName: "",
        otherUpdateAction: "",
        approved: true,
        isCheckedTerm: true,
        term: "",
      },
      userId: localStorage.getItem("user_id"),
      checkIsAdmin: JSON.parse(localStorage.getItem("is_admin")),
      employeesData: [],
      filteredEmployeeExcludeUserData: [],
      templateTitle: "Choose Template",
      listTemplate: [],
      listTemplateType: [],
      evaluationTemplate: "",
      notFoundText: "Not Found",
      competenceAssessorRoles: "",
      assessorCompetence: "",
      evaluationCompetence: [],
      competenceTitle: "competencies",
      overallCmtTitle: "overall_comments",
      showOutCome: false,
      isSignedConstract: false,
      competenceData: [],
      overCmtData: [],
      isEdit: true,
      selfRole: "Self-evaluation",
      lineManagerRole: "Line Manager",
      isRenderHeader: false,
      lastEmployeeSearching: "",
      cellStyle() {
        return {
          padding: "5px 0 !important",
        };
      },
      timer: 1,
    };
  },
  computed: {
    ...mapGetters("user", ["allUsers"]),
  },
  created() {
    this.lineManagerRole = ASSESSOR_ROLE.lineManagerRole;
    this.selfRole = ASSESSOR_ROLE.selfRole;
    this.getAllActiveTemplate();
    this.employeesData = this.allUsers;
  },
  methods: {
    renderHeader(createElement, { column, $index }, role) {
      let filterEmployee = this.filterEmployee(role);
      let element = createElement("div", [
        createElement(
          "el-select",
          {
            props: {
              value: this.assessorCompetence[role]["assessor"],
            },
            on: {
              change: (value) => {
                if (role === this.lineManagerRole)
                  this.newProbation.probationLineManagerId = value;
                if (this.assessorCompetence)
                  this.assessorCompetence[role]["assessor"] = value;
              },
            },
          },
          filterEmployee.map((item) => {
            return createElement("el-option", {
              props: {
                key: item.index,
                label: item.profile.name,
                value: item.id,
              },
            });
          })
        ),
      ]);
      element.fnScopeId = this.$options._scopeId;
      element.fnContext = this;
      return element;
    },
    filterEmployee(role) {
      if (role === this.selfRole) {
        return this.employeesData.filter(
          (el) => el.id === this.newProbation?.employeeId
        );
      }
      if (role === this.lineManagerRole) {
        return this.filteredEmployeeExcludeUserData;
      }
      return this.employeesData.filter((el) =>
        el.title ? el.title.title?.trim() === role?.trim() : false
      );
    },

    formatDate(value) {
      if (value) {
        return moment(String(value)).format("MM-DD-YYYY");
      }
    },
    async changeTitle(templateId) {
      if (templateId) {
        this.assessorCompetence = "";
        this.newProbation.templateId = templateId;
        await this.getListEvaluationAssessorRole(templateId);
        await this.changeTableData(
          templateId,
          this.newProbation.employeeId,
          this.newProbation.probationLineManagerId
        );
        const findTemplateObj = this.listTemplate.find(
          (item) => item.id === templateId
        );
        this.templateTitle = findTemplateObj.name;
        this.showOutCome = true;
      }
    },
    async changeTableData(
      templateId = null,
      employeeId = null,
      probationLineManagerId = null
    ) {
      await this.getListEvaluationCompetence(
        templateId,
        employeeId,
        probationLineManagerId
      );
      await this.getListEvaluationOverallCmt(
        templateId,
        employeeId,
        probationLineManagerId
      );
    },
    async getListEvaluationAssessorRole(templateId) {
      this.competenceAssessorRoles = "";
      const res = await ProbationService.getEvaluationCompetencesAssessorRole(
        templateId
      );
      this.assessorCompetence = Object.assign(
        {},
        ...res.data.map((key) => ({ [key]: "" }))
      );
      this.competenceAssessorRoles = [...res.data];
    },
    async getListEvaluationCompetence(
      templateId,
      employeeId,
      probationLineManagerId
    ) {
      const res = await ProbationService.getEvaluationCompetences(
        templateId,
        employeeId,
        probationLineManagerId
      );
      this.competenceData = res.data;
      if (Object.keys(this.assessorCompetence).length) {
        this.addAssessorCompetence(res.data);
      }
    },
    async getListEvaluationOverallCmt(
      templateId,
      employeeId,
      probationLineManagerId
    ) {
      const res = await ProbationService.getEvaluationOverall(
        templateId,
        employeeId,
        probationLineManagerId
      );
      this.overCmtData = res.data;
    },
    addAssessorCompetence(competenceData) {
      let allCompetenceAssessor = competenceData[0].all_assessor;
      this.assessorCompetence = _.merge(
        this.assessorCompetence,
        allCompetenceAssessor
      );
    },
    handleDataAPIUserTitle(userData) {
      let uniqueUser = _.omit(userData[0], ["title", "title_name"]);
      let groupTitle = userData.map((item) => ({
        title: item.title,
        title_name: item.title_name,
      }));
      uniqueUser = { ...uniqueUser, groupTitle };
      return uniqueUser;
    },
    async changeEmployee(employeeId) {
      let res = await GetUserService.getUserIncludeLineManagerName(employeeId);
      const user = this.handleDataAPIUserTitle(res.data);
      await this.filteredEmployeeExcludeUserId(employeeId);
      if (this.newProbation.templateId)
        await this.changeTableData(
          this.newProbation.templateId,
          employeeId,
          user.line_manager_user_id
        );
      this.newProbation.employeeName = user.user_name;
      this.newProbation.jobTitleNames = user.groupTitle
        .map((e) => e.title_name)
        .join(", ");
      this.newProbation.probationLineManagerId = user.line_manager_user_id;
      this.newProbation.probationLineManagerName = user.line_manage_name;
      this.newProbation.startDay = user.join_date;
    },

    async changeLineManager() {
      this.newProbation.probationLineManagerName = this.employeesData.find(
        (employee) => employee.id === this.newProbation.probationLineManagerId
      )?.profile.name;
      await this.changeTableData(
        this.newProbation.templateId,
        this.newProbation.employeeId,
        this.newProbation.probationLineManagerId
      );
    },
    async filteredEmployeeExcludeUserId(userId) {
      let res = await UserService.getAllEmployeesExcludeUserId(userId);
      this.filteredEmployeeExcludeUserData = res.data;
    },
    getMonths() {
      let endDay = new Date(this.newProbation.endDay);
      let startDay = new Date(this.newProbation.startDay);
      if (this.newProbation.endDay && this.newProbation.startDay) {
        let months =
          endDay.getMonth() -
          startDay.getMonth() +
          12 * (endDay.getFullYear() - startDay.getFullYear());
        if (months) this.newProbation.term = months + " months";
        else {
          let days =
            (endDay.getTime() - startDay.getTime()) / (1000 * 3600 * 24);
          this.newProbation.term = days + " days";
        }
      }
    },
    async getAllActiveTemplate() {
      const res = await ProbationService.getAllActiveTemplate();
      this.listTemplate = res.data;
      this.listTemplateType = this.handleDataAPITemplate(res.data);
    },
    handleDataAPITemplate(dataAPI) {
      const uniqueGroup = _.uniqBy(dataAPI, "type");
      return uniqueGroup.map((template) => {
        const newData = {
          group: template.type,
          name: template.name_type,
          data: [],
        };
        dataAPI.forEach((item) => {
          if (item.type === template.type) {
            newData.data.push(item);
          }
        });
        return newData;
      });
    },
    async changeCompetenceStructure(competencies) {
      let output = [];
      if (competencies.length) {
        competencies.forEach((item) => {
          let myData = {};
          myData = Object.keys(item["assessor_roles"]).map((key) => {
            item["assessor_roles"][key]["evaluation_template_competence"] =
              item["assessor_roles"][key]["evaluation_competence"];
            item["assessor_roles"][key][
              "evaluation_template_competence_assessor_role"
            ] = item["assessor_roles"][key]["id"];
            item["assessor_roles"][key]["assessor"] =
              this.assessorCompetence[key]["assessor"];
            return item["assessor_roles"][key];
          });
          output = output.concat(myData);
        });
      }
      return await Promise.all(output);
    },
    async saveData(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          this.newProbation.competencies = await this.changeCompetenceStructure(
            this.competenceData
          );
          const newProbationObj = {
            self_evaluation_end_date: this.newProbation.selfEvaluationEndDate,
            probation_line_manager: this.newProbation.probationLineManagerId,
            probation_end_date: this.newProbation.endDay,
            employee: this.newProbation.employeeId,
            evaluation_template: this.newProbation.templateId,
            competencies: this.newProbation.competencies,
            overall_comments: this.overCmtData,
            signing_official_labor_contract: this.isSignedConstract,
            labor_contract_term: this.newProbation.isCheckedTerm
              ? this.newProbation.term
              : "",
            other_actions_and_updates: this.newProbation.otherUpdateAction,
            approved: this.newProbation.approved,
          };
          if (!this.newProbation.endDay)
            this.$toast.error("Please choose end day");
          await ProbationService.create(newProbationObj)
            .then((res) => {
              if (res.status === 201) {
                this.$nextTick(() => {
                  this.$toast.success("Create new probation successfully");
                });
                this.$router.push("/evaluations");
              }
            })
            .catch((e) => {
              const error = e.response.data.error;
              this.$toast.error(error);
            });
        }
      });
    },
    back() {
      this.$router.push("/evaluations");
    },
    exportNewProbation() {
      generateNewProbationForm(this);
    },
  },
};
</script>
<style lang="scss">
@import "./probationDetail.scss";
</style>
