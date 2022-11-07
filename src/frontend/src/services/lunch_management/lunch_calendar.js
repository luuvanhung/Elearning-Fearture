import BaseService from "../base";

class LunchService extends BaseService {
  get entity() {
    return "lunch";
  }

  create(data) {
    const lunch = this.request().post(`/${this.entity}/create`, data);
    return lunch;
  }

  createMany(data) {
    const lunch = this.request().post(`/${this.entity}/list`, data);
    return lunch;
  }

  get() {
    const lunches = this.request().get(`/${this.entity}/list`);
    return lunches;
  }

  update({ data, id }) {
    const lunch = this.request().put(`/${this.entity}/action/${id}`, data);
    return lunch;
  }

  delete(id) {
    const lunch = this.request().delete(`/${this.entity}/action/${id}`);
    return lunch;
  }
}

export default new LunchService();
