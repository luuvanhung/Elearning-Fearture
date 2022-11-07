import BaseService from "../base";

class EventService extends BaseService {
  get entity() {
    return "event";
  }

  create(data) {
    const event = this.request().post(`/${this.entity}/`, data);
    return event;
  }

  getUsers(month) {
    const users = this.request().get(`/${this.entity}/users`, {
      params: { month: month },
    });
    return users;
  }

  getEvents() {
    const events = this.request().get(`/${this.entity}`);
    return events;
  }

  cancelEvent(id) {
    const response = this.request().delete(`/${this.entity}/${id}`);
    return response;
  }

  update(id, data) {
    const response = this.request().put(`/${this.entity}/${id}`, data);
    return response;
  }

  //   delete(id) {
  //     const lunch = this.request().delete(`/${this.entity}/action/${id}`)
  //     return lunch
  //   }
}

export default new EventService();
