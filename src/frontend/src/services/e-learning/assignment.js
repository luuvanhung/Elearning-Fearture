import ApiService from "@/services/ApiService";

class AssignmentService extends ApiService {
  get entity() {
    return "elearning/assignments";
  }
  async getOrCreateAssignment(id) {
    try {
      const response = await this.request().post(
        `${this.entity}/get_or_create_assignment`,
        id
      );
      const assignment = response.data;
      return assignment;
    } catch (error) {
      return null;
    }
  }
  async getAssignments(params) {
    try {
      const res = await this.request().get(`${this.entity}`, {
        params,
      });
      const assignments = res.data;
      return assignments;
    } catch (error) {
      return [];
    }
  }
  async createNewAssignment(data) {
    const option = {
      method: "post",
      url: this.entity,
      data: data,
    };
    const response = await this.request(option);
    return response ? response : [];
  }
  async delAssignments(id) {
    const option = {
      method: "delete",
      url: `${this.entity}/${id}`,
    };
    const response = await this.request(option);
    return response;
  }

  async editAssignment(id, param) {
    const option = {
      method: "put",
      url: `${this.entity}/${id}`,
      data: param,
    };
    const response = await this.request(option);
    return response ? response : [];
  }

  async getAll(params) {
    try {
      const res = await this.request().get(`${this.entity}`, { params });
      const courses = res.data;
      return courses;
    } catch (error) {
      return [];
    }
  }

  async getDetail(id) {
    try {
      const res = await this.request().get(`elearning/assignments/${id}`);
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

  async getMyAssignments() {
    try {
      const res = await this.request().get(`${this.entity}/get_my_assignments`);
      return res.data;
    } catch (error) {
      return null;
    }
  }

  async editAssignmentChapterLessonAttachment(
    assignmentId,
    assignmentChapterId,
    assignmentChapterLessonId,
    assignmentChapterLessonAttachmentId,
    params
  ) {
    try {
      const res = await this.request().put(
        `${this.entity}/${assignmentId}/chapters/${assignmentChapterId}/lessons/${assignmentChapterLessonId}/attachments/${assignmentChapterLessonAttachmentId}`,
        params
      );
      return res.data;
    } catch (e) {
      return null;
    }
  }

  async getAssignmentChapterLessonAttachment(
    assignmentId,
    assignmentChapterId,
    assignmentChapterLessonId,
    assignmentChapterLessonAttachmentId
  ) {
    try {
      const res = await this.request().get(
        `${this.entity}/${assignmentId}/chapters/${assignmentChapterId}/lessons/${assignmentChapterLessonId}/attachments/${assignmentChapterLessonAttachmentId}`
      );
      return res.data;
    } catch (e) {
      return null;
    }
  }

  async editAssignmentChapterLesson(
    assignmentId,
    assignmentChapterId,
    assignmentChapterLessonId,
    params
  ) {
    try {
      const res = await this.request().put(
        `${this.entity}/${assignmentId}/chapters/${assignmentChapterId}/lessons/${assignmentChapterLessonId}`,
        params
      );
      return res.data;
    } catch (e) {
      return null;
    }
  }

  async submitQuiz(subUrl, data) {
    try {
      const res = await this.request().post(`${this.entity}/${subUrl}`, data);
      return res.data;
    } catch (e) {
      return null;
    }
  }
}
export default new AssignmentService();
