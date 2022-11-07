import ApiService from "../ApiService";

class InviteService extends ApiService {
  get entity() {
    return "admins";
  }

  async sendList(data) {
    return this.request().post(`${this.entity}/invite-users`, data);
  }
}

export default new InviteService();
