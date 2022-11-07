export default {
  getListTypeOffGroup({ commit }, data) {
    commit("GET_TYPE_OFF_GROUP", data);
  },

  updateListTypeOffGroup({ commit }, data) {
    commit("UPDATE_TYPE_OFF_GROUP", data);
  },

  deleteListTypeOffGroup({ commit }, data) {
    commit("DELETE_TYPE_OFF_GROUP", data);
  },
};
