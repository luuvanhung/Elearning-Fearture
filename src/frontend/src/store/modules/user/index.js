import state from "./userState";
import getters from "./userGetters";
import actions from "./userAction";
import mutations from "./userMutations";

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions,
};
