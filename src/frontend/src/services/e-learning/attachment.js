import ApiService from "@/services/ApiService";
class AttachmentsService extends ApiService {
  get entity() {
    return "elearning/courses";
  }
  async get(router) {
    try {
      return await this.request().get(
        `${this.entity}/${router.course_id}/chapters/${router.chapter_id}/lessons/${router.lesson_id}/attachments/${router.id}`
      );
    } catch (e) {
      return null;
    }
  }

  async create(router, data) {
    const option = {
      method: "post",
      url: `${this.entity}/${router.course_id}/chapters/${router.chapter_id}/lessons/${router.lesson_id}/attachments`,
      data: data,
    };
    const response = await this.request(option);
    return response ? response : null;
  }

  async update(router, data) {
    const option = {
      method: "put",
      url: `${this.entity}/${router.course_id}/chapters/${router.chapter_id}/lessons/${router.lesson_id}/attachments/${router.id}`,
      data: data,
    };
    const response = await this.request(option);
    return response ? response : null;
  }

  async delete(router) {
    const option = {
      method: "delete",
      url: `${this.entity}/${router.course_id}/chapters/${router.chapter_id}/lessons/${router.lesson_id}/attachments/${router.id}`,
    };
    const response = await this.request(option);
    return response;
  }
}

export default new AttachmentsService();
