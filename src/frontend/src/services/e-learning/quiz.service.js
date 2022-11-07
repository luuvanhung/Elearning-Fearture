import ApiService from "@/services/ApiService";

class QuizService extends ApiService {
  get entity() {
    return "elearning/courses";
  }
  // Create quiz for course, chapter, lesson

  getLink(data) {
    data.lesson_id = data.lesson_id == null ? "" : data.lesson_id;
    data.chapter_id = data.chapter_id == null ? "" : data.chapter_id;
    data.course_id = data.course_id == null ? "" : data.course_id;
    let link = "";
    if (data.lesson_id == "" && data.chapter_id == "") {
      link = `${this.entity}/${data.course_id}/quizzes`;
    } else if (data.lesson_id == "") {
      link = `${this.entity}/${data.course_id}/chapters/${data.chapter_id}/quizzes`;
    } else {
      link = `${this.entity}/${data.course_id}/chapters/${data.chapter_id}/lessons/${data.lesson_id}/quizzes`;
    }
    delete data.chapter_id;
    delete data.lesson_id;
    delete data.course_id;
    return {
      link: link,
      data: { ...data },
    };
  }

  async create(data) {
    const obj = this.getLink(data);
    const option = {
      method: "post",
      url: obj.link,
      data: obj.data,
    };
    const response = await this.request(option);
    return response ? response : [];
  }

  async get(data) {
    const obj = this.getLink(data);
    const option = {
      method: "get",
      url: obj.link,
    };
    const response = await this.request(option);
    return response ? response : [];
  }

  async update(data) {
    const obj = this.getLink({
      course_id: data.course_id,
      chapter_id: data.chapter_id,
      lesson_id: data.lesson_id,
    });
    const option = {
      method: "put",
      url: obj.link + `/${data.id}`,
      data: {
        title: data.title,
        description: data.description,
        threshold: data.threshold,
        quiz_questions: data.quiz_questions,
      },
    };
    const response = await this.request(option);
    return response ? response : null;
  }

  async delete(data) {
    const obj = this.getLink({
      course_id: data.course_id,
      chapter_id: data.chapter_id,
      lesson_id: data.lesson_id,
    });
    const option = {
      method: "delete",
      url: obj.link + `/${data.id}`,
    };
    const response = await this.request(option);
    return response ? response : null;
  }
}

export default new QuizService();
