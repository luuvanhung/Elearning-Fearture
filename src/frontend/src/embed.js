import Vue from "vue";
import Embed from "./Embed.vue";
import embedRouter from "./embedRouter";
// import "./plugins/axios";

import ElementUI from "element-ui";
import locale from "element-ui/lib/locale/lang/en";
import "./assets/css/index.css";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import Toast from "vue-toastification";

Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.use(Toast);
library.add(fas);
Vue.config.productionTip = false;
Vue.use(ElementUI, { locale });
new Vue({
  router: embedRouter,
  render: (h) => h(Embed),
}).$mount("#embed");
