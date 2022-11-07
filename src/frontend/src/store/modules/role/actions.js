import RoleService from "@/services/role/role_service";

export default {
  async getRoleList({ commit }, payload) {
    commit(
      "GET_ROLE_LIST",
      await RoleService.getRoles(payload.page_size, payload.page, payload.name)
    );
  },
};
