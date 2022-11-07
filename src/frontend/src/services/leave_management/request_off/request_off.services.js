import ApiService from "../../ApiService";
class RequestOffService extends ApiService {
  get entity() {
    return "workday/request-off";
  }

  async create(data) {
    return this.request({
      method: "post",
      url: `/${this.entity}`,
      data: data,
    });
  }

  async searchRequest(data) {
    const option = {
      method: "get",
      url: `/${this.entity}/search`,
      params: data,
    };
    return this.request(option);
  }

  async getAllRequest(page, page_size) {
    const option = {
      method: "get",
      url: `/${this.entity}`,
      params: {
        page: page,
        page_size: page_size,
      },
    };
    const response = await this.request(option);
    if (response) {
      return response.data;
    }
    return [];
  }

  async getMyRequest(
    page = 1,
    page_size = 8,
    year = "",
    month = "",
    day = "",
    status = ""
  ) {
    const option = {
      method: "get",
      url: `/${this.entity}/list_request_user`,
      params: {
        year: year,
        month: month,
        day: day,
        status: status,
        page: page,
        page_size: page_size,
      },
    };
    const response = await this.request(option);
    if (response) {
      return response.data;
    }
    return [];
  }

  async update({ data, id }) {
    return this.request({
      method: "put",
      url: `/${this.entity}/${id}`,
      data: data,
    });
  }

  async delete(id) {
    return this.request({
      method: "delete",
      url: `/${this.entity}/${id}`,
    });
  }

  async countTotalTypeOffDays(profile, typeOff, year) {
    const option = {
      method: "get",
      url: `/${this.entity}/total_off_by_types`,
      params: {
        profile: profile,
        leave_type: typeOff,
        year: year,
      },
    };
    const response = await this.request(option);
    if (response) {
      return response.data;
    }
    return 0;
  }
}

export default new RequestOffService();
