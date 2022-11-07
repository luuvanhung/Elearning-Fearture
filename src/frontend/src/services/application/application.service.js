import BaseService from "../base";

class Application extends BaseService {
  get entity() {
    return "oauth2/applications";
  }

  async getListApp(page, pageSize) {
    try {
      const res = await this.request().get(
        `${this.entity}?page=${page}&page_size=${pageSize}`
      );
      return res;
    } catch (e) {
      return false;
    }
  }

  async getOneApp(id) {
    try {
      const res = await this.request().get(`${this.entity}/${id}`);
      return res;
    } catch (e) {
      return false;
    }
  }

  async addNewApp(data) {
    try {
      const res = await this.request().post(`${this.entity}`, data);
      return res;
    } catch (e) {
      return false;
    }
  }

  async editApp(id, data) {
    try {
      const res = await this.request().put(`${this.entity}/${id}`, data);
      return res;
    } catch (e) {
      return false;
    }
  }

  async deleteApp(id) {
    try {
      const res = await this.request().delete(`${this.entity}/${id}`);
      return res;
    } catch (e) {
      return false;
    }
  }
  getApplicationScopes(client_id) {
    try {
      return this.request({ auth: true }).get(
        `${this.entity}/${client_id}/retrieve_application_scopes`
      );
    } catch (e) {
      console.log(e);
    }
  }
}

export default new Application();
