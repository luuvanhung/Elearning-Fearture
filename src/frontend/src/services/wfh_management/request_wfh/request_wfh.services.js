import BaseService from "../../base";

class RequestWfhService extends BaseService {
  get entity() {
    return "wfh/wfh-request";
  }

  async search(name_or_email, fromDate, toDate, page, page_size) {
    try {
      const response = await this.request().get(`${this.entity}/search`, {
        params: {
          name_or_email: name_or_email,
          from_date: fromDate,
          to_date: toDate,
          page: page,
          page_size: page_size,
        },
      });
      return response;
    } catch (error) {
      return [];
    }
  }

  async create(data) {
    const wfhRequest = await this.request().post(`/${this.entity}`, data);
    return wfhRequest;
  }

  async getAllRequest(page, page_size) {
    try {
      const res = await this.request().get(
        `/${this.entity}?page=${page}&page_size=${page_size}`
      );
      const wfhRequests = res.data;
      return wfhRequests;
    } catch (error) {
      return [];
    }
  }

  async getMyWfhRequest(page, page_size) {
    try {
      const res = await this.request().get(
        `/${this.entity}/list_request_user`,
        {
          params: {
            page: page,
            page_size: page_size,
          },
        }
      );
      const wfhRequests = res.data;
      return wfhRequests;
    } catch (error) {
      return [];
    }
  }

  async update({ data, id }) {
    const wfhRequest = await this.request().put(`/${this.entity}/${id}`, data);
    return wfhRequest;
  }

  async delete(id) {
    const wfhRequest = await this.request().delete(`/${this.entity}/${id}`);
    return wfhRequest;
  }

  async countTotalTypeOffDays(profile, typeOff, year) {
    const res = await this.request().get(
      `/${this.entity}/total_off_by_types?profile=${profile}&leave_type=${typeOff}&year=${year}`
    );
    const totalTypeOffLeaves = res.data;
    if (totalTypeOffLeaves) return totalTypeOffLeaves;
    else return 0;
  }
}

export default new RequestWfhService();
