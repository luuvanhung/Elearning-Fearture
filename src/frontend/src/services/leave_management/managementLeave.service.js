import ApiService from "../ApiService";
import { ACTION } from "@/const/actions";

class ManagementLeaveService extends ApiService {
  get entity() {
    return "workday/request";
  }

  async getManagementRequestOff(
    page = 1,
    pageSize = 12,
    year = "",
    month = "",
    day = "",
    status = "",
    search = ""
  ) {
    const option = {
      method: "get",
      url: `/${this.entity}/management/get_request_detail_by_user`,
      params: {
        year: year,
        month: month,
        day: day,
        status: status,
        search: search,
        page: page,
        page_size: pageSize,
      },
    };
    const response = this.request(option);
    if (response) {
      return response;
    }
    return [];
  }

  async searchManageRequestOff(data) {
    const option = {
      method: "get",
      url: `/${this.entity}/management/search_request_detail`,
      params: data,
    };
    const response = this.request(option);
    if (response) {
      return response;
    }
    return [];
  }

  async actionRequest(data) {
    const { action } = data;

    let url = "";

    if (action === ACTION.delete) {
      url = "management/multi";
    } else {
      url = "management";
    }

    const option = {
      method: "post",
      url: `/${this.entity}/${url}`,
      data: data,
    };

    return this.request(option, true);
  }

  async countRequest() {
    const option = {
      method: "get",
      url: `/${this.entity}/management/count`,
    };

    const response = this.request(option);
    if (response && response.status === 200 && response.data) {
      return response.data;
    }
    return 0;
  }
}

export default new ManagementLeaveService();
