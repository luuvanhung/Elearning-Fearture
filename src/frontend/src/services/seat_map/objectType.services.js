import BaseService from "../base";

class ObjectTypeService extends BaseService {
  get entity() {
    return "object-type";
  }

  create(data) {
    return this.request().post(`/seat-map/${this.entity}`, data);
  }

  getAll() {
    return this.request().get(`/seat-map/${this.entity}/get_all`);
  }
}

export default new ObjectTypeService();
