import BaseService from "../base";

class ContactService extends BaseService {
  get entity() {
    return "contact";
  }

  create(id, data) {
    const contact = this.request().post(`user/${this.entity}/${id}/add`, data);
    return contact;
  }

  get(id) {
    const contact = this.request().get(`user/${this.entity}/${id}`);
    return contact;
  }

  update(id, data) {
    const contact = this.request().put(`user/${this.entity}/${id}`, data);
    return contact;
  }

  delete(id) {
    return this.request().delete(`user/${this.entity}/${id}`);
  }
}

export default new ContactService();
