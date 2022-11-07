import BaseService from "../base";

class LessonService extends BaseService {
  get entity() {
    return "elearning/lessons";
  }
  async create(requestData) {
    try {
      const response = await this.request().post(`${this.entity}`, {
        chapter: requestData.chapter,
        title: requestData.title,
        content: requestData.content,
        index: requestData.index,
      });
      return response;
    } catch (error) {
      return null;
    }
  }
  async update(requestData) {
    try {
      const response = await this.request().put(
        `${this.entity}/${requestData.id}`,
        {
          status: requestData.status,
          due: requestData.due.split("T")[0] + "T00:00:00",
        }
      );
      return response;
    } catch (error) {
      return error.response.data.due;
    }
  }
  async delete(requestData) {
    try {
      const response = await this.request().delete(
        `${this.entity}/${requestData.id}`
      );
      return response;
    } catch (error) {
      return error.response;
    }
  }
}

export default new LessonService();
