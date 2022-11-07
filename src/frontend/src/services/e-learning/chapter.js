import ApiService from "@/services/ApiService";
import Vue from "vue";

class ChapterService extends ApiService {
  get entity() {
    return "elearning/courses";
  }
  async create(data) {
    const option = {
      method: "post",
      url: `${this.entity}/${data.course_id}/chapters`,
      data: data,
    };
    const response = await this.request(option);
    return response ? response : [];
  }

  // async getAll(params) {
  //   try {
  //     const res = await this.request().get(
  //       `${this.entity}/`, { params }
  //     );
  //     const courses = res.data;
  //     return courses
  //   } catch (error) {
  //     return [];
  //   }
  // }

  async update(router, data) {
    const option = {
      method: "put",
      url: `${this.entity}/${router.course_id}/chapters/${router.id}`,
      data: data,
    };
    const response = await this.request(option);
    return response ? response : [];
  }

  async delete(data) {
    const option = {
      method: "delete",
      url: `${this.entity}/${data.course_id}/chapters/${data.id}`,
    };
    const response = await this.request(option);
    return response;
  }
}

export default new ChapterService();
