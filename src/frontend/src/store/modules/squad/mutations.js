export default {
  GET_LIST_SQUAD: (state, payload) => {
    state.listSquads = payload;
  },
  GET_LIST_DEPARTMENT: (state, payload) => {
    state.listDepartments = payload;
  },
};
