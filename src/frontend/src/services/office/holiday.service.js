import BaseService from "../base";

class holidayServices extends BaseService {
  get entity() {
    return "office";
  }

  async get(officeId) {
    const response = await this.request().get(
      `${this.entity}/${officeId}/holidays`
    );
    return response;
  }

  async sync(officeId) {
    const response = await this.request().get(
      `${this.entity}/${officeId}/holidays/sync_data`
    );
    return response;
  }

  async create(officeId, data) {
    const response = await this.request().post(
      `${this.entity}/${officeId}/holidays`,
      data
    );
    return response;
  }

  async update(officeId, id, data) {
    const response = await this.request().put(
      `${this.entity}/${officeId}/holidays/${id}`,
      data
    );
    return response;
  }

  async delete(officeId, id) {
    const response = await this.request().delete(
      `${this.entity}/${officeId}/holidays/${id}`
    );
    return response;
  }
}

export default new holidayServices();
