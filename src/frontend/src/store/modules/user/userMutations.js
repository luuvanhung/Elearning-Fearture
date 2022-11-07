export default {
  SET_CURRENT_USER(state, currentUserData) {
    state.currentUser.id = currentUserData.user;
    state.currentUser.email = currentUserData.email;
    state.currentUser.name = currentUserData.name;
    state.currentUser.profile_id = currentUserData.profile_id;
    state.currentUser.is_admin = currentUserData.is_admin;
  },
  CHANGE_AVATAR: (state, imageUrl) => {
    state.currentUser.imageUrl = imageUrl;
  },
  SET_ALL_USERS_LIST: (state, allUsersData) => {
    state.allUsers = allUsersData;
  },
  SET_ALL_EXISTED_ACCOUNTS: (state, allExistedAccounts) => {
    state.allExistedAccounts = allExistedAccounts;
  },
};
