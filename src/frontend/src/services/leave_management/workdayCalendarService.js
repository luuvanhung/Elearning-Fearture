import BaseService from "../base";

class WorkdayCalendarService extends BaseService {
  get entity() {
    return "workday/calendar";
  }

  async syncData(dateSync) {
    try {
      const body = {
        time_start: dateSync[0],
        time_end: dateSync[1],
      };
      return await this.request().post(`${this.entity}/sync_data`, body);
    } catch (e) {
      console.log(e);
    }
  }
}

export default new WorkdayCalendarService();
