<template>
  <div class="navbar-container col-md-9 col-xl-10 px-0">
    <el-menu
      mode="horizontal"
      background-color="#FFFFFF"
      text-color="#000000"
      active-text-color="#25c9d0"
      menu-trigger="click"
      class="row"
    >
      <el-menu-item
        index="1"
        class="d-md-none bg-color-primary col-2 col-sm-1 col-md-0 px-0"
      >
        <div class="menu-mobile">
          <div class="menu" @click="changeValue">
            <font-awesome-icon
              :icon="['fas', 'bars']"
              class="nav-icon text-white"
              v-if="!isCollapse"
            />
            <font-awesome-icon
              :icon="['fas', 'times']"
              class="nav-icon text-white"
              v-else
            />
          </div>
        </div>
        <MobileSiderbar />
      </el-menu-item>
      <div
        class="col-10 col-sm-11 col-md-12 col-xl-12 d-flex justify-content-end pr-0"
      >
        <el-submenu index="2">
          <template slot="title">
            <img
              v-if="hasProfileImg()"
              class="img-fluid rounded-circle"
              :src="imageUrl"
              alt="profile"
            />
            <img
              v-else
              class="img-fluid rounded-circle"
              src="@/static/images/icon-whitebg.jpg"
              alt="profile default"
            />
            <span class="mx-1 fontsize-18px name"> {{ name }}</span>
          </template>
          <el-menu-item index="2-1">
            <router-link
              class="my-2 btn btn-block text-left"
              :to="'/profile/' + profileId"
            >
              <li class="ml-auto mt-1">Profile</li>
            </router-link>
          </el-menu-item>
          <el-menu-item index="2-2">
            <router-link
              class="my-2 btn btn-block text-left"
              to="/changepassword"
              ><li class="ml-auto mt-1 text-muted">Change password</li>
            </router-link>
          </el-menu-item>
          <li class="divider">
            <el-divider></el-divider>
          </li>
          <el-menu-item index="2-3" @click="logout">
            <li class="ml-auto mb-1">
              <a class="my-2 btn btn-block text-left"> Logout </a>
            </li>
          </el-menu-item>
        </el-submenu>
        <el-menu-item
          index="1"
          class="d-md-none bg-color-primary col-2 col-sm-1 px-0"
        >
          <div class="menu-mobile">
            <img
              src="@/static/images/logoParadox.png"
              class="logoCollapse"
              alt="logo"
            />
          </div>
        </el-menu-item>
      </div>
    </el-menu>
  </div>
</template>
<script>
import { mapActions, mapState, mapGetters } from "vuex";
import Oauth2Service from "@/services/authentication/oauth2.services";
import MobileSiderbar from "@/components/MobileSiderbar.vue";

export default {
  data() {
    return {
      profileId: localStorage.getItem("user_id"),
      email: localStorage.getItem("email"),
      name: localStorage.getItem("name"),
      imageUrl: localStorage.getItem("imageUrl"),
    };
  },
  components: {
    MobileSiderbar,
  },
  computed: {
    ...mapGetters({
      isCollapse: "value",
    }),
    ...mapState({
      newImageUrl: (state) => state.user.currentUser.imageUrl,
    }),
  },
  created() {
    this.fetchData();
  },
  watch: {
    $route: function () {
      this.fetchData();
    },
    newImageUrl: function () {
      this.imageUrl = this.newImageUrl;
    },
  },
  methods: {
    ...mapActions(["changeValue"]),
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
    fetchData() {
      this.imageUrl = localStorage.getItem("imageUrl");
    },
    hasProfileImg() {
      return (this.imageUrl !== "null") & (this.imageUrl !== "undefined");
    },
    handleTogle() {
      /* TODO document why this method 'handleTogle' is empty */
    },
  },
};
</script>
<style lang="scss" scoped>
.menu-mobile {
  text-align: center;
}

.nav-icon {
  font-size: 40px;
}

.logoCollapse {
  width: 100% !important;
}

.navbar-container {
  position: fixed;
  width: 100%;
  z-index: 9999;
}

li,
a {
  color: #707070;
  text-decoration: none;

  * {
    font-family: "Times New Roman", Times, serif;
  }
}

.fontsize-18px {
  font-size: 18px;
}

img {
  max-width: 40px;
  height: 40px;
}

.rounded-circle {
  border-radius: 50%;
}

.el-divider {
  margin: 5px 15px 5px 0px;
}

.el-menu-item {
  border-bottom: none !important;
}

.divider {
  padding: 0 10px;
}

.menu {
  position: absolute;
  width: 100%;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
  background-color: #25c9d0;
}
</style>
