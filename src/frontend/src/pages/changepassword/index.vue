<template>
  <div class="bg-light">
    <div>
      <el-form class="mt-3" label-width="180px">
        <el-form-item label="Current Password *">
          <el-input
            v-model="currentPassword"
            type="password"
            style="width: 40%"
          />
        </el-form-item>
        <el-form-item label="New Password *">
          <el-input v-model="newPassword" type="password" style="width: 40%" />
        </el-form-item>
        <el-form-item label="Confirm Password *">
          <el-input
            v-model="repeatedNewPassword"
            type="password"
            style="width: 40%"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submit">Save</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import UserService from "@/services/user/user";
import Oauth2Service from "@/services/authentication/oauth2.services";

export default {
  name: "id_change_password",
  middleware: "authentication",
  data() {
    return {
      currentPassword: "",
      newPassword: "",
      repeatedNewPassword: "",
    };
  },
  methods: {
    submit: function () {
      if (this.check_form()) {
        const formData = new FormData();
        const id = localStorage.getItem("user_id");
        formData.append("current_password", this.currentPassword);
        formData.append("new_password", this.newPassword);
        UserService.changePassword(id, formData)
          .then(() => {
            this.logout();
          })
          .catch((e) => {
            this.$toast.error("Your current password is incorrect");
          });
      }
    },
    check_form() {
      let error;
      if (this.currentPassword.length < 6) {
        error =
          this.currentPassword.length == 0
            ? "Please enter current password"
            : "Current password need more than 6 characters";
        this.currentPassword = "";
      } else if (this.newPassword.length < 6) {
        error =
          this.newPassword.length == 0
            ? "Please enter new password"
            : "New password need more than 6 characters";
        this.newPassword = "";
      } else if (this.repeatedNewPassword.length < 6) {
        error =
          this.repeatedNewPassword.length == 0
            ? "Please enter confirm password"
            : "Confirm password must more than 6 characters";
        this.repeatedNewPassword = "";
      } else if (this.newPassword !== this.repeatedNewPassword) {
        error = "Confirm password is incorrect";
        this.repeatedNewPassword = "";
      }
      if (error) {
        this.$toast.error(error);
      }
      return !error;
    },
    logout() {
      try {
        this.token = "";
        if (Oauth2Service.logout()) {
          this.$router.push("/login");
        }
      } catch (e) {
        localStorage.clear();
        this.$router.push("/login");
      }
    },
  },
};
</script>
<style lang="scss" scoped></style>
