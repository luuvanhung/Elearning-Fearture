import BaseService from "../base";

class ReportService extends BaseService {
  get entity() {
    return "report";
  }

  getAll() {
    return this.request().get(`/skill/vote/${this.entity}`);
  }
}

export default new ReportService();
