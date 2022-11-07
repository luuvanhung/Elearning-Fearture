import BaseService from "../base";

class ObjectService extends BaseService {
  get entity() {
    return "object";
  }

  create(data) {
    return this.request().post(`/seat-map/${this.entity}`, data);
  }

  getAll(data) {
    return this.request().get(`/seat-map/${this.entity}/get_all`, data);
  }

  update(data) {
    return this.request().put(`/seat-map/${this.entity}/${data.id}`, data);
  }

  delete(id) {
    return this.request().delete(`/seat-map/${this.entity}/${id}`);
  }
}

export default new ObjectService();
