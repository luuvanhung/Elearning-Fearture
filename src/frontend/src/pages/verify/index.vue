<template>
  <div class="verify-page">
    <div class="my-2">
      <div class="table-responsive mx-auto p-auto col-md-6">
        <div class="text-info text-center title">
          <h1>Verify account</h1>
          <h2>Welcome to our company!</h2>
        </div>
        <el-form
          :model="passwordForm"
          status-icon
          :rules="rules"
          ref="passwordForm"
          label-width="120px"
        >
          <el-form-item label="Password" prop="pass">
            <el-input
              type="password"
              v-model="passwordForm.pass"
              autocomplete="off"
            ></el-input>
          </el-form-item>
          <el-form-item label="Confirm" prop="checkPass">
            <el-input
              type="password"
              v-model="passwordForm.checkPass"
              autocomplete="off"
            ></el-input>
          </el-form-item>
          <el-form-item class="center-element">
            <el-button
              type="primary"
              @click="handleSubmitVerify('passwordForm')"
            >
              Verify
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script>
import { accessToken } from "@/helper/accessToken";
import UserService from "@/services/user/user";

export default {
  name: "id_verify",
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please input the password"));
      } else {
        if (this.passwordForm.checkPass !== "") {
          this.$refs.passwordForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("Please input the password again"));
      } else if (value !== this.passwordForm.pass) {
        callback(new Error("Two inputs don't match!"));
      } else {
        callback();
      }
    };

    return {
      passwordForm: {
        pass: "",
        checkPass: "",
      },
      rules: {
        pass: [
          {
            required: true,
            message: "Please input the password",
            trigger: "blur",
          },
          {
            min: 6,
            message: "Password must be more than 6 characters",
            trigger: "blur",
          },
          { validator: validatePass, trigger: "blur" },
        ],
        checkPass: [
          {
            required: true,
            message: "Please input the password confirm",
            trigger: "blur",
          },
          {
            min: 6,
            message: "Password must be more than 6 characters",
            trigger: "blur",
          },
          { validator: validatePass2, trigger: "blur" },
        ],
      },
      show: false,
    };
  },
  created() {
    if (accessToken()) {
      localStorage.clear();
    }
  },
  methods: {
    async handleVerifyUser() {
      const body = {
        token: this.$route.query.token,
        password: this.passwordForm.pass,
      };
      const res = await UserService.verifyUser(body);
      if (res == true) {
        this.$toast.success("Your password is changed successfully");
        this.goToHomePage(3);
      } else {
        let msg = "Error";
        if (res.data.msg && res.data.msg[0]) msg = res.data.msg[0];
        this.$toast.error(msg);
      }
    },
    handleSubmitVerify(formName) {
      this.$refs[formName].validate((valid) => {
        if (!valid) return false;
        this.handleVerifyUser();
      });
    },
    goToHomePage(delaySeconds = 1) {
      setTimeout(() => {
        this.$router.push("/login");
      }, 1000 * delaySeconds);
    },
  },
};
</script>

<style lang="scss">
.verify-page {
  .title {
    h1 {
      margin: 10px;
    }
    h2 {
      margin-bottom: 20px;
    }
  }

  .center-element {
    display: flex;
    justify-content: center;

    .el-form-item__content {
      margin-left: 0 !important;
    }
  }
}
</style>
