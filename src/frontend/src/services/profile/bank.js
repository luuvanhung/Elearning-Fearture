import BaseService from "../base";

class BankService extends BaseService {
  get entity() {
    return "bank";
  }

  create(id, data) {
    const bank = this.request().post(`user/${this.entity}/${id}/add`, data);
    return bank;
  }

  async get(id) {
    return await this.request().get(`user/${this.entity}/${id}`);
  }

  update(id, data) {
    const bank = this.request().put(`user/${this.entity}/${id}`, data);
    return bank;
  }

  delete(id) {
    return this.request().delete(`user/${this.entity}/${id}`);
  }

  getBankList() {
    const banks = this.request().get(`user/bank_list`);
    return banks;
  }

  addBank(name) {
    const roles = this.request().post(`user/bank_list`, { name: name });
    return roles;
  }

  removeBank(id) {
    return this.request().delete(`user/bank_list/${id}`);
  }
}

export default new BankService();
