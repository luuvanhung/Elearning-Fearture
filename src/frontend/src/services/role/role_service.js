import ApiService from "../ApiService";

export class RoleService extends ApiService {
  get entity() {
    return "user/role";
  }

  async getRole(id) {
    const options = {
      method: "get",
      url: `${this.entity}/${id}`,
    };
    const response = await this.request(options);
    return response || [];
  }

  async getRoles(page_size, page, name) {
    const options = {
      method: "get",
      url: `${this.entity}`,
      params: {
        page_size: page_size,
        page: page,
        name: name,
      },
    };
    const response = await this.request(options);
    return response || [];
  }

  async createRole(role) {
    const options = {
      method: "post",
      url: `${this.entity}`,
      data: {
        name: role.name,
        description: role.description,
        scope: role.scope,
      },
    };

    const response = this.request(options);
    return response || [];
  }

  async updateRole(role) {
    const options = {
      method: "put",
      url: `${this.entity}/${role.id}`,
      data: {
        name: role.name,
        description: role.description,
        scope: role.scope,
        id: role.id,
      },
    };

    const response = this.request(options);
    return response || [];
  }

  async deleteRole(role_id) {
    const options = {
      method: "delete",
      url: `${this.entity}/${role_id}`,
    };
    const response = await this.request(options);
    return response || [];
  }
}

export default new RoleService();
