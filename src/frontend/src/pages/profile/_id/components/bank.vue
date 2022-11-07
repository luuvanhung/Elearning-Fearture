<template>
  <div class="container-fluid">
    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">Bank Account</span>
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
            <div class="col-5 col-xl-2 my-2">Account Number:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{
                  !dataInfo.account_number ? NO_DATA : dataInfo.account_number
                }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                v-model="dataInfo.account_number"
              >
              </el-input>
              <div v-if="!$v.dataInfo.account_number.required" class="error">
                Field is required
              </div>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Bank Name:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{ !dataInfo.bank_name ? NO_DATA : dataInfo.bank_name }}
              </div>
              <el-select
                v-else
                v-model="dataInfo.bank"
                placeholder="Select your bank"
                size="mini"
                required
              >
                <el-option
                  v-for="bank in banks"
                  :key="bank.id"
                  :label="bank.name"
                  :value="bank.id"
                >
                </el-option>
              </el-select>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Bank Branch:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{ !dataInfo.branch ? NO_DATA : dataInfo.branch }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                required
                v-model="dataInfo.branch"
              >
              </el-input>
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
import BankService from "@/services/profile/bank.js";
import { required } from "vuelidate/lib/validators";
import { mapGetters } from "vuex";

const NO_DATA = "Empty";
const { checkOwner, checkHasScope } = require("../../../../utils/validation");

export default {
  name: "BankAccountInformation",
  validations: {
    dataInfo: {
      account_number: {
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
      banks: null,
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
      const banksResponse = await BankService.getBankList();
      if (banksResponse.status >= 400) {
        this.$toast.error("Cannot load list of banks!");
        return;
      }
      this.banks = banksResponse.data;

      const response = await BankService.get(this.userId);
      if (response && response.status == 200) {
        this.fetchFieldsFromData(response.data);
      }
    },

    fetchFieldsFromData(data) {
      this.dataInfo = {
        account_number: data.account_number,
        bank: data.bank,
        bank_name: data.bank_name,
        branch: data.branch,
      };
    },

    addData() {
      this.dataInfo = {
        account_number: null,
        bank: null,
        bank_name: null,
        branch: null,
      };
      this.isCreating = true;
      this.isEditing = true;
    },

    async saveData() {
      if (this.isCreating) {
        let response = await BankService.create(this.userId, this.dataInfo);
        if (response.status >= 400) {
          this.$toast.error("Create Failed");
          return;
        } else {
          this.$toast.success("Created Successfully");
          if (this.dataInfo.bank) {
            this.dataInfo.bank_name = this.banks.find(
              (bank) => bank.id === this.dataInfo.bank
            ).name;
          }
          this.isCreating = false;
          this.isEditing = false;
          this.isConfirming = false;
        }
      } else {
        let response = await BankService.update(this.userId, this.dataInfo);
        if (response && response.status == 200) {
          this.$toast.success("Updated Successfully");
          if (this.dataInfo.bank) {
            this.dataInfo.bank_name = this.banks.find(
              (bank) => bank.id === this.dataInfo.bank
            ).name;
          }
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
