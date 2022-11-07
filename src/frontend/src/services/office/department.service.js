import BaseService from "../base";

class departmentServices extends BaseService {
  get entity() {
    return "office/department";
  }

  async createDepartment(data) {
    const response = await this.request().post(`${this.entity}`, data);
    return response;
  }

  async deleteDepartment(id) {
    const response = this.request().delete(`${this.entity}/${id}`);
    return response;
  }

  async editDepartment(data, id) {
    const response = this.request().put(`${this.entity}/${id}`, data);
    return response;
  }

  async getAll() {
    return await this.request().get(`${this.entity}/get_all`);
  }

  async importDepartments(data) {
    return this.request().post(`${this.entity}/import-departments`, data);
  }
}

export default new departmentServices();
