import UserService from "@/services/user/user";
export default {
  changeAvatar({ commit }, data) {
    commit("CHANGE_AVATAR", data);
  },
  setCurrentUser: ({ commit }, payload) => {
    if (payload) {
      commit("SET_CURRENT_USER", payload);
    }
  },
  setAllUsersList: ({ commit }) => {
    const UserList = async () => {
      const res = await UserService.getAllEmployees();
      if (res.status === 200) {
        commit("SET_ALL_USERS_LIST", res.data);
      }
    };
    return UserList();
  },
  setAllExistedAccounts: ({ commit }) => {
    const allExistedAccounts = async () => {
      const res = await UserService.getAllExistedAccounts();
      if (res.status === 200) {
        commit("SET_ALL_EXISTED_ACCOUNTS", res.data);
      }
    };
    return allExistedAccounts();
  },
};
