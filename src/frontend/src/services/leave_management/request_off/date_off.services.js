import ApiService from "../../ApiService";

class DateOffService extends ApiService {
  get entity() {
    return "workday/date-off";
  }

  async getDateOffUserEffect() {
    const option = {
      method: "get",
      url: `/${this.entity}/get_date_off_user_effect`,
    };
    const response = await this.request(option);
    if (response) {
      return response.data;
    }
    return [];
  }
}

export default new DateOffService();
