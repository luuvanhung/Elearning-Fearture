import BaseService from "../base";

class DefinitionService extends BaseService {
  get entity() {
    return "definition";
  }

  createMultiple(data) {
    return this.request().post(
      `/skill/${this.entity}/create_multiple_skill_definition`,
      data
    );
  }

  create(data) {
    return this.request().post(`/skill/${this.entity}`, data);
  }

  getAll(page, page_size) {
    return this.request().get(
      `/skill/${this.entity}?page=${page}&page_size=${page_size}`
    );
  }

  get() {
    return this.request({ auth: true }).get(`/skill/${this.entity}/get_all`);
  }

  update(id, data) {
    return this.request().put(`/skill/${this.entity}/${id}`, data);
  }

  updateSkill(id, data) {
    return this.request().put(`/skill/${id}`, data);
  }

  deleteAll(id) {
    return this.request().delete(
      `/skill/${this.entity}/delete_by_skill_id?skill_id=${id}`
    );
  }

  delete(id) {
    return this.request().delete(`/skill/${this.entity}/${id}`);
  }
}

export default new DefinitionService();
