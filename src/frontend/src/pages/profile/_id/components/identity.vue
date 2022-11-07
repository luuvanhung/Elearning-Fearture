<template>
  <div class="container-fluid">
    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">Identity Information</span>
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
            <div class="col-5 col-xl-2 my-2">Identity number:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{
                  !dataInfo.identity_number ? NO_DATA : dataInfo.identity_number
                }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                v-model="dataInfo.identity_number"
              >
              </el-input>
              <div class="error" v-if="!$v.dataInfo.identity_number.required">
                Field is required
              </div>
              <div class="error" v-if="!$v.dataInfo.identity_number.integer">
                Must contain only numbers
              </div>
              <div class="error" v-if="!$v.dataInfo.identity_number.minLength">
                Required at least
                {{ $v.dataInfo.identity_number.$params.minLength.min }} digits.
              </div>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Issue date:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{ !dataInfo.issue_date ? NO_DATA : dataInfo.issue_date }}
              </div>
              <el-date-picker
                v-else
                size="small"
                placeholder="Please input"
                v-model="dataInfo.issue_date"
                type="date"
                required
                value-format="yyyy-MM-dd"
              >
              </el-date-picker>
              <div class="error" v-if="!$v.dataInfo.issue_date.required">
                Field is required
              </div>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Issue place:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{ !dataInfo.issue_place ? NO_DATA : dataInfo.issue_place }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                required
                v-model="dataInfo.issue_place"
              >
              </el-input>
              <div class="error" v-if="!$v.dataInfo.issue_place.required">
                Field is required
              </div>
            </div>
          </div>

          <div class="row mb-1">
            <div class="col-5 col-xl-2 my-2">Place of birth:</div>
            <div class="col-7 col-xl-10 text-dark my-2">
              <div v-if="!isEditing">
                {{
                  !dataInfo.place_of_birth ? NO_DATA : dataInfo.place_of_birth
                }}
              </div>
              <el-input
                v-else
                placeholder="Please input"
                size="small"
                clearable
                v-model="dataInfo.place_of_birth"
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
import IdentityService from "@/services/profile/identity.js";
import { required, minLength, integer } from "vuelidate/lib/validators";
import { mapGetters } from "vuex";

const NO_DATA = "Empty";
const { checkOwner, checkHasScope } = require("../../../../utils/validation");

export default {
  name: "IdentityInformation",

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
  validations: {
    dataInfo: {
      identity_number: {
        required,
        integer,
        minLength: minLength(9),
      },
      issue_place: {
        required,
      },
      issue_date: {
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
    async fetchData() {
      const response = await IdentityService.get(this.userId);
      if (response && response.status == 200) {
        this.fetchFieldsFromData(response.data);
      }
    },

    fetchFieldsFromData(data) {
      this.dataInfo = {
        identity_number: data.identity_number,
        issue_date: data.issue_date,
        issue_place: data.issue_place,
        place_of_birth: data.place_of_birth,
      };
    },

    addData() {
      this.dataInfo = {
        identity_number: null,
        issue_date: null,
        issue_place: null,
        place_of_birth: null,
      };
      this.isCreating = true;
      this.isEditing = true;
    },

    async saveData() {
      if (this.isCreating) {
        let response = await IdentityService.create(this.userId, this.dataInfo);
        if (response.status >= 400) {
          this.$toast.error("Create failed");
          return;
        } else {
          this.$toast.success("Create successfully");
          this.isCreating = false;
          this.isEditing = false;
          this.isConfirming = false;
        }
      } else {
        let response = await IdentityService.update(this.userId, this.dataInfo);
        if (response && response.status == 200) {
          this.$toast.success("Update successfully");
          this.isEditing = false;
          this.isConfirming = false;
        } else {
          this.$toast.error("Update failed");
          this.isConfirming = false;
        }
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
