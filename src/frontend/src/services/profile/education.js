import BaseService from "../base";

class EducationService extends BaseService {
  get entity() {
    return "education";
  }

  create(id, data) {
    const education = this.request().post(
      `user/${this.entity}/${id}/add`,
      data
    );
    return education;
  }

  get(id) {
    const education = this.request().get(`user/${this.entity}/${id}`);
    return education;
  }

  update(id, data) {
    return this.request().put(`user/${this.entity}/${id}`, data);
  }

  delete(id, data) {
    return this.request({ auth: true }).delete(
      `/user/${this.entity}/${id}`,
      data
    );
  }
}

export default new EducationService();
