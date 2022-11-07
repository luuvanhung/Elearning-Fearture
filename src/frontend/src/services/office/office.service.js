import BaseService from "../base";

class officeServices extends BaseService {
  get entity() {
    return "office";
  }

  async getAllOffice() {
    const response = await this.request().get(
      `${this.entity}/get_office_trees`
    );
    return response;
  }

  async getOffices() {
    const response = await this.request().get(`${this.entity}/`);
    return response;
  }

  async createOffice(data) {
    const response = await this.request().post(`${this.entity}/`, data);
    return response;
  }

  async deleteOffice(id) {
    const response = this.request().delete(`${this.entity}/${id}`);
    return response;
  }

  async getDetailOffice(id) {
    const response = this.request().get(`${this.entity}/${id}`);
    return response;
  }

  async getLegalType() {
    const response = this.request().get(`${this.entity}/legal_type/get_all`);
    return response;
  }

  async editOffice(data, id) {
    const response = this.request().patch(`${this.entity}/${id}`, data);
    return response;
  }

  async editAllFiledOffice(data, id) {
    const response = this.request().put(`${this.entity}/${id}`, data);
    return response;
  }

  async getOrganizationTree() {
    return await this.request().get(
      `${this.entity}/get_whole_organization_tree`
    );
  }

  async getAll() {
    return await this.request().get(`${this.entity}/get_all`);
  }
}

export default new officeServices();
