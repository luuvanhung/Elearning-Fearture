import ApiService from "@/services/ApiService";

class QuizQuestionService extends ApiService {
  get entity() {
    return "elearning/questions";
  }

  async getQuestionTypes() {
    const option = {
      method: "get",
      url: `${this.entity}/retrieve_quiz_types`,
    };
    const response = this.request(option);
    return response ? response : [];
  }
}

export default new QuizQuestionService();
