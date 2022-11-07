<template>
  <div class="import-excel-container">
    <el-form>
      <div class="probation-import">
        <div class="d-flex">
          <div class="d-flex align-items-center">
            <router-link to="/evaluations/new">
              <el-button
                style="float: left; font-size: 15px; font-weight: bold"
                icon="el-icon-arrow-left"
                type="primary"
                >Back
              </el-button>
            </router-link>
          </div>
          <div class="d-flex align-items-center choose-template">
            <el-form-item
              class="ml-3"
              label="Choose Template"
              prop="evaluationTemplate"
            >
              <el-select
                v-model="evaluationTemplate"
                placeholder="Choose Template"
                style="width: 400px"
                size="medium"
                @change="changeTemplate($event)"
              >
                <el-option
                  v-for="item in listTemplate"
                  :key="item.index"
                  :label="item.name"
                  :value="item.id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </div>
        <div>
          <el-upload
            action=""
            :on-success="handleImportExcel"
            :multiple="false"
            :show-file-list="false"
            accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            style="float: right"
          >
            <el-button
              style="font-size: 15px; font-weight: bold; float: right"
              icon="el-icon-document-add"
              type="primary"
              >Import from Excel
            </el-button>
          </el-upload>
        </div>
      </div>
    </el-form>
    <div class="bg-light">
      <el-card
        v-if="listInfo.length && listCompetence.length && listOverall.length"
      >
        <div class="row mt-4">
          <div class="col-3 col-lg-3 col-xl-3 mt-5">
            <img
              style="margin-left: 55px; width: 77%; margin-top: 50px"
              src="@/static/images/paradoxRectangle.png"
            />
          </div>
          <div class="col-9 col-lg-9 col-xl-9 mt-2">
            <h3 class="ml-4"></h3>

            <el-form
              class="bg-white text-info m-4"
              label-position="left"
              label-height="10px"
              label-width="170px"
              ref="newProbation"
              style="width: 80%"
            >
              <div v-for="(info, index) in listInfo" :key="index">
                <el-form-item :label="info.title">
                  <el-input :value="info.value" disabled> </el-input>
                </el-form-item>
              </div>
            </el-form>
          </div>
        </div>
        <el-table
          :data="listCompetence"
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
              <span class="break-work">{{ scope.row.name }}</span>
            </template>
          </el-table-column>
          <div
            v-for="(col, index) in listExcelCompetenceRole"
            :key="index"
            class="d-none"
          >
            <el-table-column :prop="col" :label="col">
              <el-table-column label="Score" align="center" width="240">
                <template slot-scope="scope">
                  <div v-if="scope.row[col]">
                    <el-radio-group v-model="scope.row[col].score" disabled>
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
                  <div v-if="scope.row[col]">
                    <el-input
                      type="textarea"
                      placeholder="Please input"
                      v-model="scope.row[col].comment"
                      class="break-work"
                      disabled
                    >
                    </el-input>
                  </div>
                </template>
              </el-table-column>
            </el-table-column>
          </div>
        </el-table>
        <br />
        <br />
        <el-table
          :data="listOverall"
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
              <span style="word-break: break-word">{{ scope.row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column label="Score" align="center" width="240">
            <template slot-scope="scope">
              <el-radio-group :value="scope.row.score">
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
              <span style="word-break: break-word">{{
                scope.row.comment
              }}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="assessor"
            label="Assessor"
            width="350"
            align="center"
          >
            <template slot-scope="scope">
              <span style="word-break: break-word">{{
                scope.row.assessor
              }}</span>
            </template>
          </el-table-column>
          <el-table-column label="Role" width="350" align="center">
            <template slot-scope="scope">
              <span style="word-break: break-word">{{ scope.row.role }}</span>
            </template>
          </el-table-column>
        </el-table>

        <div class="outcome" v-show="listOutcome.length">
          <el-row>
            <el-col :offset="1">
              <h3>Outcome</h3>
              <br />
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="5" :offset="1">
              <div class="mb-4 ml-2">
                <span>{{ listOutcome[0].title }}:</span>
              </div>
            </el-col>
            <el-col class="radio-block">
              <el-radio v-model="isSignedConstract" :label="true"
                >Yes
              </el-radio>
            </el-col>
            <el-col class="radio-block">
              <el-radio v-model="isSignedConstract" :label="false"
                >No
              </el-radio>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="5" :offset="1">
              <div class="mb-4 ml-2">
                <span class="mr-3">{{ listOutcome[1].title }}:</span>
              </div>
            </el-col>
            <el-col class="left-term-block">
              <el-row type="flex">
                <el-col :span="10">
                  <el-radio v-model="isCheckedTerm" :label="true"
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
              <el-radio v-model="isCheckedTerm" :label="false"
                >Indefinite term
              </el-radio>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="5" :offset="1">
              <div class="mb-4 ml-2">
                <span class="mr-3">{{ listOutcome[2].title }}:</span>
              </div>
            </el-col>
            <el-col :span="5">
              <el-input
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
                <span class="mr-3">{{ listOutcome[3].title }}:</span>
              </div>
            </el-col>
            <el-col class="radio-block">
              <el-radio v-model="approved" :label="true">Approve </el-radio>
            </el-col>
            <el-col class="radio-block">
              <el-radio v-model="approved" :label="false">Disapprove </el-radio>
            </el-col>
          </el-row>
        </div>
      </el-card>

      <div class="mt-5 upload-form-item text-center" v-else>
        <el-upload
          drag
          action=""
          :multiple="false"
          :show-file-list="false"
          accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          :on-success="handleImportExcel"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">
            Drop file here or <em>click to upload excel</em>
          </div>
        </el-upload>
      </div>
    </div>
  </div>
</template>

<script>
import XLSX from "xlsx";
import ProbationService from "@/services/probation_management/probation.service";
import UserService from "../../../services/user/user";
import _ from "lodash";

export default {
  props: ["id"],
  data() {
    return {
      templateId: "",
      isCheckTemplate: false,
      newOveralls: [],
      newInfos: [],
      listInfo: [],
      listOverall: [],
      listCompetence: [],
      listOutcome: [],
      listExcelCompetenceRole: [],
      employeesData: [],
      listTemplate: [],
      assessorOverallColIndex: 0,
      roleOverallColIndex: 0,
      roleOverallColLength: 0,
      listCompetenceRole: [],
      listOverallRole: [],
      evaluationTemplate: "",
      headerIndex: 0,
      infoIndex: 0,
      regionCode: {},
      excelData: [],
      sendCols: [],
      employeeBeSend: [],
    };
  },
  computed: {
    isSignedConstract() {
      return this.listOutcome.length && !!this.listOutcome[0].value[0];
    },
    isCheckedTerm() {
      return this.listOutcome.length && !!this.listOutcome[1].value[0];
    },
    term() {
      return this.listOutcome.length && this.listOutcome[1].value[0];
    },
    otherUpdateAction() {
      return this.listOutcome.length && this.listOutcome[2].value[0];
    },
    approved() {
      return this.listOutcome.length && !!this.listOutcome[3].value[0];
    },
  },
  created() {
    this.getAllEmployee();
    this.getAllActiveTemplate();
    const query = this.$route.query;
    if (query) {
      this.probationForm = query;
    }
  },
  methods: {
    async getAllActiveTemplate() {
      const res = await ProbationService.getAllActiveTemplate();
      this.listTemplate = res.data;
    },
    async changeTemplate(templateId) {
      this.templateId = templateId;
      if (templateId) {
        await this.getListCompetenceRole(templateId);
        await this.getListOverallRole(templateId);
      }
    },
    async getListCompetenceRole(templateId) {
      const res = await ProbationService.getEvaluationCompetencesAssessorRole(
        templateId
      );
      this.listCompetenceRole = res.data;
    },
    async getListOverallRole(templateId) {
      const res = await ProbationService.getEvaluationOverallsAssessorRole(
        templateId
      );
      this.listOverallRole = res.data;
    },
    handleImportExcel(esponse, file) {
      if (!this.evaluationTemplate) {
        return this.$toast.error("Please choose template for Probation");
      } else {
        const reader = new FileReader();
        reader.onload = (e) => {
          /* Parse data */
          const bstr = e.target.result;

          const wb = XLSX.read(bstr, { type: "binary" });

          const wsname = wb.SheetNames[0];
          const ws = wb.Sheets[wsname];
          const excelData = XLSX.utils.sheet_to_json(ws, {
            raw: true,
            header: 1,
          });
          if (excelData.length === 0) {
            this.$message.error("Oops, file invalid.");
            return;
          }
          this.confirmTemplate(excelData);
        };

        reader.readAsBinaryString(file.raw);
      }
    },
    confirmTemplate(excelData) {
      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm",
        message: h(
          "ConfirmTemplateProbation",
          {
            props: {
              headers: excelData,
              competenceRoles: this.listCompetenceRole,
              overallRoles: this.listOverallRole,
            },
            on: {
              inputCompetence: this.changeCompetenceIndex,
              inputOverall: this.changeOverallIndex,
              roleOverallColLength: this.changeRoleOverallColLength,
              roleOverallColIndex: this.changeRoleOverallColIndex,
              assessorOverallColIndex: this.changeAssessorOverallColIndex,
              excelCompetenceRoles: this.changeExcelCompetenceRoles,
              removeEmptyExcelData: this.changeRemoveEmptyExcelData,
              checkTemplate: this.checkTemplate,
            },
          },
          []
        ),
        roundButton: true,
        showCancelButton: true,
      }).then((res) => {
        if (this.isCheckTemplate) this.confirmHeader(excelData);
        else
          return this.$toast.error(
            "The selected template doesn't match with the imported excel"
          );
      });
    },
    confirmHeader(excelData) {
      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm",
        message: h(
          "ConfirmHeaderProbation",
          {
            props: {
              headers: excelData,
            },
            on: {
              inputInfo: this.changeInfoIndex,
              inputCompetence: this.changeCompetenceIndex,
              inputOverall: this.changeOverallIndex,
              inputOutcome: this.changeOutcomeIndex,
            },
          },
          []
        ),
        roundButton: true,
      }).then(() => {
        this.confirmAssessor(excelData);
      });
    },
    confirmAssessor(excelData) {
      const overallAssessors = excelData
        .slice(
          this.overallIndex + 1,
          this.overallIndex + 1 + this.roleOverallColLength
        )
        .map((overall) => ({
          overall: overall[0],
          old_assessor: this.getAssessorId(
            overall,
            this.employeesData,
            this.assessorOverallColIndex
          ),
          assessor_name: overall[this.assessorOverallColIndex],
          assessor: this.getAssessorId(
            overall,
            this.employeesData,
            this.assessorOverallColIndex
          ),

          role: overall[this.roleOverallColIndex],
        }));
      const infos = this.removeEmptyExcelData
        .slice(this.infoIndex, this.infoIndex + 6)
        .map((row) => ({
          title: row[0],
          value: row[1],
          check_employee_id: this.getEmployeeId(this.employeesData, row[1]),
          employee_id: this.getEmployeeId(this.employeesData, row[1]),
        }));

      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm",
        message: h(
          "ConfirmAssessor",
          {
            props: {
              overalls: overallAssessors,
              infos: infos,
              employeesData: this.employeesData,
            },
            on: {
              newOveralls: this.changeOveralls,
              newInfos: this.changeNewInfos,
            },
          },
          []
        ),
        customClass: "ConfirmAssessor",
        roundButton: true,
      }).then(async () => {
        this.showImportExcel(excelData);
      });
    },
    showImportExcel(excelData) {
      this.listInfo = this.removeEmptyExcelData
        .slice(this.infoIndex, this.infoIndex + 6)
        .map((row) => ({
          title: row[0],
          value: row[1],
        }));

      this.listOverall = excelData
        .slice(
          this.overallIndex + 1,
          this.overallIndex + 1 + this.roleOverallColLength
        )
        .map((row, index) => ({
          name: row[0],
          score: row.slice(1, 6).findIndex((item) => item) + 1,
          comment: String(row[this.assessorOverallColIndex - 1]),
          assessor: this.newOveralls[index].assessor
            ? this.newOveralls[index].assessor_name
            : "",
          role: row[this.roleOverallColIndex],
        }));

      let competence = excelData.slice(
        this.competenceIndex + 1,
        this.overallIndex
      );
      let newCompetence = _.reject(competence, _.isEmpty);

      let listCombineCompetence = [];
      for (let i = 0; i < newCompetence.length; i++) {
        const evaluateArr = _.chunk(newCompetence[i].slice(1), 6);
        const competenceName = newCompetence[i][0];
        const combineCompetence = this.listExcelCompetenceRole.reduce(
          (obj, item, index) => ({
            ...obj,
            [item]: {
              score:
                evaluateArr[index]?.slice(0, 5).findIndex((item) => item) + 1,
              comment: evaluateArr[index] ? evaluateArr[index][5] : "",
            },
            name: competenceName,
          }),
          {}
        );
        listCombineCompetence.push(combineCompetence);
      }
      this.listCompetence = listCombineCompetence;

      this.listOutcome = excelData
        .slice(this.outcomeIndex + 1, this.outcomeIndex + 1 + 4)
        .map((row) => ({
          title: row[0],
          value: row.slice(1, row.length),
        }));
    },
    changeRemoveEmptyExcelData(value) {
      this.removeEmptyExcelData = value;
    },
    getAssessorId(overall, employeesData, index) {
      return employeesData.find((item) => item?.profile.name === overall[index])
        ?.id;
    },
    getEmployeeId(employeesData, name) {
      return employeesData.find((item) => item?.profile.name === name)?.id;
    },
    changeRoleOverallColLength(value) {
      this.roleOverallColLength = value;
    },
    changeAssessorOverallColIndex(value) {
      this.assessorOverallColIndex = value;
    },
    changeRoleOverallColIndex(value) {
      this.roleOverallColIndex = value;
    },
    changeCompetenceIndex(index) {
      this.competenceIndex = index;
    },
    changeInfoIndex(index) {
      this.infoIndex = index;
    },
    changeOverallIndex(index) {
      this.overallIndex = index;
    },
    changeOutcomeIndex(index) {
      this.outcomeIndex = index;
    },
    changeOveralls(array) {
      this.newOveralls = array;
    },
    changeNewInfos(array) {
      this.newInfos = array;
    },
    changeExcelCompetenceRoles(value) {
      this.listExcelCompetenceRole = value;
    },
    checkTemplate(value) {
      this.isCheckTemplate = value;
    },
    async getAllEmployee() {
      let res = await UserService.getAllEmployees();
      this.employeesData = res.data;
    },
  },
};
</script>

<style lang="scss">
@import "importExcelProbation";
</style>
