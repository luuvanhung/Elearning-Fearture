import Http from "./http.init";
import Vue from "vue";

export default class ApiService {
  constructor() {
    if (!this.entity) {
      throw new Error("Child service class not provide entity");
    }
  }

  request(data, isLoading = false) {
    const status = { handlerEnabled: true };
    const http = new Http(status);
    if (!data) {
      return http;
    }
    const option = {
      method: data.method,
      url: data.url,
      data: data.data,
      params: data.params,
    };
    const loading = isLoading
      ? Vue.prototype.$loading({
          lock: true,
          text: "Loading",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        })
      : null;
    return http(option)
      .then((response) => {
        if (response.data.message) {
          Vue.$toast.success(response.data.message);
        }
        return response;
      })
      .catch((error) => {
        error.response.data.error
          ? Vue.$toast.error(error.response.data.error)
          : Vue.$toast.error("An error occurred");

        return false;
      })
      .finally(() => {
        if (isLoading) {
          loading.close();
        }
      });
  }
}
