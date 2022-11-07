<template>
  <div class="container-fluid">
    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">Education</span>
          <el-button
            class="edit-button"
            type="text"
            @click="editData"
            v-if="
              !isEditing &&
              checkOwnerOrHasScope('user:edit_private_user_information_list')
            "
          >
            <img
              :src="require('@/static/images/IconCardEdit.svg')"
              class="edit-icon"
              alt="edit"
            />
          </el-button>
          <el-button
            class="edit-button"
            type="text"
            @click="showConfirmDialog"
            v-if="isEditing"
          >
            <img
              :src="require('@/static/images/IconCardSave.svg')"
              class="edit-icon"
              alt="save"
            />
          </el-button>
        </div>
        <div>
          <div class="d-flex" :class="{ active: hiddenFormAdd }">
            <div class="col-2 p-0 mt-2 mb-2 ml-3 mr-3">
              <el-input
                v-model="formData.school"
                placeholder="Your university name"
              />
              <div class="error" v-if="!$v.formData.school.required">
                Field is required
              </div>
            </div>
            <div class="col-2 p-0 m-2">
              <el-input v-model="formData.degree" placeholder="Degree" />
              <div class="error" v-if="!$v.formData.degree.required">
                Field is required
              </div>
            </div>
            <div class="col-2 p-0 m-2">
              <el-input v-model="formData.field_of_study" placeholder="Major" />
              <div class="error" v-if="!$v.formData.field_of_study.required">
                Field is required
              </div>
            </div>
            <div class="col-2 p-0 m-2">
              <el-input
                v-model="formData.graduated_year"
                type="number"
                min="2000"
                max="3000"
                placeholder="Your graduated year"
              />
            </div>
            <div class="col-2 p-0 ml-3 mt-2 mb-2">
              <el-input
                v-model="formData.additional_notes"
                placeholder="Notes"
              />
            </div>
            <div class="text-center p-0 ml-3 m-2" style="width: 100%">
              <el-button
                type="primary"
                @click="createEducation()"
                style="font-family: 'Times New Roman'; font-weight: bold"
              >
                Add New
              </el-button>
            </div>
          </div>

          <el-table
            highlight-current-row
            :data="userEducations"
            stripe
            header-cell-class-name="bg-header-table"
            border
            style="width: 100%"
            class="mt-2"
          >
            <el-table-column prop="school" label="School Name">
              <template slot-scope="scope">
                <el-input
                  v-model="scope.row.school"
                  :disabled="!scope.row.editMode"
                />
              </template>
            </el-table-column>
            <el-table-column prop="degree" label="Degree">
              <template slot-scope="scope">
                <el-input
                  v-model="scope.row.degree"
                  :disabled="!scope.row.editMode"
                />
              </template>
            </el-table-column>
            <el-table-column prop="field_of_study" label="Major">
              <template slot-scope="scope">
                <el-input
                  v-model="scope.row.field_of_study"
                  :disabled="!scope.row.editMode"
                />
              </template>
            </el-table-column>
            <el-table-column prop="graduated_year" label="Year of graduation">
              <template slot-scope="scope">
                <el-input
                  v-model="scope.row.graduated_year"
                  type="number"
                  :min="2000"
                  :max="3000"
                  :disabled="!scope.row.editMode"
                />
              </template>
            </el-table-column>
            <el-table-column prop="additional_notes" label="Notes">
              <template slot-scope="scope">
                <el-input
                  v-model="scope.row.additional_notes"
                  :disabled="!scope.row.editMode"
                />
              </template>
            </el-table-column>
            <el-table-column label="Action" width="150">
              <template slot-scope="scope" v-if="isEditing">
                <div
                  class="text-center"
                  v-if="
                    !scope.row.editMode &&
                    checkOwnerOrHasScope(
                      'user:edit_private_user_information_list'
                    )
                  "
                >
                  <img
                    :src="require('@/static/images/IconEdit.svg')"
                    @click="toggleEditing(scope.row)"
                    alt="edit"
                  />
                  <img
                    :src="require('@/static/images/IconDelete.svg')"
                    @click="toggleConfirmDelete(scope.row)"
                    alt="delete"
                  />
                </div>
                <div class="text-center" v-else>
                  <img
                    :src="require('@/static/images/IconCheck.svg')"
                    class="mr-3"
                    alt="check"
                    @click="updateEducation(scope.row)"
                  />
                  <img
                    :src="require('@/static/images/IconCancel.svg')"
                    class="ml-3"
                    alt="cancel"
                    @click="cancelUpdateEducation(scope.row)"
                  />
                </div>
              </template>
            </el-table-column>
          </el-table>
          <el-dialog :visible.sync="dialogDelete" title="Confirm Delete">
            <slot>
              <h3 class="text-center">Do you want to remove?</h3>
              <div class="text-center">
                <el-button
                  type="danger"
                  class="mt-3"
                  @click="deleteEducation()"
                >
                  Delete
                </el-button>
              </div>
            </slot>
          </el-dialog>
        </div>
      </el-card>
      <el-dialog title="Confirm" :visible.sync="isConfirming" width="30%">
        <span>Do you want to save this change?</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="cancelConfirm">Cancel</el-button>
          <el-button type="primary" @click="saveConfirm">Save</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import EducationService from "@/services/profile/education.js";
import { required } from "vuelidate/lib/validators";
import { mapGetters } from "vuex";

const { checkOwner, checkHasScope } = require("../../../../utils/validation");

export default {
  data: () => ({
    isEditing: false,
    isConfirming: false,
    hiddenFormAdd: true,
    dialogDelete: false,
    educationToDelete: "",
    selected: "",
    formData: {
      education_id: "",
      school: "",
      degree: "",
      field_of_study: "",
      graduated_year: null,
      additional_notes: null,
    },
    userId: Number,
    userEducations: [],
  }),
  validations: {
    formData: {
      school: {
        required,
      },
      degree: {
        required,
      },
      field_of_study: {
        required,
      },
    },
  },
  methods: {
    checkOwnerOrHasScope(scope) {
      return (
        checkOwner(this.userId, this.tokenInfo) ||
        checkHasScope(scope, this.tokenInfo)
      );
    },
    showConfirmDialog() {
      this.isConfirming = true;
    },
    cancelConfirm() {
      this.isConfirming = false;
    },
    saveConfirm() {
      this.isEditing = false;
      this.isConfirming = false;
      this.hiddenFormAdd = true;
    },
    cancelUpdateEducation(userEducation) {
      this.$set(userEducation, "editMode", false);
      userEducation.school = userEducation.oldSchool;
      userEducation.degree = userEducation.oldDegree;
      userEducation.field_of_study = userEducation.oldFieldOfStudy;
      userEducation.graduated_year = userEducation.OldGraduatedYear;
      userEducation.additional_notes = userEducation.OldNote;
    },
    toggleEditing(userEducation) {
      this.$set(userEducation, "editMode", true);
      userEducation.oldSchool = userEducation.school;
      userEducation.oldDegree = userEducation.degree;
      userEducation.oldFieldOfStudy = userEducation.field_of_study;
      userEducation.OldGraduatedYear = userEducation.graduated_year;
      userEducation.OldNote = userEducation.additional_notes;
    },
    toggleConfirmDelete(userEducation) {
      this.educationToDelete = userEducation;
      this.dialogDelete = true;
    },
    editData() {
      this.hiddenFormAdd = false;
      this.isEditing = true;
    },
    async getData() {
      this.userEducations = (await EducationService.get(this.userId)).data;
    },
    async createEducation() {
      try {
        this.userEducations.push(
          (await EducationService.create(this.userId, this.formData)).data
        );
        this.formData = {};
        this.dialog = false;
        this.$toast.success("Created Success");
      } catch (error) {
        if (error.response && error.response.data) {
          this.$emit("openSnack", error.response.data, "error");
        }
      }
    },
    async updateEducation(userEducation) {
      try {
        let tempEducation = (
          await EducationService.update(this.userId, userEducation)
        ).data;
        for (let i in this.userEducations) {
          if (this.userEducations[i].id === tempEducation.id) {
            this.userEducations[i] = { ...tempEducation };
            break;
          }
        }
        this.$set(userEducation, "editMode", false);
        this.dialog = false;
        this.$toast.success("Updated Success");
      } catch (error) {
        if (error.response && error.response.data) {
          this.$emit("openSnack", error.response.data, "error");
        }
      }
    },
    async deleteEducation() {
      try {
        const data = {
          education_id: this.educationToDelete.id,
        };
        const res = await EducationService.delete(this.userId, data);
        if (res.status >= 200 && res.status < 400) {
          this.userEducations.splice(
            this.userEducations.indexOf(this.educationToDelete),
            1
          );
          this.educationToDelete = {};
          this.dialogDelete = false;
          this.$toast.success("Deleted Success");
        }
      } catch (error) {
        this.$toast.error("Deleted Error");
        this.$emit("openSnack", error.response.data, "error");
      }
    },
  },
  mounted() {
    this.userId = this.$route.params.id;
    this.getData();
  },
  computed: {
    ...mapGetters({ tokenInfo: "scope/tokenInfo" }),
  },
};
</script>

<style scoped>
.active {
  display: none !important;
}
</style>
