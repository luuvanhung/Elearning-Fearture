import BaseService from "../base";

export class CalendarAdminServices extends BaseService {
  get entity() {
    return "workday/calendar/admin";
  }

  handleData(data) {
    return data.map((item) => {
      return {
        id: item.id,
        start: item.date,
        end: item.date,
        title: item.request_off.leave_type.name,
        typeOff: item.request_off.leave_type.name,
        name: item.name,
        email: item.email,
        reason: item.request_off.reason,
        lunch: item.lunch ? "Yes" : "No",
        type: item.request_off.leave_type.leave_type_group,
        timeType: item.type,
        color: "",
        detail: [],
      };
    });
  }

  async getCalendar() {
    try {
      return this.request()
        .get(`${this.entity}`)
        .then((res) => this.handleData(res.data));
    } catch (e) {
      console.log(e);
    }
  }
}

export default new CalendarAdminServices();
