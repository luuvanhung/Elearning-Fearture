import BaseService from "../base";

class LunchScheduleService extends BaseService {
  get entity() {
    return "lunches";
  }

  async create(data) {
    const lunch = await this.request().post(`/${this.entity}/`, data);
    return lunch;
  }

  async get(params) {
    try {
      const res = await this.request().get(`/${this.entity}/`, { params });
      return res.data;
    } catch {
      return null;
    }
  }

  async update({ data, id }) {
    const lunch = await this.request().put(`/${this.entity}/${id}`, data);
    return lunch;
  }

  async delete(id) {
    const lunch = await this.request().delete(`/${this.entity}/${id}`);
    return lunch;
  }
}

export default new LunchScheduleService();
