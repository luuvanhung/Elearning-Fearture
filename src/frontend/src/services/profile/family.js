import BaseService from "../base";

class FamilyService extends BaseService {
  get entity() {
    return "family";
  }

  create(id, data) {
    const familyMembers = this.request().post(
      `user/${this.entity}/${id}/add`,
      data
    );
    return familyMembers;
  }

  get(id) {
    const familyMembers = this.request().get(`user/${this.entity}/${id}`);
    return familyMembers;
  }

  update(id, data) {
    return this.request().put(`user/${this.entity}/${id}`, data);
  }

  delete(family_id) {
    return this.request().delete(`user/${this.entity}/${family_id}`);
  }
}

export default new FamilyService();
