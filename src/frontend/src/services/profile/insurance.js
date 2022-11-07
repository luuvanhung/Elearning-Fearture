import BaseService from "../base";

class InsuranceService extends BaseService {
  get entity() {
    return "insurance";
  }

  create(id, data) {
    const insurance = this.request().post(
      `user/${this.entity}/${id}/add`,
      data
    );
    return insurance;
  }

  get(id) {
    const insurance = this.request().get(`user/${this.entity}/${id}`);
    return insurance;
  }

  update(id, data) {
    const insurance = this.request().put(`user/${this.entity}/${id}`, data);
    return insurance;
  }

  delete(id) {
    return this.request().delete(`user/${this.entity}/${id}`);
  }
}

export default new InsuranceService();
