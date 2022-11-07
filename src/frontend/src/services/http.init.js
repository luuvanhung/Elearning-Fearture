import axios from "axios";
import env from "../../env";
import { refreshToken } from "@/helper/refreshToken";
import { getConfigApp } from "@/helper/getConfigApp";
import { accessToken } from "@/helper/accessToken";
import { storeTokenToVuex } from "@/helper/storeTokenToVuex";

// const Cookie = require("js-cookie");
export default class Http {
  constructor(status) {
    this.handlerEnabled =
      status && status.handlerEnabled ? status.handlerEnabled : false;
    this.instance = axios.create({
      baseURL: env.VUE_APP_API_URL,
    });
    return this.init();
  }

  requestHandler(request) {
    const store = require("@/store");
    const tokenInfo = store ? store.default.getters["scope/tokenInfo"] : null;
    const authenticated = !request.url.startsWith("oauth2/login");
    if (authenticated && tokenInfo) {
      const { access_token } = tokenInfo;
      if (access_token && access_token.length !== 0) {
        request.headers["Authorization"] = `Bearer ${accessToken()}`;
      }
    }
    return request;
  }

  errorHandler(error) {
    if (error?.response?.status === 401) {
      this.renewToken();
    }
    return Promise.reject(error);
  }

  successHandler(response) {
    if (this.handlerEnabled) {
      return response; // TODO: Handle Success Response if need
    }
    return response;
  }

  init() {
    this.instance.interceptors.request.use((request) =>
      this.requestHandler(request)
    );
    this.instance.interceptors.response.use(
      (response) => this.successHandler(response),
      (error) => this.errorHandler(error)
    );
    return this.instance;
  }

  async renewToken() {
    const token = refreshToken();
    if (token) {
      const data = getConfigApp();
      data.append("refresh_token", token);
      try {
        await this.instance
          .post(`oauth2/refresh_token`, data)
          .then((response) => {
            if (response?.status === 200) {
              storeTokenToVuex(
                response.data.access_token,
                response.data.refresh_token
              );
            } else {
              localStorage.removeItem("vuex");
              localStorage.clear();
            }
          });
      } catch (error) {
        return false;
      }
    }
    return false;
  }
}
