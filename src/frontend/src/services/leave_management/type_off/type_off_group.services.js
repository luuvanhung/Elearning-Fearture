import BaseService from "../../base";

export class TypeOffGroupAdminServices extends BaseService {
  get entity() {
    return "workday/admin/group-leave-types";
  }

  getTypeOffGroup() {
    return this.request().get(`${this.entity}`);
  }

  updateOrCreateTypeOffGroup(pk, id, data) {
    if (pk === 0) {
      return this.request().post(`${this.entity}`, data);
    }
    return this.request().put(`${this.entity}/${id}`, data);
  }

  deleteTypeOffGroup(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }
}

export default new TypeOffGroupAdminServices();
