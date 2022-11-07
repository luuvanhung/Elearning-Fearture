import BaseService from "../base";

class GetUserService extends BaseService {
  get entity() {
    return "user";
  }

  get(page_size, page, active = 1) {
    const res = this.request().get(
      `${this.entity}/?page_size=${page_size}&page=${page}&active=${active}`
    );
    return res;
  }

  getCurrentUser(id) {
    try {
      const res = this.request().get(`${this.entity}/${id}`);
      return res;
    } catch (e) {
      console.log(e);
    }
  }

  // Return List User have "name" in name
  searchUserByNameOrEmail(name, page, page_size, active = 1) {
    try {
      const res = this.request().get(
        `${this.entity}/search?page_size=${page_size}&page=${page}&name_or_email=${name}&active=${active}`
      );
      return res;
    } catch (e) {
      return [];
    }
  }

  updateUserRole(userId, roles) {
    try {
      return this.request().put(`${this.entity}/${userId}`, {
        roles: roles,
      });
    } catch (e) {
      console.log(e);
    }
  }

  updateGeneralProfile(data) {
    return this.request({ auth: true }).put(
      `${this.entity}/profile/${data.id}`,
      data
    );
  }

  getAllTitles() {
    return this.request({ auth: true }).get(`${this.entity}/title`);
  }

  getLineManager(id) {
    return this.request({ auth: true }).get(
      `${this.entity}/get_line_manager?id=${id}`
    );
  }

  getUserIncludeLineManagerName(userId) {
    return this.request({ auth: true }).get(
      `${this.entity}/get_users_include_line_manager?user_id=${userId}`
    );
  }
}

export default new GetUserService();
