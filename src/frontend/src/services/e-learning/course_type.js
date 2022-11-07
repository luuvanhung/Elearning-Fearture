import BaseService from "../base";

class CourseTypeService extends BaseService {
  get entity() {
    return "course-types";
  }

  // createMultiple(data) {
  //   return this.request().post(
  //     `/elearning/${this.entity}`,
  //     data
  //   );
  // }

  async create(data) {
    try {
      return await this.request().post(`/elearning/${this.entity}`, data);
    } catch (e) {
      return e.response;
    }
  }

  async getAll(params) {
    try {
      const res = await this.request().get(`/elearning/${this.entity}`, {
        params,
      });
      const course_types = res.data;
      return course_types;
    } catch (error) {
      return [];
    }
  }

  // get(id) {
  //   return this.request({ auth: true }).get(`elearning/${this.entity}/${id}`);
  // }

  update(course_type) {
    try {
      return this.request().put(
        `/elearning/${this.entity}/${course_type.get("id")}`,
        course_type,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
    } catch (e) {
      return e.response;
    }
  }

  async delete(id) {
    try {
      return await this.request().delete(`/elearning/${this.entity}/${id}`);
    } catch (e) {
      return false;
    }
  }
}

export default new CourseTypeService();
