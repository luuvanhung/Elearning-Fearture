import BaseService from "../base";

class AuthenticationService extends BaseService {
  get entity() {
    return "admins";
  }

  async login(data) {
    try {
      const response = await this.request().post(`login`, data);
      return response;
    } catch (error) {
      return false;
    }
  }

  async forgotPassword(data) {
    try {
      const response = await this.request().post(
        `actions/forgot-password`,
        data
      );
      return response;
    } catch (error) {
      return false;
    }
  }
}

export default new AuthenticationService();
