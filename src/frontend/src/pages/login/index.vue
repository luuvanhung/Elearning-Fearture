<template>
  <div class="background">
    <div class="row justify-content-center m-0">
      <div class="col-10 col-xl-4 col-lg-4 text-center">
        <img
          class="icon"
          src="@/static/images/logo-paradox-white-01.png"
          alt="logo"
          style="margin-top: 10vh"
        />
      </div>
    </div>

    <div class="hero-content text-info">
      <div
        id="loginform"
        class="container"
        v-show="checkForgotPassword === false"
      >
        <!-- Outer Row -->
        <div class="row justify-content-center">
          <div class="col-xl-5 col-lg-5 col-md-8 col-sm-12 col-12">
            <div class="my-5">
              <el-card class="box-card py-4" shadow="always">
                <div class="text-center">
                  <h1 class="h4 text-info mb-3 font-weight-bold">
                    Welcome Back!
                  </h1>
                </div>
                <div class="form-controller">
                  <el-form
                    ref="formLogin"
                    :model="loginFormData"
                    @submit.native.prevent="login('formLogin')"
                    @keyup.enter="login"
                    label-width="120px"
                  >
                    <el-form-item
                      label-width="0px"
                      prop="email"
                      :rules="rules.email"
                    >
                      <el-input
                        v-model="loginFormData.email"
                        aria-describedby="emailHelp"
                        type="email"
                        class="form-control form-control-user"
                        placeholder="Email Address"
                        clearable
                      ></el-input>
                    </el-form-item>
                    <el-form-item
                      label-width="0px"
                      prop="password"
                      :rules="rules.password"
                    >
                      <el-input
                        v-model="loginFormData.password"
                        type="password"
                        class="form-control form-control-user"
                        placeholder="Password"
                        clearable
                      ></el-input>
                    </el-form-item>
                    <hr />
                    <el-form-item label-width="0px">
                      <el-button
                        :loading="loading"
                        class="login-button"
                        type="primary"
                        native-type="submit"
                        block
                        >Login</el-button
                      >
                    </el-form-item>
                    <el-form-item label-width="0px">
                      <el-button
                        size="medium"
                        round
                        @click.prevent="loginWithGoogle"
                        class="google-button"
                      >
                        <span>
                          <img
                            alt="Google login"
                            src="../../static/images/googleIcon.svg"
                          />
                          <span class="text-login">Login with Google</span>
                        </span>
                      </el-button>
                      <div v-if="error !== ''" class="text-danger">
                        {{ error }}
                      </div>
                    </el-form-item>
                  </el-form>
                </div>
                <div class="text-center mt-3">
                  <a
                    class="no-underline pointer"
                    title="Click to find your password"
                    @click="displayForgotPassBox"
                    >Forgot password?</a
                  >
                </div>
                <div class="text-center mt-3">
                  <a class="no-underline pointer" href="terms-of-use/"
                    >Term of use</a
                  >
                  <a class="no-underline pointer">|</a>
                  <a class="no-underline pointer" href="privacy-policy/"
                    >Privacy policy</a
                  >
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </div>
      <div class="container" v-show="checkForgotPassword === true">
        <div class="row justify-content-center">
          <div class="col-xl-6 col-lg-6 col-md-8 col-sm-12 col-12">
            <div class="card o-hidden border-0 shadow-lg my-5" v-if="!success">
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <div class="text-center">
                    <h1 class="h4 text-info mt-3 font-weight-bold">
                      Find your account
                    </h1>
                  </div>
                </div>
                <div class="form-controller">
                  <div class="row">
                    <div
                      class="col-12 alert color-danger mt-2"
                      v-show="forgotPassError.title !== ''"
                    >
                      <el-alert type="error">
                        <strong>{{ forgotPassError.title }}</strong>
                        <br />
                        {{ forgotPassError.content }}
                      </el-alert>
                    </div>
                    <div class="col-12 mx-auto text-dark my-2 text-center">
                      Please enter your email address:
                    </div>
                    <div class="col-12">
                      <el-form
                        class="login-form"
                        ref="formForgotPass"
                        :model="forgotPassFormData"
                        @submit.native.prevent="submitForgotPassBox"
                        @keyup.enter="submitForgotPassBox"
                      >
                        <el-form-item
                          :rules="rules.email"
                          label-width="0px"
                          prop="emailToGetPassword"
                        >
                          <el-input
                            class="w-100 p-1 form-control"
                            v-model="forgotPassFormData.emailToGetPassword"
                            type="email"
                            placeholder="Email address"
                            aria-label="email address"
                            clearable
                          ></el-input>
                        </el-form-item>
                        <el-form-item class="text-right">
                          <el-button type="info" @click="displayForgotPassBox"
                            >Cancel</el-button
                          >
                          <el-button type="primary" @click="submitForgotPassBox"
                            >Send reset password email</el-button
                          >
                        </el-form-item>
                      </el-form>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>
            <div class="card o-hidden border-0 shadow-lg my-5" v-else>
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <div class="text-center">
                    <h1 class="h4 text-info mt-3 font-weight-bold">Success</h1>
                  </div>
                </div>
                <div class="card-body mb-3">
                  <div class="row">
                    <el-alert type="success">
                      Reset password link had been sent to email
                      {{ forgotPassFormData.emailToGetPassword }}.
                    </el-alert>
                  </div>
                </div>
                <div class="card-footer text-right">
                  <div class="justify-content-end d-flex">
                    <el-button type="primary" @click="displayForgotPassBox"
                      >Return to login</el-button
                    >
                  </div>
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
import authenticationServices from "@/services/authentication/authentication.services.js";
import Oauth2Service from "@/services/authentication/oauth2.services.js";
import GetUserService from "@/services/user/getUser";
import messageResponse from "@/services/authentication/responseMessage";
import { mapActions } from "vuex";

const { validateEmail } = require("../../utils/validation");

export default {
  name: "login",
  middleware: "afterlogin",
  data() {
    return {
      forgotPassFormData: {
        emailToGetPassword: "",
      },
      error: "",
      loginFormData: {
        email: "",
        password: "",
      },
      checkForgotPassword: false,
      forgotPassError: {
        title: "",
        content: "",
      },
      success: false,
      loading: false,
      isSubmit: false,
      token: "",
      user: "",
      rules: {
        email: [
          {
            validator: async (_rule, value, callback, _source, _options) => {
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
              if (this.isSubmit) {
                this.token = await Oauth2Service.login(this.loginFormData);
                if (!this.token) {
                  this.isSubmit = false;
                  callback(
                    new Error(messageResponse.AUTHENTICATION.INCORRECT_ACCOUNT)
                  );
                }
                this.user = await GetUserService.getCurrentUser(this.token.sub);
                if (!this.user) {
                  this.isSubmit = false;
                  callback(
                    new Error(messageResponse.AUTHENTICATION.INCORRECT_ACCOUNT)
                  );
                }
              }
              callback();
            },
            trigger: "change",
          },
        ],
        password: [
          {
            validator: (_rule, _value, callback, _source, _options) => {
              if (this.loginFormData.password.length < 6) {
                callback(new Error(messageResponse.VALIDATION.PASSWORD));
              }
              callback();
            },
            trigger: "change",
          },
        ],
      },
    };
  },
  head() {
    return {
      title: "Login",
    };
  },
  methods: {
    ...mapActions("user", ["setCurrentUser"]),

    submitForgotPassBox: async function () {
      this.forgotPassError = {
        title: "",
        content: "",
      };
      const formData = new FormData();
      formData.append("email", this.forgotPassFormData.emailToGetPassword);

      const responseResult = await authenticationServices.forgotPassword(
        formData
      );
      if (responseResult) {
        this.success = true;
      } else {
        this.forgotPassError.title = messageResponse.SEARCH_RESULT.TITLE;
        this.forgotPassError.content = messageResponse.SEARCH_RESULT.CONTENT;
      }
    },

    displayForgotPassBox() {
      this.checkForgotPassword = !this.checkForgotPassword;
      this.forgotPassError = {
        title: "",
        content: "",
      };
      this.forgotPassFormData.emailToGetPassword = "";
      this.success = false;
    },

    login: async function (formName) {
      this.isSubmit = true;
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          this.loading = true;
          const { id, email, profile, admin } = this.user.data;
          const userData = {
            user: id,
            email: email,
            name: profile.name,
            profile_id: profile.id,
            is_admin: admin,
          };
          this.$store.commit("user/SET_CURRENT_USER", userData);
          localStorage.setItem("email", email);
          localStorage.setItem("user_id", id);
          localStorage.setItem("profile_id", profile.id);
          localStorage.setItem("is_admin", admin);
          localStorage.setItem("imageUrl", profile.image);
          localStorage.setItem("name", profile.name);
          this.loading = false;
          if (this.$router.currentRoute.name === "Login") {
            await this.$router.push("/");
            this.$router.go(0);
          }
        }
      });
    },

    loginWithGoogle: async function () {
      const googleUser = await this.$gAuth.signIn();
      const id_token = googleUser.Cc.id_token;
      const token = await Oauth2Service.loginWithGoogle(id_token);
      if (token) {
        const user = await GetUserService.getCurrentUser(token.sub);
        if (user) {
          const { id, email, profile, active, admin } = user.data;
          if (!active) {
            this.error = messageResponse.AUTHENTICATION.USER_DEACTIVATED;
            this.loginFormData.password = "";
            return;
          }
          const userData = {
            user: id,
            email: email,
            name: profile.name,
            profile_id: profile.id,
            is_admin: admin,
          };
          this.$store.commit("user/SET_CURRENT_USER", userData);
          localStorage.setItem("email", email);
          localStorage.setItem("user_id", id);
          localStorage.setItem("profile_id", profile.id);
          localStorage.setItem("is_admin", admin);
          localStorage.setItem("imageUrl", profile.image);
          localStorage.setItem("name", profile.name);
          if (this.$router.currentRoute.name === "Login") {
            await this.$router.push("/");
            this.$router.go(0);
          }
        } else {
          this.error = messageResponse.AUTHENTICATION.INCORRECT_ACCOUNT;
          this.loginFormData.email = "";
          this.loginFormData.password = "";
        }
      } else this.error = messageResponse.AUTHENTICATION.ACCOUNT_NOT_EXIST;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "index.scss";
</style>
