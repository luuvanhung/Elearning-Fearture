const state = {
  isCollapse: false,
  navCollapse: false,
};

const getters = {
  value: (state) => {
    return state.isCollapse;
  },
};

const mutations = {
  changeValue(state) {
    state.isCollapse = !state.isCollapse;
  },
};

const actions = {
  changeValue: ({ commit }) => {
    commit("changeValue");
  },
};

export default {
  state,
  mutations,
  getters,
  actions,
};
