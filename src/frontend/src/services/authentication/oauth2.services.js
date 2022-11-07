import BaseService from "../base";
import { accessToken } from "@/helper/accessToken";
import { refreshToken } from "@/helper/refreshToken";
import { getConfigApp } from "@/helper/getConfigApp";
import { storeTokenToVuex } from "@/helper/storeTokenToVuex";

class Oauth2Service extends BaseService {
  get entity() {
    return "oauth2";
  }

  async loginWithGoogle(id_token) {
    try {
      const formData = new FormData();
      formData.append("token", id_token);
      const response = await this.request().post(
        `authenservice/login/google/`,
        formData
      );
      if (response) {
        const { access_token, refresh_token } = response.data;
        return storeTokenToVuex(access_token, refresh_token);
      }
    } catch (e) {
      console.log(e);
    }
  }

  async login(data) {
    const app = getConfigApp();
    app.append("username", data?.email);
    app.append("password", data?.password);
    try {
      const response = await this.request().post(`${this.entity}/login`, app);
      if (response) {
        const { access_token, refresh_token } = response.data;
        return storeTokenToVuex(access_token, refresh_token);
      }
    } catch (e) {
      console.log(e);
    }
  }

  async logout() {
    const app = getConfigApp();
    app.append("access_token", accessToken());
    app.append("refresh_token", refreshToken());
    try {
      const response = await this.request().post(`oauth2/logout`, app);
      if (response.status === 200) {
        localStorage.removeItem("vuex");
        localStorage.clear();
        return true;
      }
    } catch (error) {
      return false;
    }
  }
}

export default new Oauth2Service();
