import TeamService from "../../../services/team/team.services";

export default {
  async getListTeam({ commit }) {
    const response = await TeamService.getAll();
    commit("GET_LIST_TEAM", response.data);
  },
};
