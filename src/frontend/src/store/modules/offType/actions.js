export default {
  getListTypeOff({ commit }, data) {
    commit("GET_TYPE_OFF", data);
  },

  updateListTypeOff({ commit, rootState }, data) {
    let payLoad = {
      rootState: rootState,
      dataUpdate: data,
    };
    commit("UPDATE_LIST_TYPE_OFF", payLoad);
  },

  deleteListTypeOff({ commit }, data) {
    commit("DELETE_TYPE_OFF", data);
  },
};
