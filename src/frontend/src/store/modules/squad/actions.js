import SquadService from "../../../services/office/squad.service";
import DepartmentService from "../../../services/office/department.service";

export default {
  async getListSquad({ commit }) {
    const response = await SquadService.getAll();
    commit("GET_LIST_SQUAD", response.data);
  },
  async getListDepartment({ commit }) {
    const response = await DepartmentService.getAll();
    commit("GET_LIST_DEPARTMENT", response.data);
  },
};
