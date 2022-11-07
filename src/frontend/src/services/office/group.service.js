import BaseService from "../base";

class groupServices extends BaseService {
  get entity() {
    return "office/group";
  }

  async createGroup(data) {
    const response = await this.request().post(`${this.entity}`, data);
    return response;
  }

  async deleteGroup(id) {
    const response = this.request().delete(`${this.entity}/${id}`);
    return response;
  }

  async editGroup(data, id) {
    const response = this.request().put(`${this.entity}/${id}`, data);
    return response;
  }

  async getAll() {
    const response = this.request().get(`${this.entity}/get_all`);
    return response;
  }
}

export default new groupServices();
