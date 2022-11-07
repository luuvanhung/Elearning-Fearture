export default {
  GET_ROLE_LIST: (state, payload) => {
    state.roleList.rows = payload.data.results;
    state.roleList.totalPage = payload.data.page_number;
    state.roleList.currentPage = payload.data.current;
    state.roleList.count = payload.data.count;
    state.roleList.page_size = payload.data.page_size;
  },
};
