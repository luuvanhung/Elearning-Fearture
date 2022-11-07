const QUESTION_TYPES = {
  for_selecting: [
    {
      value: "SINGLE_CHOICE",
      label: "Single Choice",
    },
    {
      value: "MULTIPLE_CHOICE",
      label: "Multiple Choice",
    },
  ],
  for_displaying: {
    SINGLE_CHOICE: "Single Choice",
    MULTIPLE_CHOICE: "Multiple Choice",
  },
};

const TOOLTIPS = {
  quiz_threshold: "Passing percentage",
  question_score: "This Questions's Score",
  save_quiz: "Save quiz",
  delete_quiz: "delete quiz",
  add_answer: "Add answer below",
  add_question: "Add question below",
  remove_answer: "Remove this answer",
  save_question: "Save this question",
  remove_question: "Remove this question",
  copy_question: "Make a copy from this question",
  "single choice": "Select only one correct answer",
  "multiple choice": "Select one or many correct answers",
  set_right_anwser: "Select to set this answer true",
};

export { QUESTION_TYPES, TOOLTIPS };
