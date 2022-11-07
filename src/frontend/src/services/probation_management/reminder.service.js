import BaseService from "../base";

class ProbationReminderService extends BaseService {
  get entity() {
    return "probation/reminder";
  }

  async create(data, probation_id) {
    return await this.request().post(
      `/${this.entity}/create_reminders?probation_id=${probation_id}`,
      data
    );
  }

  async update(data, probation_id) {
    return await this.request().put(
      `/${this.entity}/update_reminders?probation_id=${probation_id}`,
      data
    );
  }

  async getReminders(probation_id) {
    try {
      return await this.request().get(
        `${this.entity}/get_reminder_detail?probation_id=${probation_id}`
      );
    } catch (e) {
      console.log(e);
    }
  }
}

export default new ProbationReminderService();
