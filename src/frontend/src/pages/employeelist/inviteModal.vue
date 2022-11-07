<template>
  <div>
    <validation-observer ref="observer">
      <el-form :model="invite" ref="invite" :inline="true">
        <div class="pt-3 row">
          <div class="col-12 col-sm-5 d-flex justify-content-start">
            <el-form-item prop="name" :rules="rules.name">
              <el-input
                v-model="invite.name"
                :counter="50"
                placeholder="Enter name"
                ref="name"
                clearable
              ></el-input>
            </el-form-item>
          </div>

          <div class="col-12 col-sm-5 d-flex justify-content-start">
            <el-form-item prop="email" :rules="rules.email">
              <el-input
                @keyup.enter="add"
                v-model="invite.email"
                placeholder="E-mail"
                type="email"
                clearable
              ></el-input>
            </el-form-item>
          </div>
          <div
            class="col-12 col-sm-2 d-flex justify-content-end align-items-baseline"
          >
            <el-button type="primary" @click="add('invite')">Add</el-button>
          </div>
        </div>
      </el-form>

      <div class="row">
        <div class="col-12 mt-3">
          <el-table
            :data="tableData"
            style="width: 100%"
            stripe
            header-cell-class-name="bg-header-table"
            :row-class-name="tableRowClassName"
          >
            <el-table-column
              prop="name"
              label="Name"
              align="center"
            ></el-table-column>
            <el-table-column
              prop="email"
              label="Email"
              align="center"
            ></el-table-column>
            <el-table-column
              prop="status"
              label="Status"
              align="center"
              v-if="showResult"
            ></el-table-column>
            <el-table-column label="Action" v-if="!showResult" align="center">
              <template v-slot="scope">
                <el-button type="danger" @click="remove(scope.$index)">
                  <font-awesome-icon
                    class="text-white fa-fw"
                    :icon="['fas', 'times']"
                  />
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <div>
        <div>
          <div v-show="showResult" class="float-left">
            <div class="pt-2">
              <div class="text-success ml-3">
                Success: {{ validUser.length }}
              </div>
              <div class="text-danger ml-3" @click="sendList">
                Failure: {{ invalidUser.length }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </validation-observer>
    <div class="footer-dialog d-flex justify-content-end mt-2">
      <el-button type="info" @click="clearTable">Clear</el-button>
      <el-button type="primary" @click="sendList">Send invitations</el-button>
    </div>
  </div>
</template>
<script>
import InviteService from "@/services/employee/inviteModal.sercice";
import { ValidationObserver, setInteractionMode } from "vee-validate";

const STATUS_SUCCESS = "Success";
const STATUS_EXISTED = "Already existed";
const { validateEmail } = require("../../utils/validation");

setInteractionMode("eager");

export default {
  name: "inviteModal",
  middleware: "authentication",
  components: {
    ValidationObserver,
  },
  data() {
    return {
      showResult: false,
      listInvite: [],
      invalidUser: [],
      validUser: [],
      invite: {
        name: "",
        email: "",
      },
      defaultInvite: {
        name: "",
        email: "",
      },
      rules: {
        name: [
          {
            validator: (_rule, value, callback, _source, _options) => {
              if (value.trim().length === 0) {
                callback(new Error("Name is required"));
              } else if (value.trim().length > 50 || value.trim().length < 3) {
                callback(new Error("Name must be between 3 and 50 characters"));
              }
              callback();
            },
            trigger: ["blur"],
          },
        ],
        email: [
          {
            validator: (_rule, value, callback, _source, _options) => {
              if (!validateEmail(value)) {
                callback(new Error("Please input correct email address"));
              } else if (process.env.VUE_APP_BLOCKED_EMAIL_DOMAINS.length) {
                const blockedEmailDomains =
                  process.env.VUE_APP_BLOCKED_EMAIL_DOMAINS.split(",");
                blockedEmailDomains.forEach((domain) => {
                  if (value.endsWith(domain)) {
                    callback(new Error(`Email ${value} is blocked`));
                  }
                });
              }
              callback();
            },
            trigger: ["blur", "change"],
          },
        ],
      },
    };
  },
  methods: {
    async sendList() {
      if (!this.listInvite.length) {
        return;
      }
      this.resetForm();
      let response = await InviteService.sendList(this.listInvite);
      if (response.status === 201 && response.data) {
        this.listInvite = [];
        this.invalidUser = response.data.invalid_user;
        this.validUser = response.data.valid_user;
        if (this.invalidUser.length) {
          this.$toast.warning(`Failure: ${this.invalidUser.length}`);
        } else {
          this.$toast.success("Sent Successfully");
        }
        this.showResult = true;
      } else {
        this.$toast.error("Sent Failed");
      }
    },
    add(formName) {
      this.$refs[formName].validate((valid, _obj) => {
        if (valid) {
          this.listInvite.unshift(this.invite);
          this.resetForm();
          this.$refs.name.focus();
        }
      });
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.status === STATUS_EXISTED) {
        return `text-danger ${rowIndex}`;
      } else if (row.status === STATUS_SUCCESS) {
        return `text-success ${rowIndex}`;
      }
      return "";
    },
    clearTable() {
      this.validUser = [];
      this.listInvite = [];
      this.invalidUser = [];
      this.showResult = false;
      this.resetForm();
    },
    resetForm() {
      this.invite = Object.assign({}, this.defaultInvite);
      this.$refs.observer.reset();
    },
    remove(index) {
      this.listInvite.splice(index, 1);
    },
  },
  computed: {
    tableData() {
      if (this.listInvite.length > 0) {
        return this.listInvite;
      } else {
        return this.invalidUser.concat(this.validUser);
      }
    },
  },
};
</script>
