<template>
  <div class="container-fluid">
    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">Social Insurance</span>
          <el-button
            class="edit-button"
            type="text"
            @click="showConfirmDialog"
            v-if="isEditing || isCreating"
          >
            <img
              :src="require('@/static/images/IconCardSave.svg')"
              class="edit-icon"
              alt="save"
            />
          </el-button>
          <el-button
            class="edit-button"
            type="text"
            @click="isEditing = true"
            v-else-if="
              dataInfo !== null &&
              checkOwnerOrHasScope('user:edit_private_user_information_list')
            "
          >
            <img
              :src="require('@/static/images/IconCardEdit.svg')"
              class="edit-icon"
              alt="edit"
            />
          </el-button>
        </div>
        <div v-if="dataInfo" class="text item mx-2">
          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Social Insurance Code:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{
                  !dataInfo.social_insurance_code
                    ? NO_DATA
                    : dataInfo.social_insurance_code
                }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                v-model="dataInfo.social_insurance_code"
              >
              </el-input>
              <div
                class="error"
                v-if="!$v.dataInfo.social_insurance_code.required"
              >
                Field is required
              </div>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Start Date:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{ !dataInfo.start_date ? NO_DATA : dataInfo.start_date }}
              </div>
              <el-date-picker
                v-else
                size="small"
                placeholder="Please input"
                v-model="dataInfo.start_date"
                type="date"
                required
                value-format="yyyy-MM-dd"
              >
              </el-date-picker>
            </div>
          </div>
        </div>

        <div v-else>
          <div
            class="d-flex flex-row"
            @click="addData()"
            v-if="
              checkOwnerOrHasScope('user:edit_private_user_information_list')
            "
          >
            <img
              class="img-add"
              style="height: 30px"
              :src="require('@/static/images/IconAdd.svg')"
              alt="add"
            />
            <h3 class="mt-1 ml-3 text-info">Click to add information</h3>
          </div>
        </div>
      </el-card>

      <el-dialog title="Confirm" :visible.sync="isConfirming" width="30%">
        <span>Do you want to save this change?</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="cancelConfirm">Cancel</el-button>
          <el-button
            type="primary"
            @click="saveData"
            :disabled="$v.dataInfo.$invalid"
            >Save</el-button
          >
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import InsuranceService from "@/services/profile/insurance.js";
import { required } from "vuelidate/lib/validators";
import { mapGetters } from "vuex";

const NO_DATA = "Empty";
const { checkOwner, checkHasScope } = require("../../../../utils/validation");

export default {
  name: "InsuranceInformation",
  validations: {
    dataInfo: {
      social_insurance_code: {
        required,
      },
    },
  },
  data() {
    return {
      isEditing: false,
      isConfirming: false,
      isCreating: false,
      dataInfo: null,
      userId: Number,
      NO_DATA,
    };
  },
  methods: {
    checkOwnerOrHasScope(scope) {
      return (
        checkOwner(this.userId, this.tokenInfo) ||
        checkHasScope(scope, this.tokenInfo)
      );
    },
    async fetchData() {
      const response = await InsuranceService.get(this.userId);
      if (response && response.status == 200) {
        this.fetchFieldsFromData(response.data);
      }
    },

    fetchFieldsFromData(data) {
      this.dataInfo = {
        social_insurance_code: data.social_insurance_code,
        start_date: data.start_date,
      };
    },

    addData() {
      this.dataInfo = {
        social_insurance_code: null,
        start_date: null,
      };
      this.isCreating = true;
      this.isEditing = true;
    },

    async saveData() {
      if (this.isCreating) {
        let response = await InsuranceService.create(
          this.userId,
          this.dataInfo
        );
        if (response.status >= 400) {
          this.$toast.error("Create Failed");
          return;
        } else {
          this.$toast.success("Created successfully");
          this.isCreating = false;
          this.isEditing = false;
          this.isConfirming = false;
        }
      } else {
        let response = await InsuranceService.update(
          this.userId,
          this.dataInfo
        );
        if (response && response.status == 200) {
          this.$toast.success("Updated successfully");
        } else {
          this.$toast.error("Update Failed");
        }
        this.isEditing = false;
        this.isConfirming = false;
      }
    },

    showConfirmDialog() {
      this.isConfirming = true;
    },

    cancelConfirm() {
      this.isConfirming = false;
    },

    showEditForm() {
      this.isEditing = true;
    },

    saveForm() {
      this.isEditing = false;
      this.isConfirming = true;
    },
  },
  async created() {
    this.userId = this.$route.params.id;
    this.fetchData();
  },
  computed: {
    ...mapGetters({ tokenInfo: "scope/tokenInfo" }),
  },
};
</script>

<style></style>
