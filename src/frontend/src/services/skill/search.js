import BaseService from "../base";

class SearchService extends BaseService {
  get entity() {
    return "search";
  }

  getAll(page, page_size, data) {
    return this.request({ auth: true }).get(
      `/skill/vote/${this.entity}?page=${page}&page-size=${page_size}&${data}`
    );
  }
}

export default new SearchService();
