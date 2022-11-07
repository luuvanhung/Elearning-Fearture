import ApiService from "@/services/ApiService";

class LessonService extends ApiService {
  get entity() {
    return "elearning/courses";
  }

  async create(router) {
    const option = {
      method: "post",
      url: `${this.entity}/${router.course_id}/chapters/${router.chapter_id}/lessons`,
    };
    const response = await this.request(option);
    return response ? response : null;
  }
  async get(router) {
    try {
      return await this.request().get(
        `${this.entity}/${router.course_id}/chapters/${router.chapter_id}/lessons/${router.id}`
      );
    } catch (e) {
      return e.response;
    }
  }

  async update(router, data) {
    const option = {
      method: "put",
      url: `${this.entity}/${router.course_id}/chapters/${router.chapter_id}/lessons/${router.id}`,
      data: data,
    };
    const response = await this.request(option);
    return response ? response : null;
  }

  async delete(router) {
    const option = {
      method: "delete",
      url: `${this.entity}/${router.course_id}/chapters/${router.chapter_id}/lessons/${router.id}`,
    };
    const response = await this.request(option);
    return response;
  }
}

export default new LessonService();
