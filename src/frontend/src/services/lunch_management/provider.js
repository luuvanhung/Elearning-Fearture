import BaseService from "../base";

class ProviderService extends BaseService {
  get entity() {
    return "provider";
  }

  create(data) {
    const provider = this.request().post(`${this.entity}/`, data);
    return provider;
  }

  get() {
    const providers = this.request().get(`${this.entity}/`);
    return providers;
  }

  update({ data, id }) {
    const providers = this.request().put(`${this.entity}/${id}`, data);
    return providers;
  }

  delete(id) {
    const providers = this.request().delete(`${this.entity}/${id}`);
    return providers;
  }
}

export default new ProviderService();
