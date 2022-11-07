import BaseService from "../../base";

class BonusTypeService extends BaseService {
  get entity() {
    return "workday/bonus-type";
  }

  get() {
    const res = this.request().get(`${this.entity}`);
    return res;
  }

  create_or_update(data) {
    const res = this.request().post(`${this.entity}/create_or_update`, data);
    return res;
  }

  delete(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }
}

export default new BonusTypeService();
