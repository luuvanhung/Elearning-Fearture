<template>
  <div class="container-fluid">
    <div class="header-container my-3">
      <div class="avatar-block" @click="onPickFile">
        <img :src="avatar" alt />
        <div class="avatar-mask">Change</div>
        <input
          ref="avatarInput"
          type="file"
          accept="image/*"
          style="display: none"
          @change="onFilePicked"
        />
      </div>

      <div class="content">
        <div class="name-block">
          <p>{{ profileInfo.name }}</p>
        </div>
        <div class="change-avatar-block">
          <p>
            {{
              !profileInfo.title.length
                ? " "
                : profileInfo.title.map((e) => e.title).join(", ")
            }}
          </p>
        </div>
      </div>
    </div>

    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">General Profile</span>
          <el-button
            class="edit-button"
            type="text"
            @click="isEditing = true"
            v-if="
              !isEditing &&
              checkOwnerOrHasScope('user:edit_public_user_information_list')
            "
            :disabled="
              !checkOwnerOrHasScope('user:edit_public_user_information_list')
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
            @click="submitForm('ruleForm')"
            v-else-if="
              checkOwnerOrHasScope('user:edit_public_user_information_list')
            "
          >
            <img
              :src="require('@/static/images/IconCardSave.svg')"
              class="edit-icon"
              alt="save"
            />
          </el-button>
        </div>
        <el-form :model="profileInfo" ref="ruleForm" :rules="rules" status-icon>
          <div class="text item mx-2">
            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Name:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !profileInfo.name ? NO_DATA : profileInfo.name }}
                </div>
                <el-form-item v-else prop="name">
                  <el-input
                    placeholder="Please input"
                    size="small"
                    v-model="profileInfo.name"
                  ></el-input>
                </el-form-item>
              </div>
            </div>

            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Email:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !profileInfo.email ? NO_DATA : profileInfo.email }}
                </div>
                <el-form-item v-else prop="email">
                  <el-input
                    placeholder="Please input"
                    size="small"
                    type="email"
                    v-model="profileInfo.email"
                  ></el-input>
                </el-form-item>
              </div>
            </div>

            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Gender:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !profileInfo.gender ? NO_DATA : profileInfo.gender.text }}
                </div>
                <el-form-item v-else prop="gender">
                  <el-select
                    v-model="profileInfo.gender"
                    placeholder="Select Gender"
                    size="mini"
                    required
                  >
                    <el-option
                      v-for="gender in GENDERS"
                      :key="gender.value"
                      :label="gender.text"
                      :value="gender"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </div>
            </div>

            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Join date:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !profileInfo.join_date ? NO_DATA : profileInfo.join_date }}
                </div>
                <el-form-item v-else prop="join_date">
                  <el-date-picker
                    placeholder="Please input"
                    size="small"
                    type="date"
                    value-format="yyyy-MM-dd"
                    v-model="profileInfo.join_date"
                    :disabled="!isAdmin"
                  ></el-date-picker>
                </el-form-item>
              </div>
            </div>

            <div
              class="row mb-1"
              v-show="
                checkOwnerOrHasScope(
                  'user:edit_private_user_information_list'
                ) ||
                checkOwnerOrHasScope('user:view_private_user_information_list')
              "
            >
              <div class="col-5 col-xl-2 my-2">Personal email:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{
                    !profileInfo.personal_email
                      ? NO_DATA
                      : profileInfo.personal_email
                  }}
                </div>
                <el-form-item v-else prop="personal_email">
                  <el-input
                    placeholder="Please input"
                    size="small"
                    v-model="profileInfo.personal_email"
                  ></el-input>
                </el-form-item>
              </div>
            </div>

            <div
              class="row mb-1"
              v-show="
                checkOwnerOrHasScope(
                  'user:edit_private_user_information_list'
                ) ||
                checkOwnerOrHasScope('user:view_private_user_information_list')
              "
            >
              <div class="col-5 col-xl-2 my-2">Phone:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !profileInfo.phone ? NO_DATA : profileInfo.phone }}
                </div>
                <el-form-item v-else prop="phone">
                  <el-input
                    placeholder="Please input"
                    size="small"
                    v-model="profileInfo.phone"
                  ></el-input>
                </el-form-item>
              </div>
            </div>

            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Slack ID:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !profileInfo.slack_id ? NO_DATA : profileInfo.slack_id }}
                </div>
                <el-form-item v-else prop="slack_id">
                  <el-input
                    placeholder="Please input"
                    size="small"
                    v-model="profileInfo.slack_id"
                  ></el-input>
                </el-form-item>
              </div>
            </div>

            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Title:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{
                    !profileInfo.title.length
                      ? NO_DATA
                      : profileInfo.title.map((e) => e.title).join(", ")
                  }}
                </div>
                <el-form-item v-else prop="selectTitle">
                  <el-select
                    v-model="selectTitle"
                    multiple
                    placeholder="Select title"
                    size="small"
                    required
                  >
                    <el-option
                      v-for="title in titles"
                      :key="title.id"
                      :label="title.title"
                      :value="title.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </div>
            </div>

            <div
              class="row mb-1"
              v-show="
                checkOwnerOrHasScope(
                  'user:edit_private_user_information_list'
                ) ||
                checkOwnerOrHasScope('user:view_private_user_information_list')
              "
            >
              <div class="col-5 col-xl-2 my-2">Birthday:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !profileInfo.birth_day ? NO_DATA : profileInfo.birth_day }}
                </div>
                <el-form-item v-else prop="birth_day">
                  <el-date-picker
                    placeholder="Please input"
                    size="small"
                    type="date"
                    value-format="yyyy-MM-dd"
                    v-model="profileInfo.birth_day"
                  ></el-date-picker>
                </el-form-item>
              </div>
            </div>

            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Line manager:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{
                    profileInfo.line_manager_user_name
                      ? profileInfo.line_manager_user_name
                      : profileInfo.maximum_level_approved != 0
                      ? NO_DATA
                      : "User has highest role"
                  }}
                </div>
                <el-form-item v-else prop="line_manager">
                  <el-select
                    v-model="profileInfo.line_manager"
                    filterable
                    remote
                    reserve-keyword
                    @change="changeUser($event)"
                    placeholder="Select line manager"
                    :disabled="!isAdmin"
                  >
                    <el-option
                      v-for="item in usersData"
                      :key="item.id"
                      :label="item.profile.name"
                      :value="item.profile.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </div>
            </div>

            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Maximum level approve:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{
                    isNaN(profileInfo.maximum_level_approved)
                      ? NO_DATA
                      : profileInfo.maximum_level_approved
                  }}
                </div>
                <el-input
                  v-else
                  placeholder="Please input"
                  size="small"
                  type="number"
                  v-model="profileInfo.maximum_level_approved"
                  :disabled="!isAdmin"
                ></el-input>
              </div>
            </div>
            <restricted-view :scope="['user:set_role']">
              <template v-slot:default>
                <div class="row mb-1">
                  <div class="col-5 col-xl-2 my-2">Set role:</div>
                  <div class="col-7 col-xl-10 text-dark my-2">
                    <div v-if="!isEditing">
                      <span v-for="role in user.roles" :key="role.id">
                        <span
                          v-if="
                            role === user.roles[user.roles.length - 1] &&
                            !editRoles
                          "
                          >{{ role.name + " " }}</span
                        >
                        <span v-else v-show="!editRoles">{{
                          role.name + ", "
                        }}</span>
                      </span>
                      <font-awesome-icon
                        @click="editRoles = true"
                        v-show="!editRoles"
                        :icon="['fas', 'edit']"
                        class="text-info ml-2"
                        style="cursor: pointer"
                      />
                      <div>
                        <el-select
                          v-model="selectedRoles"
                          multiple
                          collapse-tags
                          placeholder="Select role"
                          v-show="editRoles"
                        >
                          <el-option
                            v-for="item in options"
                            :key="item.id"
                            :label="item.name"
                            :value="item.id"
                          ></el-option>
                        </el-select>
                      </div>
                      <el-button
                        style="margin-bottom: 1%"
                        type="primary"
                        @click="handleClose()"
                        class="mt-2"
                        v-show="editRoles"
                        >Confirm</el-button
                      >
                    </div>
                  </div>
                </div>
              </template>
            </restricted-view>
          </div>
        </el-form>
      </el-card>

      <el-dialog title="Confirm" :visible.sync="isConfirming" width="30%">
        <span>Do you want to save this change?</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="cancelConfirm">Cancel</el-button>
          <el-button type="primary" @click="saveData">Save</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import logo from "@/static/images/icon.png";
import GetUserService from "@/services/user/getUser";
import UserService from "@/services/user/user";
import RoleService from "@/services/role/role_service";
import RestrictedView from "@/components/RestrictedView";
import { GENDERS } from "@/const/genders";
import { mapGetters } from "vuex";
import { validateEmail, validatePhone } from "@/utils/validation";
import { formatDate } from "@/utils/time";
import moment from "moment";

const ERROR_MESSAGE = "Error when fetching data";
const NO_DATA = "No data";
const { checkOwner, checkHasScope } = require("../../../../utils/validation");

export default {
  name: "GeneralInformation",
  components: {
    RestrictedView,
  },
  data() {
    return {
      avatar: logo,
      isEditing: false,
      isConfirming: false,
      profileInfo: "",
      GENDERS,
      titles: Object,
      selectTitle: [],
      NO_DATA,
      user: {},
      profile: {},
      selectedRoles: [],
      options: [],
      editRoles: false,
      usersData: [],
      isAdmin: false,
      userId: Number,
      profileInfoTmp: "",
      today: moment.now(),
      rules: {
        name: [
          {
            trigger: ["blur", "change"],
            validator: (_rule, value, callback, _source, _options) => {
              if (value.trim().length === 0) {
                callback(new Error("Team name is required"));
              } else if (value.trim().length > 100 || value.trim().length < 3) {
                callback(
                  new Error(
                    "Profile name  must be between 3 and 100 characters"
                  )
                );
              }
              callback();
            },
          },
        ],
        email: [
          {
            trigger: ["blur", "change"],
            validator: (rule, value, callback, source, options) => {
              if (value.trim().length === 0) {
                callback(new Error("Email is required"));
              } else if (!validateEmail(value)) {
                callback(new Error("Email is Invalid"));
              }
              callback();
            },
          },
        ],
        phone: [
          {
            trigger: ["blur", "change"],
            validator: (rule, value, callback, source, options) => {
              if (value.trim().length === 0) {
                callback(new Error("Phone is required"));
              } else if (!validatePhone(value)) {
                callback(new Error("Phone is Invalid"));
              }
              callback();
            },
          },
        ],
        personal_email: [
          {
            trigger: ["blur", "change"],
            validator: (rule, value, callback, source, options) => {
              if (value.trim().length === 0) {
                callback(new Error("Personal email is required"));
              } else if (!validateEmail(value)) {
                callback(new Error("Email is Invalid"));
              }
              callback();
            },
          },
        ],
        birth_day: [
          {
            trigger: ["blur", "change"],
            validator: (rule, value, callback, source, options) => {
              if (value.trim().length === 0) {
                callback(new Error("Birth day is required"));
              } else if (formatDate(value) >= formatDate(this.today)) {
                callback(new Error("Birthday cannot be in the future!"));
              }
              callback();
            },
          },
        ],
        join_date: [
          {
            trigger: ["blur", "change"],
            validator: (rule, value, callback, source, options) => {
              if (value.trim().length === 0) {
                callback(new Error("Join date is required"));
              } else if (formatDate(value) > formatDate(this.today)) {
                callback(new Error("Join date cannot be in the future!"));
              }
              callback();
            },
          },
        ],
        slack_id: [
          {
            validator: (_rule, value, callback, _source, _options) => {
              if (value.trim().length === 0) {
                callback(new Error("Slack id is required"));
              } else if (value.trim().length !== 11) {
                callback(new Error("Slack Id must bu 11 characters"));
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
    formatDate,
    changeUser(profile_id) {
      this.profileInfo.line_manager = profile_id;
    },

    checkOwnerOrHasScope(scope) {
      return (
        checkOwner(this.userId, this.tokenInfo) ||
        checkHasScope(scope, this.tokenInfo)
      );
    },

    async handleClose() {
      this.editRoles = false;
      await this.$confirm("Save?", "Warning", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
        type: "warning",
      })
        .then(() => {
          GetUserService.updateUserRole(
            this.$route.params.id,
            this.selectedRoles.map((t) => {
              return { id: t };
            })
          ).then((res) => {
            if (res.status === 200) {
              this.$toast.success("Success update role");
              this.fetchData();
            }
          });
        })
        .catch((res) => {
          console.log(res);
          this.$toast.error("Canceled or an error occurred");
        });
    },

    showEditForm() {
      this.isEditing = true;
    },

    saveForm() {
      this.isEditing = false;
      this.isConfirming = true;
    },

    async fetchData() {
      await GetUserService.getCurrentUser(this.$route.params.id)
        .then((response) => {
          if (response.status >= 400) {
            this.$toast.error(ERROR_MESSAGE);
            return;
          }
          if (!response.data.profile) {
            this.$toast.error("Profile data is empty!");
            return;
          }
          this.fetchFieldsFromData(response.data);
          this.user = response.data;
          this.selectedRoles = response.data.roles.map((t) => t.id);
        })
        .catch((res) => {
          console.log(res);
          this.$toast.error(" error occurred");
        });
      this.options = await RoleService.getRoles(100, 1, "").then(
        (res) => res.data.results
      );
    },

    fetchFieldsFromData(data) {
      this.profileInfo = {
        id: data.profile.id,
        name: data.profile.name,
        email: data.email,
        gender: data.profile.gender,
        join_date: data.profile.join_date,
        personal_email: data.profile.personal_email,
        phone: data.profile.phone,
        slack_id: data.profile.slack_id,
        title: data.title,
        birth_day: data.profile.birth_day,
        line_manager: data.profile.line_manager,
        line_manager_user_name: data.profile.line_manager_user_name,
        maximum_level_approved: data.profile.maximum_level_approved,
        user: data.profile.user,
      };
      this.profileInfoTmp = {
        join_date: data.profile.join_date,
        birth_day: data.profile.birth_day,
      };
      this.selectTitle = data.title.map((e) => e.id);
      if (this.profileInfo.gender !== undefined) {
        this.profileInfo.gender = this.GENDERS.find(
          (gender) => gender.value === this.profileInfo.gender
        );
      }
      if (!this.profileInfo.title) {
        this.profileInfo.title = {
          id: null,
          title: "Empty",
        };
      }

      this.avatar = data.profile.image ? data.profile.image : logo;
    },

    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.showConfirmDialog();
        } else {
          this.$toast.error("Input is invalid!");
          return false;
        }
      });
    },

    showConfirmDialog() {
      this.isConfirming = true;
    },

    cancelConfirm() {
      this.isConfirming = false;
    },

    async saveData() {
      this.isConfirming = false;
      const gender = this.profileInfo.gender;
      const title = this.selectTitle;
      let titles = this.titles;
      this.profileInfo.birth_day =
        this.profileInfo.birth_day === null
          ? this.profileInfoTmp.birth_day
          : this.profileInfo.birth_day;
      this.profileInfo.join_date =
        this.profileInfo.join_date === null
          ? this.profileInfoTmp.join_date
          : this.profileInfo.join_date;
      if (title) {
        title.forEach((id, index) => {
          let titleName = titles.find((el) => el.id === id).title;
          title[index] = { id: id, title: titleName };
        });
        this.profileInfo.title = title;
      } else {
        delete this.profileInfo.title;
      }
      if (gender !== undefined) {
        this.profileInfo.gender = gender.value;
      }
      await GetUserService.updateGeneralProfile(this.profileInfo)
        .then((res) => {
          if (res.status === 200) {
            this.$toast.success("Updated Successfully");
            this.$emit("reloadRemainLeave");
          }
        })
        .catch(() => {
          this.$toast.error("Updated Failed");
          this.$emit("reloadRemainLeave");
        });
      if (!this.profileInfo.title) {
        this.profileInfo.title = {
          id: null,
          title: "Empty",
        };
      }
      this.profileInfo.gender = gender;
      this.isEditing = false;
      await this.fetchData();
    },

    async onFilePicked(event) {
      this.selectedImage = event.target.files[0];
      const formData = new FormData();
      formData.append("image", this.selectedImage);
      const res = await UserService.changeAvatar(this.profileInfo.id, formData);
      if (res && res.status === 200) {
        this.$toast.success("Updated Successfully!");
        this.avatar = res.data.image;
        if (this.profileInfo.user === localStorage.getItem("user_id")) {
          localStorage.setItem("imageUrl", res.data.image);
          this.$store.dispatch("user/changeAvatar", this.avatar);
        }
      } else {
        this.$toast.error("Update Failed");
      }
    },

    onPickFile() {
      this.$refs.avatarInput.click();
    },
  },

  async created() {
    const titleResponseData = await GetUserService.getAllTitles();
    this.titles = titleResponseData.data;
    await this.fetchData();
    this.usersData = this.usersData.concat(this.allUsers);
    this.userId = this.$route.params.id;
    this.isAdmin = checkHasScope(
      "user:edit_public_user_information_list",
      this.tokenInfo
    );
  },
  computed: {
    ...mapGetters({ allUsers: "user/allUsers", tokenInfo: "scope/tokenInfo" }),
  },
};
</script>

<style lang="scss" scoped>
* {
  font-family: "Times New Roman", Times, serif;
}

.header-container {
  height: 150px;
  display: flex;
  align-items: center;
  align-content: center;
  border-radius: 20px;
  border: 1px solid gray;
  background-color: #fff;

  .avatar-block {
    width: 120px;
    height: 120px;
    margin-left: 15px;
    margin-right: 25px;
    position: relative;
    border-radius: 50%;
    cursor: pointer;

    img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      border: 1px solid #707070;
    }

    .avatar-mask {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      border-radius: 50%;
      background-color: #000;
      opacity: 0.6;
      font-size: 18px;
      text-align: center;
      color: white;
      line-height: 120px;
    }

    &:hover .avatar-mask {
      animation: scale-display 0.3s;
      display: initial;
    }

    &:not(:hover) .avatar-mask {
      animation: scale-display--reversed 0.3s;
      animation-fill-mode: forwards;
    }
  }

  .content {
    display: flex;
    flex-direction: column;
    height: 100%;
    flex: 1;
    border: none;

    .name-block {
      height: 50%;
      display: block;
      position: relative;

      p {
        font-size: 30px;
        position: absolute;
        bottom: 0px;
        font-weight: 500;
      }
    }

    .change-avatar-block {
      font-size: 20px;
      color: #43c9d0;
      height: 50%;
      position: relative;

      p {
        position: absolute;
        top: 15px;
      }
    }
  }

  @keyframes scale-display {
    0% {
      opacity: 0;
      transform: scale(0);
      -webkit-transform: scale(0);
    }

    100% {
      opacity: 0.6;
      transform: scale(1);
      -webkit-transform: scale(1);
    }
  }

  @keyframes scale-display--reversed {
    0% {
      display: inline-flex;
      opacity: 0.6;
      transform: scale(1);
      -webkit-transform: scale(1);
    }
    99% {
      display: inline-flex;
      opacity: 0;
      transform: scale(0);
      -webkit-transform: scale(0);
    }
    100% {
      display: none;
      opacity: 0;
      transform: scale(0);
      -webkit-transform: scale(0);
    }
  }
}
</style>
