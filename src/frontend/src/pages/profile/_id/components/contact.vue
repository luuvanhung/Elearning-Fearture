<template>
  <div class="container-fluid">
    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">Contact Information</span>
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
            <div class="col-5 col-xl-2 my-2">Permanent Address:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{
                  !dataInfo.permanent_address
                    ? NO_DATA
                    : dataInfo.permanent_address
                }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                v-model="dataInfo.permanent_address"
              >
              </el-input>
              <div class="error" v-if="!$v.dataInfo.permanent_address.required">
                Field is required
              </div>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Temporary Address:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{
                  !dataInfo.temporary_address
                    ? NO_DATA
                    : dataInfo.temporary_address
                }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                required
                v-model="dataInfo.temporary_address"
              >
              </el-input>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">
              Household Registration Number:
            </div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{
                  !dataInfo.household_registration_number
                    ? NO_DATA
                    : dataInfo.household_registration_number
                }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                required
                v-model="dataInfo.household_registration_number"
              >
              </el-input>
              <div
                class="error"
                v-if="!$v.dataInfo.household_registration_number.minLength"
              >
                Required at least
                {{
                  $v.dataInfo.household_registration_number.$params.minLength
                    .min
                }}
                characters.
              </div>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Contact Emergency:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{
                  !dataInfo.contact_emergency
                    ? NO_DATA
                    : dataInfo.contact_emergency
                }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                clearable
                v-model="dataInfo.contact_emergency"
              >
              </el-input>
              <div class="error" v-if="!$v.dataInfo.contact_emergency.required">
                Field is required.
              </div>
              <div class="error" v-if="!$v.dataInfo.contact_emergency.integer">
                Contact must be number
              </div>
              <div
                class="error"
                v-if="!$v.dataInfo.contact_emergency.minLength"
              >
                Required at least
                {{ $v.dataInfo.contact_emergency.$params.minLength.min }}
                digits.
              </div>
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
import ContactService from "@/services/profile/contact.js";
import { required, minLength, integer } from "vuelidate/lib/validators";
import { mapGetters } from "vuex";

const NO_DATA = "Empty";
const { checkOwner, checkHasScope } = require("../../../../utils/validation");

export default {
  name: "ContactInformation",
  validations: {
    dataInfo: {
      permanent_address: {
        required,
      },
      household_registration_number: {
        minLength: minLength(5),
      },
      contact_emergency: {
        required,
        integer,
        minLength: minLength(9),
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
      const response = await ContactService.get(this.userId);
      if (response && response.status === 200) {
        this.fetchFieldsFromData(response.data);
      }
    },

    fetchFieldsFromData(data) {
      this.dataInfo = {
        permanent_address: data.permanent_address,
        temporary_address: data.temporary_address,
        household_registration_number: data.household_registration_number,
        contact_emergency: data.contact_emergency,
      };
    },

    addData() {
      this.dataInfo = {
        permanent_address: null,
        issue_datemporary_addresste: null,
        household_registration_number: null,
        contact_emergency: null,
      };
      this.isCreating = true;
      this.isEditing = true;
    },

    async saveData() {
      if (this.isCreating) {
        let response = await ContactService.create(this.userId, this.dataInfo);
        if (response.status >= 400) {
          this.$toast.error("Create Failed");
          return;
        } else {
          this.$toast.success("Created Successfully");
          this.isCreating = false;
          this.isEditing = false;
          this.isConfirming = false;
        }
      } else {
        let response = await ContactService.update(this.userId, this.dataInfo);
        if (response && response.status === 200) {
          this.$toast.success("Updated Successfully");
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
    await this.fetchData();
  },
  computed: {
    ...mapGetters({ tokenInfo: "scope/tokenInfo" }),
  },
};
</script>

<style></style>
