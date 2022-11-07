import BaseService from "../base";

class positionSkillServices extends BaseService {
  get entity() {
    return "skill";
  }

  async getPositionSkill() {
    const response = this.request().get(`${this.entity}/title`);
    return response;
  }

  async createPositionSkill(data) {
    const response = this.request().post(`${this.entity}/title`, data);
    return response;
  }

  async updatePositionSkill(id, data) {
    return this.request().put(`${this.entity}/title/${id}`, data);
  }

  async deletePositionSkill(id) {
    const response = this.request().delete(`${this.entity}/title/${id}`);
    return response;
  }
}

export default new positionSkillServices();
