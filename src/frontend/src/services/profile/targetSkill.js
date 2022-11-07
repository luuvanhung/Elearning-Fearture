import BaseService from "../base";

class TargetSkillService extends BaseService {
  get entity() {
    return "target";
  }

  create(data) {
    return this.request().post(`/skill/${this.entity}`, data);
  }

  get(id) {
    return this.request().get(
      `/skill/${this.entity}/get_by_target_user?user_id=${id}`
    );
  }

  update(id, data) {
    return this.request().put(`/skill/${this.entity}/${id}`, data);
  }

  delete(id) {
    return this.request().delete(`/skill/${this.entity}/${id}`);
  }
}

export default new TargetSkillService();
