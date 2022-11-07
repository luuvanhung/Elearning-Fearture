import BaseService from "../base";

class StatisticDateOffService extends BaseService {
  get entity() {
    return "workday/statistic";
  }

  getByUser(year) {
    const res = this.request().get(`${this.entity}/user?y=${year}`);
    return res;
  }

  getMyTeam(params) {
    try {
      const res = this.request().get(`${this.entity}/team`, { params });
      return res;
    } catch {
      return null;
    }
  }

  getByAdmin(params) {
    try {
      const res = this.request().get(`${this.entity}/office`, { params });
      return res;
    } catch {
      return null;
    }
  }
}

export default new StatisticDateOffService();
