import BaseService from "../base";

class IdentityService extends BaseService {
  get entity() {
    return "identity";
  }

  create(id, data) {
    return this.request().post(`user/${this.entity}/${id}/add`, data);
  }

  get(id) {
    return this.request().get(`user/${this.entity}/${id}`);
  }

  update(id, data) {
    return this.request().put(`user/${this.entity}/${id}`, data);
  }

  delete(id) {
    return this.request().delete(`user/${this.entity}/${id}`);
  }
}

export default new IdentityService();
