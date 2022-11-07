export default {
  getTokenInfo: ({ commit }, payload) => {
    if (payload) {
      commit("GET_TOKEN_INFO", payload);
    }
  },
  getApplicationScope: ({ commit }, payload) => {
    if (payload) {
      commit("GET_APPLICATION_SCOPE", payload);
    }
  },
  setTokenInfo: ({ commit }, payload) => {
    if (payload) {
      commit("SET_TOKEN_INFO", payload);
    }
  },
  logout: ({ commit }) => {
    commit("LOGOUT");
    localStorage.clear();
  },
};
