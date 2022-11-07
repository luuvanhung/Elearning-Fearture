export default {
  isAdmin: (state) => state.currentUser.role === 1,
  allUsers: (state) => state.allUsers,
  allUsersExcludeCurrentUser: (state) =>
    state.allUsers.filter((user) => user.id !== state.currentUser.id),
  allExistedAccounts: (state) => state.allExistedAccounts,
};
