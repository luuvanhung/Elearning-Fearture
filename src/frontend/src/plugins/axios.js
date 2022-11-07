import Vue from "vue";

import axios from "axios";
import env from "../../env";

axios.defaults.baseURL = env.VUE_APP_API_URL
  ? `${env.VUE_APP_API_URL}`
  : "/api/v1";
Vue.use(axios);
