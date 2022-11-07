<template>
  <div class="bg-light" :key="$route.params.id">
    <div v-if="isLoadingMask" class="lmask" ref="loading-mask"></div>
    <div :style="{ visibility: !isLoadingMask ? 'visible' : 'hidden' }">
      <GeneralInformation @reloadRemainLeave="setReloadRemainLeave" />
      <RemainLeave
        :key="reloadRemainLeave"
        v-if="checkOwnerOrHasScope('user:view_private_user_information_list')"
      ></RemainLeave>
      <CurrentSkillInformation />
      <TargetSkillInformation />
      <IdentityInformation
        v-if="checkOwnerOrHasScope('user:view_private_user_information_list')"
      ></IdentityInformation>
      <ContactInformation
        v-if="checkOwnerOrHasScope('user:view_private_user_information_list')"
      ></ContactInformation>
      <BankAccountInformation
        v-if="checkOwnerOrHasScope('user:view_private_user_information_list')"
      ></BankAccountInformation>
      <InsuranceInformation
        v-if="checkOwnerOrHasScope('user:view_private_user_information_list')"
      ></InsuranceInformation>
      <EducationInformation
        v-if="checkOwnerOrHasScope('user:view_private_user_information_list')"
      ></EducationInformation>
      <div class="d-flex justify-content-center mb-3" style="gap: 1rem">
        <restricted-view :scope="['user:activate_user']">
          <template v-slot:default>
            <div class="text-center">
              <el-button
                v-show="user.active === true"
                type="danger"
                @click="showModal(user.id)"
              >
                Deactivate User
              </el-button>
              <el-button
                v-show="user.active === false"
                type="primary"
                @click="active(user.id)"
              >
                Active User
              </el-button>
            </div>
          </template>
        </restricted-view>
        <restricted-view :scope="['user:destroy']">
          <template v-slot:default>
            <div class="text-center">
              <el-button type="danger" @click="showConfirmDeleteUser = true">
                Delete User
              </el-button>
            </div>
          </template>
        </restricted-view>
      </div>
    </div>
    <el-dialog :visible.sync="isDeactivate" title="Deactivate User">
      <div class="d-block text-center text-danger mb-4">
        <h3>Do you want to deactivate this user ?</h3>
      </div>
      <div class="row">
        <el-button
          class="mt-3 mx-auto col-4"
          type="primary"
          @click="cancelDeActiveUser"
        >
          Cancel
        </el-button>
        <el-button
          class="mt-3 mx-auto col-4"
          type="danger"
          @click="deactivateUser"
        >
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="showConfirmDeleteUser" title="Delete User">
      <div class="d-block text-center text-danger mb-4">
        <h3>Do you want to delete this user ?</h3>
      </div>
      <div class="row">
        <el-button
          class="mt-3 mx-auto col-4"
          type="primary"
          @click="cancelDeleteUser"
        >
          Cancel
        </el-button>
        <el-button class="mt-3 mx-auto col-4" type="danger" @click="deleteUser">
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import GeneralInformation from "./components/general.vue";
import IdentityInformation from "./components/identity.vue";
import ContactInformation from "./components/contact.vue";
import BankAccountInformation from "./components/bank.vue";
import InsuranceInformation from "./components/insurance.vue";
import EducationInformation from "./components/education.vue";
import CurrentSkillInformation from "./components/currentSkill";
import TargetSkillInformation from "./components/targetSkill";
import RemainLeave from "./components/RemainLeave";
import RestrictedView from "@/components/RestrictedView";
import GetUserService from "@/services/user/getUser";
import userService from "@/services/user/user";
const { checkOwner, checkHasScope } = require("../../../utils/validation");

import { mapGetters } from "vuex";

export default {
  name: "profile",
  components: {
    GeneralInformation,
    RemainLeave,
    IdentityInformation,
    ContactInformation,
    BankAccountInformation,
    InsuranceInformation,
    EducationInformation,
    CurrentSkillInformation,
    TargetSkillInformation,
    RestrictedView,
  },
  async created() {
    setTimeout(this.disableMask, 1000);
    await this.asyncData();
  },
  data() {
    return {
      userId: this.$route.params.id,
      isLoadingMask: true,
      currentId: "",
      user: "",
      isDeactivate: false,
      showConfirmDeleteUser: false,
      reloadRemainLeave: false,
    };
  },
  watch: {
    $route(to, from) {
      this.asyncData();
    },
  },
  methods: {
    checkOwnerOrHasScope(scope) {
      return (
        checkOwner(this.userId, this.tokenInfo) ||
        checkHasScope(scope, this.tokenInfo)
      );
    },
    setReloadRemainLeave() {
      this.reloadRemainLeave = !this.reloadRemainLeave;
    },
    disableMask() {
      this.isLoadingMask = false;
    },
    showModal(id) {
      this.isDeactivate = true;
      this.currentID = id;
    },
    cancelDeActiveUser() {
      this.isDeactivate = false;
    },
    cancelDeleteUser() {
      this.showConfirmDeleteUser = false;
    },
    async asyncData() {
      const response = await GetUserService.getCurrentUser(
        this.$route.params.id
      );
      this.user = response.data;
    },
    active: function (id) {
      userService
        .activeUser(id)
        .then(() => {
          this.user.active = true;
          this.$toast.success("Activate User Successfully");
        })
        .catch((e) => {
          console.log(e);
        });
    },
    deactivateUser: async function () {
      await userService
        .deactivateUser(this.user.id)
        .then(() => {
          this.isDeactivate = false;
          this.user.active = false;
          this.$toast.success("Deactivate User Successfully");
        })
        .catch((e) => {
          console.log(e);
        });
    },
    async deleteUser() {
      const result = await userService.deleteUser(this.user.id);
      if (result) {
        this.$toast.success("Delete User Successfully");
        this.$router.push("/employeelist");
      }
    },
  },
  computed: {
    ...mapGetters({ tokenInfo: "scope/tokenInfo" }),
  },
};
</script>

<style lang="scss" scoped>
.lmask {
  position: sticky;
  height: calc(100vh - 110px);
  width: 100%;
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
  z-index: 0;
  opacity: 0.4;

  &.fixed {
    position: fixed;
  }

  &:before {
    content: "";
    background-color: rgba(0, 0, 0, 0);
    border: 5px solid rgba(0, 183, 229, 0.9);
    opacity: 0.9;
    border-right: 5px solid rgba(0, 0, 0, 0);
    border-left: 5px solid rgba(0, 0, 0, 0);
    border-radius: 50px;
    box-shadow: 0 0 35px #2187e7;
    width: 50px;
    height: 50px;
    -moz-animation: spinPulse 1s infinite ease-in-out;
    -webkit-animation: spinPulse 1s infinite linear;

    margin: -25px 0 0 -25px;
    position: absolute;
    top: 50%;
    left: 50%;
  }

  &:after {
    content: "";
    background-color: rgba(0, 0, 0, 0);
    border: 5px solid rgba(0, 183, 229, 0.9);
    opacity: 0.9;
    border-left: 5px solid rgba(0, 0, 0, 0);
    border-right: 5px solid rgba(0, 0, 0, 0);
    border-radius: 50px;
    box-shadow: 0 0 15px #2187e7;
    width: 30px;
    height: 30px;
    -moz-animation: spinoffPulse 1s infinite linear;
    -webkit-animation: spinoffPulse 1s infinite linear;

    margin: -15px 0 0 -15px;
    position: absolute;
    top: 50%;
    left: 50%;
  }
}

@-moz-keyframes spinPulse {
  0% {
    -moz-transform: rotate(160deg);
    opacity: 0;
    box-shadow: 0 0 1px #2187e7;
  }
  50% {
    -moz-transform: rotate(145deg);
    opacity: 1;
  }
  100% {
    -moz-transform: rotate(-320deg);
    opacity: 0;
  }
}

@-moz-keyframes spinoffPulse {
  0% {
    -moz-transform: rotate(0deg);
  }
  100% {
    -moz-transform: rotate(360deg);
  }
}

@-webkit-keyframes spinPulse {
  0% {
    -webkit-transform: rotate(160deg);
    opacity: 0;
    box-shadow: 0 0 1px #2187e7;
  }
  50% {
    -webkit-transform: rotate(145deg);
    opacity: 1;
  }
  100% {
    -webkit-transform: rotate(-320deg);
    opacity: 0;
  }
}

@-webkit-keyframes spinoffPulse {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}
</style>
