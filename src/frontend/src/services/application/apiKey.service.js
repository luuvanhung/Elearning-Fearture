import BaseService from "../base";

class APIKeyService extends BaseService {
  get entity() {
    return "oauth2/api_key";
  }

  async getListAPIKey() {
    const url = this.entity;
    try {
      const response = await this.request().get(url);
      return response.status == 200 ? response.data : null;
    } catch (e) {
      return null;
    }
  }

  async deleteAPIKeyByPrefix(prefix) {
    const url = `${this.entity}/delete-by-prefix`;
    const body = { data: { prefix: prefix } };
    try {
      const response = await this.request().delete(url, body);
      return response.status == 200;
    } catch (e) {
      return false;
    }
  }

  async createAPIKey(data) {
    const url = `${this.entity}`;
    const body = data;
    try {
      const response = await this.request().post(url, body);
      return response.status == 201 ? response.data : null;
    } catch (e) {
      return null;
    }
  }
}

export default new APIKeyService();
