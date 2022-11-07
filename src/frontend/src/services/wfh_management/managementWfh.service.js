import BaseService from "../base";

class ManagementWFHService extends BaseService {
  get entity() {
    return "wfh/request";
  }

  async getManagementRequestWFH(
    page = 1,
    pageSize = 12,
    year = "",
    month = "",
    day = "",
    status = "",
    search = ""
  ) {
    try {
      const request = this.request().get(
        `/${this.entity}/management/get_request_detail`,
        {
          params: {
            year: year,
            month: month,
            day: day,
            status: status,
            search: search,
            page: page,
            page_size: pageSize,
          },
        }
      );
      return request;
    } catch (error) {
      return [];
    }
  }

  async countRequest() {
    try {
      let response = this.request().get(`/${this.entity}/management/count`);
      if (response && response.status === 200 && response.data) {
        return response.data;
      }
      return 0;
    } catch (error) {
      return 0;
    }
  }
}

export default ManagementWFHService();
