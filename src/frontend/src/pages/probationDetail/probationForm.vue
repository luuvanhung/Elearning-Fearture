<template>
  <div class="bg-light">
    <div v-if="isLoadingMask" class="lmask" ref="loading-mask"></div>
    <div :style="{ visibility: !isLoadingMask ? 'visible' : 'hidden' }">
      <div class="row m-4">
        <div
          class="col-12 col-lg-6 col-xl-6 ml-auto justify-xl-end d-flex justify-content-end"
        >
          <ReminderModal
            class="mr-2"
            :probationEndDate="probationDetail.probation_end_date"
            @maxReminderDate="getMaxReminderDate"
          />
          <el-button type="primary" @click="exportToExcel">
            <download-excel
              class="btn btn-info"
              worksheet="My Worksheet"
              title="Click to export excel"
              name="user.xls"
            >
              <font-awesome-icon :icon="['fas', 'file-export']" />
              Export
            </download-excel>
          </el-button>
          <el-button type="secondary" @click="dialogInvite = true">
            <font-awesome-icon :icon="['fas', 'file-import']" />
            <span class="ml-2">Import</span>
          </el-button>
          <el-button type="info" @click="updatedData()">
            <font-awesome-icon :icon="['fas', 'save']" />
            <span class="ml-2">Update</span>
          </el-button>
          <el-button type="danger" @click="back()">
            <font-awesome-icon :icon="['fas', 'step-backward']" />
            <span class="ml-2">Discard</span
            ><em class="fa-solid fa-arrow-left-long-to-line"></em>
          </el-button>
        </div>
      </div>
      <el-card>
        <div class="row mt-4">
          <div class="col-3 col-lg-3 col-xl-3 mt-5">
            <img
              style="margin-left: 55px; width: 77%; margin-top: 50px"
              src="@/static/images/paradoxRectangle.png"
              alt="Paradox"
            />
          </div>
          <div class="col-9 col-lg-9 col-xl-9 mt-2">
            <h3 class="ml-4">
              {{ evaluationTemplateTitle }}
            </h3>

            <el-form
              class="bg-white text-info m-4"
              label-position="left"
              label-height="10px"
              label-width="190px"
              style="width: 80%"
            >
              <el-form-item label="Employee Name">
                <el-input
                  v-model="employeeName"
                  placeholder="Employee Name"
                  disabled
                ></el-input>
              </el-form-item>
              <el-form-item label="Job title">
                <el-input
                  :value="jobTitle"
                  placeholder="Job Title"
                  disabled
                ></el-input>
              </el-form-item>
              <el-form-item label="Line manager">
                <el-select
                  v-model="probationLineManager"
                  placeholder="Employee Name"
                  :disabled="permitIfOneOfAllScope(['probation:create'])"
                >
                  <el-option
                    v-for="item in filteredEmployeeExcludeUserData"
                    :key="item.index"
                    :label="item.profile.name"
                    :value="item.id"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="Period of appraisal">
                <div>
                  From
                  <flat-pickr
                    v-model="startDay"
                    :config="{
                      altInput: true,
                      altFormat: 'd-m-Y',
                      minDate: this.joinDate,
                      dateFormat: 'Y-m-d',
                    }"
                    class="mr-2 ml-2"
                    placeholder="Select date"
                    name="date"
                    @input="getMonths()"
                    disabled
                  />
                  To
                  <flat-pickr
                    v-model="endDay"
                    :disabled="permitIfOneOfAllScope(['probation:create'])"
                    :config="{
                      altInput: true,
                      altFormat: 'd-m-Y',
                      dateFormat: 'Y-m-d',
                      minDate: startDay,
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
                    v-model="selfEvaluationEndDate"
                    :config="{
                      altInput: true,
                      altFormat: 'd-m-Y',
                      minDate: startDay,
                      maxDate: endDay,
                      dateFormat: 'Y-m-d',
                    }"
                    class="mr-2 ml-2"
                    placeholder="Select date"
                    name="date"
                    @input="getMonths()"
                    :disabled="permitIfOneOfAllScope(['probation:create'])"
                  />
                </div>
              </el-form-item>
              <el-form-item
                class="choose-template-select"
                label="Choose Template"
              >
                <el-select
                  v-model="evaluationTemplate"
                  placeholder="Choose Template"
                  @change="changeTitle($event)"
                  disabled
                >
                  <el-option
                    v-for="item in listEvaluationTemplate"
                    :key="item.index"
                    :label="item"
                    :value="item"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </div>
        <el-table
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
              <span class="break-work">{{
                scope.row.evaluation_template_competence.competence
              }}</span>
            </template>
          </el-table-column>
          <div
            v-for="(col, index) in competenceAssessorRoles"
            :key="index"
            style="display: none"
          >
            <el-table-column :prop="col" :label="col">
              <el-table-column
                :render-header="(h, obj) => renderHeader(h, obj, col)"
              >
                <el-table-column label="Score" align="center" width="250">
                  <template slot-scope="scope">
                    <div
                      v-if="
                        scope.row.evaluation_template_competence_assessor_role[
                          col
                        ]
                      "
                    >
                      <el-radio-group
                        v-model="
                          scope.row
                            .evaluation_template_competence_assessor_role[col]
                            .score
                        "
                        :disabled="
                          checkIsAdmin
                            ? !isEdit
                            : checkEvaluation(
                                scope.row
                                  .evaluation_template_competence_assessor_role[
                                  col
                                ].assessor_id
                              )
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
                    <div
                      v-if="
                        scope.row.evaluation_template_competence_assessor_role[
                          col
                        ]
                      "
                    >
                      <el-input
                        type="textarea"
                        placeholder="Please input"
                        v-model="
                          scope.row
                            .evaluation_template_competence_assessor_role[col]
                            .comments
                        "
                        :disabled="
                          checkIsAdmin
                            ? !isEdit
                            : checkEvaluation(
                                scope.row
                                  .evaluation_template_competence_assessor_role[
                                  col
                                ].assessor_id
                              )
                        "
                        class="break-work"
                      >
                      </el-input>
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
                scope.row.evaluation_template_overall_comment.term
              }}</span>
            </template>
          </el-table-column>
          <el-table-column label="Score" align="center" width="250">
            <template slot-scope="scope">
              <el-radio-group
                v-model="scope.row.score"
                :disabled="
                  checkIsAdmin
                    ? !isEdit
                    : checkEvaluation(scope.row.assessor_id)
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
                  checkIsAdmin
                    ? !isEdit
                    : checkEvaluation(scope.row.assessor_id)
                "
                class="break-work"
              >
              </el-input>
            </template>
          </el-table-column>
          <el-table-column
            prop="assessor"
            label="Assessor"
            width="350"
            align="center"
          >
            <template slot-scope="scope">
              <el-select
                v-model="scope.row.assessor_id"
                placeholder="Employee Name"
                :disabled="
                  scope.row.evaluation_template_overall_comment_assessor_role
                    .overall_comment_role === lineManagerRole
                    ? true
                    : permitIfOneOfAllScope(['probation:create'])
                "
              >
                <el-option
                  v-for="item in filterEmployee(
                    scope.row.evaluation_template_overall_comment_assessor_role
                      .overall_comment_role
                  )"
                  :key="item.index"
                  :label="item.profile.name"
                  :value="item.id"
                >
                </el-option>
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="Role" width="350" align="center">
            <template slot-scope="scope">
              <el-input
                placeholder="Please input"
                v-model="
                  scope.row.evaluation_template_overall_comment_assessor_role
                    .overall_comment_role
                "
                disabled
              >
              </el-input>
            </template>
          </el-table-column>
        </el-table>
        <br />
        <br />
        <br />
        <div class="outcome">
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
              <el-radio
                :disabled="permitIfOneOfAllScope(['probation:create'])"
                v-model="isSignedConstract"
                :label="true"
                >Yes
              </el-radio>
            </el-col>
            <el-col class="radio-block">
              <el-radio
                :disabled="permitIfOneOfAllScope(['probation:create'])"
                v-model="isSignedConstract"
                :label="false"
                >No
              </el-radio>
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
                  <el-radio
                    :disabled="permitIfOneOfAllScope(['probation:create'])"
                    v-model="isCheckedTerm"
                    :label="true"
                    >Definite Term
                  </el-radio>
                </el-col>
                <el-col :span="14">
                  <el-input
                    size="small"
                    placeholder="Term (months)"
                    v-model="term"
                    class="term-input"
                    disabled
                  >
                  </el-input>
                </el-col>
              </el-row>
            </el-col>
            <el-col class="right-term-block">
              <el-radio
                :disabled="permitIfOneOfAllScope(['probation:create'])"
                v-model="isCheckedTerm"
                :label="false"
                >Indefinite term
              </el-radio>
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
                :disabled="permitIfOneOfAllScope(['probation:create'])"
                size="small"
                placeholder="Please input text"
                width="60%"
                v-model="otherUpdateAction"
              >
              </el-input>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="5" :offset="1">
              <div class="mb-4 ml-2">
                <span class="mr-3">Director's approval:</span>
              </div>
            </el-col>
            <el-col class="radio-block">
              <el-radio
                :disabled="permitIfOneOfAllScope(['probation:create'])"
                v-model="approved"
                :label="true"
                >Approve
              </el-radio>
            </el-col>
            <el-col class="radio-block">
              <el-radio
                :disabled="permitIfOneOfAllScope(['probation:create'])"
                v-model="approved"
                :label="false"
                >Disapprove
              </el-radio>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import "vue-cal/dist/vuecal.css";
import "flatpickr/dist/flatpickr.css";
import flatPickr from "vue-flatpickr-component";
import ProbationService from "@/services/probation_management/probation.service";
import GetUserService from "../../services/user/getUser";
import _ from "lodash";
import { mapGetters, mapActions } from "vuex";
import ReminderModal from "./reminder/reminderModal";
import UserService from "../../services/user/user";
import { generateProbationForm } from "@/utils/excel";
import { ASSESSOR_ROLE } from "@/const/probationDetail";

export default {
  name: "ProbationForm",
  components: {
    flatPickr,
    ReminderModal,
  },
  computed: {
    ...mapGetters({
      tokenInfo: "scope/tokenInfo",
      allUsers: "user/allUsers",
    }),
  },
  data() {
    return {
      userId: localStorage.getItem("user_id"),
      checkIsAdmin: JSON.parse(localStorage.getItem("is_admin")),
      maxReminderDate: "",
      term: "",
      startDay: null,
      endDay: null,
      joinDate: null,
      selfEvaluationEndDate: null,
      employeeName: "",
      employeeId: "",
      filteredEmployeeExcludeUserData: [],
      jobTitle: "",
      result: [],
      isSignedConstract: false,
      isCheckedTerm: true,
      approved: true,
      evaluationTemplateTitle: "Choose Template",
      listEvaluationTemplate: [],
      competenceData: [],
      probationDetail: {},
      listJobTitle: [],
      overCmtData: [],
      lineManager: "",
      lineManagerUserId: "",
      probationLineManager: "",
      evaluationTemplate: "",
      evaluationTemplateId: "",
      competenceAssessorRoles: [],
      assessorCompetence: "123",
      isDisable: false,
      assessorRoleIndex: "",
      otherUpdateAction: "",
      profileTitle: "profile",
      employeesData: [],
      selfRole: "",
      lineManagerRole: "",
      isEdit: true,
      listEmployee: [],
      isLoadingMask: true,
      isSelfEvaluated: false,
      cellStyle() {
        return {
          padding: "5px 0 !important",
        };
      },
    };
  },
  async created() {
    this.lineManagerRole = ASSESSOR_ROLE.lineManagerRole;
    this.selfRole = ASSESSOR_ROLE.selfRole;
    await this.getCurrentProbation();
    setTimeout(this.disableMask, 500);
    await this.getAllEmployee();
    await this.getAllTitles();
    await this.setAllUsersList();
  },
  methods: {
    ...mapActions({ setAllUsersList: "user/setAllUsersList" }),
    getMaxReminderDate(data) {
      this.maxReminderDate = data;
    },
    checkEvaluation(assessorId) {
      let today = moment(new Date()).format("YYYY-MM-DD");
      if (assessorId === this.userId) {
        if (
          assessorId === this.employeeId ||
          this.isSelfEvaluated ||
          today > this.selfEvaluationEndDate
        )
          return false;
      }
      return true;
    },
    disableMask() {
      this.isLoadingMask = false;
    },
    renderHeader(createElement, { _column, _$index }, role) {
      let filterEmployee = this.filterEmployee(role);
      let element = createElement("div", [
        createElement(
          "el-select",
          {
            props: {
              value: this.assessorCompetence[role]["assessor"],
              disabled:
                role === this.lineManagerRole
                  ? true
                  : this.permitIfOneOfAllScope(["probation:create"]),
            },
            on: {
              input: (value) => {
                this.assessorCompetence[role]["assessor"] = value;
              },
              change: (value) => {
                this.competenceData.forEach((item) => {
                  if (
                    role in item.evaluation_template_competence_assessor_role
                  ) {
                    item.evaluation_template_competence_assessor_role[
                      role
                    ].assessor_id = value;
                  }
                });
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
    async getAllEmployee() {
      this.employeesData = this.allUsers;
    },
    async filteredEmployeeExcludeUserId(userId) {
      let res = await UserService.getAllEmployeesExcludeUserId(userId);
      this.filteredEmployeeExcludeUserData = res.data;
    },
    filterEmployee(role) {
      if (role) {
        if (role === this.selfRole) {
          return this.employeesData.filter(
            (el) => el.id === this.probationDetail.employee.id
          );
        }
        if (role === this.lineManagerRole) {
          return this.filteredEmployeeExcludeUserData;
        }
        return this.employeesData.filter((el) =>
          el.title ? el.title.title?.trim() === role.trim() : false
        );
      }
    },
    formatDate(value) {
      if (value) {
        return moment(String(value)).format("MM-DD-YYYY");
      }
    },
    changeTitle(event) {
      this.evaluationTemplateTitle = event;
    },
    async getCurrentProbation() {
      const res = await ProbationService.getProbation(this.$route.params.id);
      await this.getListEvaluationAssessorRole(res.data.evaluation_template.id);
      this.competenceData = await this.getCompetenceDataCombineAccessorRole(
        res.data.competencies
      );
      this.overCmtData = await res.data.overall_comments;
      this.probationDetail = res.data;
      this.isSelfEvaluated = res.data.is_self_evaluated;
      this.selfEvaluationEndDate = res.data.self_evaluation_end_date;
      this.otherUpdateAction = res.data.other_actions_and_updates;
      this.employeeName = res.data.employee.profile.name;
      this.employeeId = res.data.employee.id;
      this.startDay = res.data.employee.profile.join_date;
      this.endDay = res.data.probation_end_date;
      this.evaluationTemplate = res.data.evaluation_template.name;
      this.evaluationTemplateTitle = res.data.evaluation_template.name;
      this.evaluationTemplateId = res.data.evaluation_template.id;
      this.jobTitle = res.data.employee?.title.map((e) => e.title).join(", ");
      this.isSignedConstract = res.data.signing_official_labor_contract;
      this.isCheckedTerm = !!res.data.labor_contract_term;
      this.approved = res.data.approved;
      this.probationLineManager = res.data.probation_line_manager?.id;
      if (res.data.employee.profile.line_manager) {
        this.lineManagerUserId = res.data.employee.profile.line_manager_user_id;
      }
      await this.filteredEmployeeExcludeUserId(this.employeeId);
    },

    async getAllTitles() {
      const res = await GetUserService.getAllTitles();
      this.listJobTitle = res.data;
    },
    async getListEvaluationAssessorRole(templateId) {
      const res = await ProbationService.getEvaluationCompetencesAssessorRole(
        templateId
      );
      this.assessorCompetence = Object.assign(
        {},
        ...res.data.map((key) => ({ [key]: { assessor: "" } }))
      );
      this.competenceAssessorRoles = res.data;
    },
    async getCompetenceDataCombineAccessorRole(competenceData) {
      let output = [];
      if (competenceData.length) {
        competenceData.forEach((item) => {
          let assessorRoleItem = {
            comments: item.comments,
            score: item.score,
            assessor: item.assessor ? item.assessor : "",
            assessor_id: item.assessor ? item.assessor.id : "",
            id: item.id,
            competence_role:
              item.evaluation_template_competence_assessor_role.assessor_role,
          };
          let changeKey =
            item.evaluation_template_competence_assessor_role.assessor_role;
          let existingArr = output.filter(function (v) {
            return (
              v.evaluation_template_competence.id ===
              item.evaluation_template_competence.id
            );
          });
          if (existingArr.length) {
            let existingIndex = output.indexOf(existingArr[0]);
            output[existingIndex].evaluation_template_competence_assessor_role[
              `${changeKey}`
            ] = assessorRoleItem;
            output[existingIndex] = _.pick(output[existingIndex], [
              "evaluation_template_competence_assessor_role",
              "evaluation_template_competence",
            ]);
            output[existingIndex].evaluation_template_competence_assessor_role =
              _.pickBy(
                output[existingIndex]
                  .evaluation_template_competence_assessor_role,
                _.isPlainObject
              );
          } else {
            item.evaluation_template_competence_assessor_role[`${changeKey}`] =
              assessorRoleItem;
            item = _.pick(item, [
              "evaluation_template_competence_assessor_role",
              "evaluation_template_competence",
            ]);
            item.evaluation_template_competence_assessor_role = _.pickBy(
              item.evaluation_template_competence_assessor_role,
              _.isPlainObject
            );
            output.push(item);
          }
          if (Object.keys(this.assessorCompetence).length) {
            this.assessorCompetence[`${changeKey}`]["assessor"] =
              assessorRoleItem.assessor?.id;
          }
        });
      }

      return Promise.all(output);
    },
    getMonths() {
      let endDay = new Date(this.endDay);
      let startDay = new Date(this.startDay);
      let months =
        endDay.getMonth() -
        startDay.getMonth() +
        12 * (endDay.getFullYear() - startDay.getFullYear());
      if (months) this.term = months + " months";
      else {
        let days = (endDay.getTime() - startDay.getTime()) / (1000 * 3600 * 24);
        this.term = days + " days";
      }
    },
    async changeCompetenceStructure(competencies) {
      let output = [];
      if (competencies.length) {
        competencies.forEach((item) => {
          let myData = {};
          myData = Object.keys(
            item["evaluation_template_competence_assessor_role"]
          ).map((key) => {
            return item["evaluation_template_competence_assessor_role"][key];
          });
          output = output.concat(myData);
        });
      }

      return Promise.all(output);
    },
    async updatedData() {
      this.probationDetail.competencies = await this.changeCompetenceStructure(
        this.competenceData
      );
      const updatedProbationObj = {
        ...this.probationDetail,
        is_self_evaluated: this.isSelfEvaluated,
        self_evaluation_end_date: this.selfEvaluationEndDate,
        probation_end_date: this.endDay,
        competencies: this.probationDetail.competencies,
        overall_comments: this.probationDetail.overall_comments,
        signing_official_labor_contract: this.isSignedConstract,
        labor_contract_term: this.isCheckedTerm ? this.term : "",
        other_actions_and_updates: this.otherUpdateAction,
        approved: this.approved,
        employee_id: this.probationDetail.employee.id,
        probation_line_manager: this.probationLineManager,
      };
      if (
        new Date(this.endDay).getTime() <
        new Date(this.maxReminderDate).getTime()
      )
        return this.$toast.error(
          "The probation end date is not smaller than reminder dates"
        );
      await ProbationService.update(updatedProbationObj, this.$route.params.id)
        .then((res) => {
          if (res.status === 200) {
            this.$nextTick(() => {
              this.$toast.success("Updated Successfully");
            });
            this.$router.push("/evaluations");
          }
        })
        .catch((e) => {
          const error = e.response.data.error;
          this.$toast.error(error);
        });
    },
    permitIfOneOfAllScope(scopes) {
      return scopes.some((n) => {
        return this.tokenInfo["scope"].indexOf(n) === -1;
      });
    },
    back() {
      this.$router.push("/evaluations");
    },
    exportToExcel() {
      generateProbationForm(this);
    },
  },
};
</script>
<style lang="scss" scoped>
@import "./probationDetail.scss";
</style>
