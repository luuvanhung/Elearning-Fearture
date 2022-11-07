export default {
  SET_COURSES: (state, courses) => {
    state.courses = courses;
  },
  SET_TOPICS: (state, topics) => {
    state.topics = topics;
  },
  ADD_TOPIC: (state, topic) => {
    state.topics.splice(0, 0, topic);
  },
  UPDATE_TOPIC: (state, updatedTopic) => {
    const index = state.topics.findIndex(
      (topic) => topic.id == updatedTopic.id
    );
    state.topics.splice(index, 1, updatedTopic);
  },
  DELETE_TOPIC: (state, topic_id) => {
    const index = state.topics.findIndex((topic) => topic.id == topic_id);
    state.topics.splice(index, 1);
  },
  SET_COURSE_TYPES: (state, course_types) => {
    state.course_types = course_types;
  },
  SET_CURRENT_COURSE: (state, course) => {
    state.currentCourse = course;
  },
  SET_CURRENT_QUIZ(state, quiz) {
    state.current_quiz = quiz;
  },
  SET_QUESTION_TYPES(state, question_types) {
    state.question_types = question_types;
  },
  INSERT_QUESTION_TO_CURRENT_QUIZ(state, { index, question }) {
    state.current_quiz.questions.splice(index + 1, 0, question);
  },
  ADD_QUESTION_TO_CURRENT_QUIZ(state, question) {
    state.current_quiz.questions.push(question);
  },
  REMOVE_QUESTION_FROM_CURRENT_QUIZ(state, id) {
    state.current_quiz.questions = state.current_quiz.questions.filter(
      (question) => question.id !== id
    );
  },
};
