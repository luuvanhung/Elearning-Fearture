import BaseService from "../base";

class officeSessionService extends BaseService {
  get entity() {
    return "session";
  }

  createMultiple(data) {
    return this.request().post(`/${this.entity}/create_multiple`, data);
  }

  create(data) {
    return this.request().post(`/${this.entity}/`, data);
  }

  getAll(office_id) {
    return this.request().get(
      `/${this.entity}/get_by_office_id?office_id=${office_id}`
    );
  }

  async getSessionTimesByProfile() {
    const res = await this.request().get(`/${this.entity}/get_by_profile`);
    const sessions = res.data;
    if (sessions) {
      return sessions;
    } else return [];
  }

  update(id, data) {
    return this.request().put(`/${this.entity}/${id}`, data);
  }

  deleteById(id) {
    return this.request().delete(`/${this.entity}/${id}`);
  }

  deleteByDay(dow) {
    return this.request().delete(`/${this.entity}/delete_by_dow?dow=${dow}`);
  }
}

export default new officeSessionService();
