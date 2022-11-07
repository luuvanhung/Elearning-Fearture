import BaseService from "../base";

class LevelService extends BaseService {
  get entity() {
    return "level";
  }

  create(data) {
    return this.request().post(`/skill/${this.entity}`, data);
  }

  getAll() {
    return this.request().get(`/skill/${this.entity}`);
  }

  update(id, data) {
    return this.request().put(`/skill/${this.entity}/${id}`, data);
  }

  delete(id) {
    return this.request().delete(`/skill/${this.entity}/${id}`);
  }
}

export default new LevelService();
