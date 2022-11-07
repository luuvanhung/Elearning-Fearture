import BaseService from "../base";

class SquadServices extends BaseService {
  get entity() {
    return "office/squad";
  }

  async createDepartment(data) {
    return this.request().post(`${this.entity}`, data);
  }

  async deleteDepartment(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }

  async editDepartment(data, id) {
    return this.request().put(`${this.entity}/${id}`, data);
  }

  async getAll() {
    return this.request().get(`${this.entity}/get_all`);
  }

  async importSquads(data) {
    return this.request().post(`${this.entity}/import-squads`, data);
  }
}

export default new SquadServices();
