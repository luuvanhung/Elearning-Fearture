<template>
  <div class="background container-fluid">
    <div class="row justify-content-center m-0">
      <div class="col-10 col-xl-4 col-lg-4 text-center">
        <img class="icon" src="@/static/images/logo-paradox-white-01.png" />
      </div>
    </div>
    <div v-show="password.new === password.confirm"></div>
    <div class="hero-content text-info">
      <div class="container">
        <!-- Outer Row -->
        <div class="row justify-content-center">
          <div class="col-xl-4 col-lg-4 col-md-6 col-sm-8 col-12">
            <div class="my-5">
              <el-card class="box-card py-4" shadow="always">
                <div class="text-center">
                  <h1 class="h4 text-info mb-3 font-weight-bold">
                    Reset Password
                  </h1>
                </div>
                <div class="form-controler">
                  <el-form
                    id="reset-pass"
                    class="reset-pass-form"
                    method="POST"
                    ref="form"
                    @submit.native.prevent="checkForm"
                    @keyup.enter="checkForm"
                    label-width="0px"
                  >
                    <div v-if="error !== ''" class="text-danger">
                      {{ error }}
                    </div>
                    <br />
                    <el-form-item prop="email">
                      <el-input
                        id="email"
                        v-model="password.new"
                        type="password"
                        class="form-control form-control-user"
                        placeholder="New Password"
                      ></el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                      <el-input
                        id="password"
                        v-model="password.confirm"
                        type="password"
                        class="form-control form-control-user"
                        placeholder="Confirm Password"
                      ></el-input>
                    </el-form-item>
                    <hr />
                    <el-form-item>
                      <el-button
                        class="reset-pass-button"
                        type="primary"
                        native-type="submit"
                        block
                        >Reset
                      </el-button>
                    </el-form-item>
                  </el-form>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  middleware: "afterlogin",
  data() {
    return {
      password: {
        new: "",
        confirm: "",
      },
      error: "",
    };
  },
  methods: {
    checkForm() {
      if (this.password.new === "") {
        this.error = "New password required";
      } else if (this.password.confirm === "") {
        this.error = "Confirm password required";
      } else if (this.password.new.length < 6) {
        this.error = "Password must be at least 6 characters";
      } else if (this.password.new !== this.password.confirm) {
        this.error = "New password and confirm password does not match";
      } else {
        this.error = "";
        const formdata = new FormData();
        formdata.append("token", this.$route.query.token);
        formdata.append("password", this.password.new);
        this.password = {
          new: "",
          confirm: "",
        };
        axios
          .put(`/actions/change-password`, formdata)
          .then(() => {
            this.$router.push("/login");
          })
          .catch((e) => {
            console.log(e);
            this.error = "Token is not valid";
          });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
html body {
  .background {
    background: #25c9d0;
    min-height: 100vh;
  }

  .reset-pass-form {
    margin: 0 20px;
  }

  .reset-pass-button {
    width: 100%;
    margin-top: 20px;
    border-radius: 50px;
    font-weight: bold;
  }

  .reset-pass-button:hover {
    background-color: #2a96a5;
  }

  .icon {
    margin-top: 3%;
    width: 100%;
    min-width: 50px;
  }

  hr {
    background-color: #8d8d8d !important;
    opacity: 0.25;
    height: 3px;
  }

  .no-underline {
    color: #17a2b8;
  }

  .btn-search {
    background-color: #25c9d0;
  }

  .no-underline:hover {
    text-decoration: none;
    color: black;
  }

  .pointer {
    cursor: pointer;
  }
}
</style>
