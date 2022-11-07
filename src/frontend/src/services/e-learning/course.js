import ApiService from "@/services/ApiService";

class CourseService extends ApiService {
  get entity() {
    return "elearning/courses";
  }

  async create(data) {
    const option = {
      method: "post",
      url: this.entity,
      data: data,
    };
    const response = await this.request(option);
    return response ? response : [];
  }

  async getAll(params) {
    try {
      const res = await this.request().get(`${this.entity}`, {
        params,
      });
      const courses = res.data;
      return courses;
    } catch (error) {
      return [];
    }
  }

  async search(params) {
    try {
      const res = await this.request().get(`${this.entity}`, {
        params,
      });
      const courses = res.data;
      return courses;
    } catch (error) {
      return [];
    }
  }

  async update(course) {
    const option = {
      method: "put",
      url: `${this.entity}/${course.get("id")}`,
      data: course,
    };
    const response = await this.request(option);
    return response ? response : [];
  }

  async delete(id) {
    const option = {
      method: "delete",
      url: `${this.entity}/${id}`,
    };
    const response = await this.request(option);
    return response;
  }

  async getDetail(id) {
    try {
      const res = await this.request().get(`${this.entity}/${id}`);
      return res.data;
    } catch (error) {
      return null;
    }
  }

  async getUserExclude(id) {
    try {
      const res = await this.request().get(
        `${this.entity}/${id}/get_exclude_users_assignment`
      );
      return res.data;
    } catch (error) {
      return null;
    }
  }

  async getAssignedUsers(id) {
    try {
      const res = await this.request().get(`${this.entity}/${id}/get_users`);
      return res.data;
    } catch (error) {
      return null;
    }
  }

  async getCourseAssignment(id) {
    try {
      const res = await this.request().get(
        `${this.entity}/${id}/get_assignment`
      );
      return res.data;
    } catch (error) {
      return null;
    }
  }

  async getAssignedCourses() {
    try {
      const res = await this.request().get(
        `${this.entity}/get_assigned_course`
      );
      return res.data;
    } catch (error) {
      return null;
    }
  }
}

export default new CourseService();
