import userService from "@/services/user/user";
import officeService from "@/services/office/office.service";
import templateTypeService from "@/services/probation/evaluation_template_type.services";
export default {
  async fetchTitles({ commit }) {
    const title = await userService.getAllRoles();
    commit("SET_TITLES", title.data);
    return title.data;
  },

  async fetchOffices({ commit }) {
    const offices = await officeService.getAll();
    commit("SET_OFFICES", offices.data);
    return offices.data;
  },

  async setEvaluationTemplates({ commit }, template) {
    commit("SET_EVALUATION_TEMPLATES", template.data);
    return template.data;
  },

  async fetchTypes({ commit }) {
    const types = await templateTypeService.getAll();
    commit("SET_TEMPLATE_TYPES", types.data);
    return types.data;
  },
};
