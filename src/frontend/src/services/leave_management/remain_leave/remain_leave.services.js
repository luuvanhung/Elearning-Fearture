import BaseService from "../../base";

class RemainLeaveService extends BaseService {
  get entity() {
    return "workday/remain-leave";
  }

  async getRemainLeaves() {
    const res = await this.request().get(`/${this.entity}`);
    return res;
  }

  async getRemainLeaveUser(id) {
    const res = await this.request().get(`/${this.entity}/remain_leave_user`, {
      params: {
        id: id,
      },
    });
    return res;
  }

  async create(data) {
    const res = await this.request().post(
      `/${this.entity}/create_remain_leave`,
      data
    );
    return res;
  }

  async update(id, data) {
    const res = await this.request().put(`/${this.entity}/${id}`, data);
    return res;
  }

  async destroy(id) {
    const res = await this.request().delete(`/${this.entity}/${id}`);
    return res;
  }

  async getRetrieveDate() {
    const remainDay = await this.request().get(`/${this.entity}/retrieve_date`);
    return remainDay;
  }
}

export default new RemainLeaveService();
