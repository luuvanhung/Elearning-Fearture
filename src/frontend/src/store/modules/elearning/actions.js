import CourseService from "@/services/e-learning/course";
import LessonService from "@/services/e-learning/lesson";
import TopicService from "@/services/e-learning/topic";
import CourseTypeService from "@/services/e-learning/course_type";
import QuizService from "@/services/e-learning/quiz.service.js";
import QuizQuestionService from "@/services/e-learning/quizQuestion.service.js";

export default {
  async fetchCourses({ commit }, params) {
    const courses = await CourseService.getAll(params);
    commit("SET_COURSES", courses.results);
    return courses;
  },
  async fetchTopics({ commit }, params) {
    const topics = await TopicService.getAll(params);
    commit("SET_TOPICS", topics);
    return topics;
  },
  async fetchCourseTypes({ commit }, params) {
    const types = await CourseTypeService.getAll(params);
    commit("SET_COURSE_TYPES", types.results);
    return types;
  },

  async fetchCurrentQuiz({ commit }, id) {
    const result = await QuizService.get(id);
    commit("SET_CURRENT_QUIZ", result);
    return result;
  },

  async fetchCurrentCourse({ commit }, id) {
    const currentCourse = await CourseService.getDetail(id);
    commit("SET_CURRENT_COURSE", currentCourse);
    return currentCourse;
  },

  async fetchCurrentLesson({ commit }, id) {
    const currentLesson = await LessonService.getDetail(id);
    return currentLesson;
  },

  async fetchQuestionTypes({ commit }) {
    const response = await QuizQuestionService.getQuestionTypes();
    commit("SET_QUESTION_TYPES", response.data);
    return response;
  },

  async addCourse({ commit }, course) {
    course = await CourseService.create(course);
    return course;
  },

  async addTopic({ commit }, topic) {
    const response = await TopicService.create(topic);
    if (response) {
      commit("ADD_TOPIC", response.data);
    }
    return response;
  },

  async addCourseType({ commit }, course_type) {
    course_type = await CourseTypeService.create(course_type);
    return course_type;
  },

  async deleteCourse({ commit }, course_id) {
    let response = await CourseService.delete(course_id);
    return response;
  },

  async deleteTopic({ commit }, topic_id) {
    const response = await TopicService.delete(topic_id);
    commit("DELETE_TOPIC", topic_id);
    return response;
  },

  async deleteCourseType({ commit }, course_type_id) {
    let response = await CourseTypeService.delete(course_type_id);
    return response;
  },

  async updateCourse({ commit }, course) {
    course = await CourseService.update(course);
    return course;
  },

  async updateTopic({ commit }, topic) {
    const response = await TopicService.update(topic);
    if (response) {
      commit("UPDATE_TOPIC", response.data);
    }
    return response;
  },

  async updateCourseType({ commit }, course_type) {
    course_type = await CourseTypeService.update(course_type);
    return course_type;
  },
};
