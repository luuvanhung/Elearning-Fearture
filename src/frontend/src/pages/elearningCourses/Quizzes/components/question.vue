<template>
  <div>
    <el-card class="question-card">
      <!-- Question content and Question Type-->
      <el-row :gutter="24">
        <el-col :span="18">
          <el-form
            ref="form"
            :rules="rules"
            :model="question"
            label-width="auto"
            label-position="top"
            size="large"
          >
            <el-form-item prop="content">
              <quill-editor
                :class="is_in_edit_mode ? 'editor-form' : 'view-form'"
                :options="is_in_edit_mode ? null : VIEW_OPTIONS"
                :disabled="!is_in_edit_mode"
                v-model="question.content"
              />
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="6">
          <el-select
            v-if="is_in_edit_mode"
            style="width: 100%"
            reserve-keyword
            v-model="question.type"
            value-key="name"
            placeholder="Select"
          >
            <el-option
              v-for="question_type in question_types"
              :key="question_type.id"
              :label="question_type.name"
              :value="question_type"
            ></el-option>
          </el-select>
        </el-col>
      </el-row>

      <!-- Answers -->
      <el-form
        ref="form"
        :rules="rules"
        :model="correct_answers"
        label-width="auto"
        label-position="top"
        size="large"
        class="question-card__answers"
      >
        <!-- For Multiple Choice Question -->
        <el-form-item
          prop="multiple_choices"
          v-if="isMultipleChoiceQuestion(question.type.name)"
        >
          <el-checkbox-group
            class="answer-wrapper"
            v-model="correct_answers.multiple_choices"
            :disabled="current_quiz.is_passed"
          >
            <el-checkbox
              v-for="(answer, index) in question.question_answers"
              :key="answer.id"
              :label="answer.content"
            >
              <span style="display: flex">
                <input
                  :disabled="!is_in_edit_mode"
                  class="question-card__answer"
                  type="text"
                  placeholder="Question without title"
                  v-model="answer.content"
                />
                <el-tooltip
                  v-if="is_in_edit_mode"
                  class="item remove-btn"
                  effect="light"
                  :content="tooltips.add_answer"
                  placement="top"
                >
                  <i
                    class="el-icon-circle-plus-outline add-anwser-btn"
                    @click="addAnswer(index)"
                  />
                </el-tooltip>
                <el-tooltip
                  v-if="is_in_edit_mode"
                  class="item remove-btn"
                  effect="light"
                  content="Remove this answer"
                  placement="right"
                >
                  <i
                    class="el-icon-close add-anwser-btn"
                    @click="removeAnswer(index)"
                  />
                </el-tooltip>
              </span>
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <!-- For Single Choice Question -->
        <el-form-item
          prop="single_choices"
          v-if="isSingleChoiceQuestion(question.type.name)"
        >
          <el-radio-group
            class="answer-wrapper"
            v-model="correct_answers.single_choices"
            :disabled="current_quiz.is_passed"
          >
            <el-radio
              v-for="(answer, index) in question.question_answers"
              :key="answer.id"
              :label="answer.content"
            >
              <span style="display: flex">
                <input
                  :disabled="!is_in_edit_mode"
                  class="question-card__answer"
                  type="text"
                  placeholder="Question without title"
                  v-model="answer.content"
                />
                <el-tooltip
                  v-if="is_in_edit_mode"
                  effect="light"
                  :content="tooltips.add_answer"
                  class="item remove-btn"
                  placement="top"
                >
                  <i
                    class="el-icon-circle-plus-outline add-anwser-btn"
                    @click="addAnswer(index)"
                  />
                </el-tooltip>
                <el-tooltip
                  v-if="is_in_edit_mode"
                  class="item remove-btn"
                  effect="light"
                  content="Remove this answer"
                  placement="right"
                >
                  <i
                    class="el-icon-close add-anwser-btn"
                    @click="removeAnswer(index)"
                  />
                </el-tooltip>
              </span>
            </el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div class="break-line mb-4"></div>
      <!-- Operators -->
      <div class="question-card__operators">
        <!-- Question's score -->
        <div class="question-card__operators--points">
          <i class="el-icon-s-claim"></i>
          <!-- For Editing -->
          <el-tooltip
            v-if="is_in_edit_mode"
            class="for-editing"
            effect="light"
            :content="tooltips.question_score"
            placement="bottom"
          >
            <el-input-number
              v-model="question.score"
              :min="1"
              :max="100"
              label="Score"
              :step="1"
              size="medium"
            ></el-input-number>
          </el-tooltip>
          <!-- For viewing -->
          <el-tooltip
            :class="{ 'for-viewing': is_in_edit_mode }"
            effect="light"
            content="This question's score"
            placement="bottom"
          >
            <span class="question-score">{{ question.score }}</span>
          </el-tooltip>
        </div>
        <div v-if="is_in_edit_mode" class="question-card__operators--others">
          <el-tooltip
            effect="light"
            :content="tooltips.add_question"
            placement="bottom"
          >
            <i
              class="el-icon-circle-plus-outline"
              @click="addQuestion(questionIndex)"
            ></i>
          </el-tooltip>
          <el-tooltip
            effect="light"
            :content="tooltips.copy_question"
            placement="bottom"
          >
            <i
              class="el-icon-document-copy"
              @click="copyQuestion(questionIndex)"
            ></i>
          </el-tooltip>
          <el-tooltip
            effect="light"
            :content="tooltips.remove_question"
            placement="bottom"
          >
            <i
              class="el-icon-delete"
              @click="removeQuestion(questionIndex)"
            ></i>
          </el-tooltip>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { TOOLTIPS } from "@/const/quiz";
import { VIEW_OPTIONS } from "@/const/quillEditorModules.js";

import _ from "lodash";

export default {
  props: ["current_quiz", "current_question", "questionIndex", "question_id"],
  data() {
    return {
      VIEW_OPTIONS: VIEW_OPTIONS,
      question: JSON.parse(JSON.stringify(this.current_question)),
      correct_answers: {
        multiple_choices: [],
        single_choices: "",
      },
      tooltips: TOOLTIPS,
      value: true,
      question_type: "",
      rules: {
        multiple_choices: [
          {
            type: "array",
            required: true,
            trigger: "change",
            message: "Set at least one True answer",
          },
        ],
        resource: [
          {
            required: true,
            message: "Set True answer",
            trigger: "change",
          },
        ],
      },
    };
  },
  computed: {
    ...mapState("elearning", ["question_types"]),
    is_in_edit_mode() {
      return this.$route.fullPath.split("/").slice(-1).join("") === "edit";
    },
    question_submitting_data() {
      let question_submitting_data = {
        question_id: this.question_id,
        quiz_result_detail_answers: [],
      };
      if (!this.is_in_edit_mode) {
        this.current_question.question_answers.forEach((answer) => {
          question_submitting_data.quiz_result_detail_answers.push({
            answer_id: answer.id,
            chosen: this.correct_answers.multiple_choices.includes(
              answer.content
            ),
          });
        });
      }
      return question_submitting_data;
    },
  },
  mounted() {
    this.getCorrectAnswers();
    if (!this.is_in_edit_mode && !this.current_quiz.is_passed) {
      this.correct_answers.multiple_choices = [];
      this.correct_answers.single_choices = "";
    }
  },
  methods: {
    isMultipleChoiceQuestion(type) {
      return type.toLowerCase().includes("multiple");
    },
    isSingleChoiceQuestion(type) {
      return type.toLowerCase().includes("single");
    },
    getCorrectAnswers() {
      if (this.isMultipleChoiceQuestion(this.question.type.name)) {
        this.question.question_answers.forEach((answer) => {
          if (answer.is_correct)
            this.correct_answers.multiple_choices.push(answer.content);
        });
      } else if (this.isSingleChoiceQuestion(this.question.type.name)) {
        this.question.question_answers.forEach((answer) => {
          if (answer.is_correct)
            this.correct_answers.single_choices = answer.content;
        });
      }
    },
    addAnswer(index) {
      this.question.question_answers.splice(index + 1, 0, {
        content: `Answer ${this.question.question_answers.length + 1}`,
        is_correct: false,
      });
    },
    removeAnswer(index) {
      if (this.question.question_answers.length > 1) {
        if (this.isMultipleChoiceQuestion(this.question.type.name)) {
          this.correct_answers.multiple_choices.splice(
            this.correct_answers.multiple_choices.indexOf(
              this.question.question_answers[index].content
            ),
            1
          );
        } else if (this.isSingleChoiceQuestion(this.question.type.name)) {
          if (
            this.question.question_answers[index].content ===
            this.correct_answers.single_choices
          ) {
            this.correct_answers.single_choices = "";
          }
        }
        this.question.question_answers.splice(index, 1);
      }
    },
    removeQuestion(index) {
      if (this.current_quiz.quiz_questions.length > 1) {
        this.$emit("deleteQuestionInCurrentQuiz", index);
      }
    },
    copyQuestion(index) {
      const oldQuestion = _.omit(this.question, "id");
      let copyQuestion = JSON.parse(JSON.stringify(oldQuestion));
      copyQuestion.question_answers.map((answer) => {
        delete answer.id;
      });
      this.$emit("insertQuestionToCurrentQuiz", index, copyQuestion);
    },
    addQuestion(index) {
      const newQuestion = {
        content: "New question",
        order: index,
        score: 1,
        type: this.question_types[0],
        question_answers: [
          {
            content: "New answer",
            is_correct: false,
          },
        ],
      };
      this.$emit("insertQuestionToCurrentQuiz", index, newQuestion);
    },
  },
  watch: {
    "correct_answers.multiple_choices": {
      handler() {
        this.question.question_answers.forEach((answer) => {
          answer.is_correct = this.correct_answers.multiple_choices.includes(
            answer.content
          );
        });
      },
      deep: true,
    },
    question: {
      deep: true,
      handler(newValue, oldValue) {
        this.$emit("updateCurrentQuestion", newValue);
        if (oldValue) {
          this.$emit("updateQuizSubmittingData", this.question_submitting_data);
        }
      },
    },
    question_type: {
      handler(newVal, oldVal) {
        if (oldVal) {
          this.correct_answers.multiple_choices = [];
          this.correct_answers.single_choices = "";
        }
      },
    },
    "correct_answers.single_choices"() {
      if (this.correct_answers.single_choices) {
        this.correct_answers.multiple_choices.splice(
          0,
          1,
          this.correct_answers.single_choices
        );
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.question-card {
  width: 100%;
  transition: all 0.2s ease-in-out;
  border-radius: 12px;
  padding: 12px 20px;
  margin: 10px 0px;
  overflow: unset;
  :deep(.question-card__question) {
    width: 100%;
    height: fit-content;
    border: none !important;
  }
  .remove-btn,
  .for-editing,
  .el-select {
    display: none;
  }
  .for-viewing {
    display: block;
    font-size: 20px;
  }

  &:focus-within {
    border-left: solid 8px #f7a9c4;
    .for-editing,
    .el-select {
      display: inline-block;
    }
    .for-viewing {
      display: none;
    }
    &__operators--others {
      display: flex;
    }
    &__answers {
      width: 100%;
      .remove-btn {
        margin: auto;
        display: block;
      }
    }
  }

  input {
    width: 100%;
    border: none;
    line-height: 36px;
    height: 36px;
    font-family: inherit;

    &:focus-visible {
      border-bottom: 1px solid rgba(0, 0, 0, 0.24);
      transition: all 0.4s ease-in-out;
      outline: none;
    }
  }

  .break-line {
    height: 1px;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.24);
  }

  .question-type {
    line-height: 36px;
    height: 36px;
    font-size: 12pt;
    text-align: center;
  }

  .answer-wrapper {
    align-items: center;
    width: 100%;
    .el-checkbox {
      width: inherit;
      height: 40px;
      :deep(.el-checkbox__label) {
        width: 100%;
        input {
          width: 100%;
        }
      }
    }
  }

  &__question {
    font-size: 12pt;
    line-height: 24px;
    color: #202124;
    font-weight: 400;
    padding: 16px 0;
  }

  &__answers > div {
    font-size: 11pt;
    line-height: 15pt;
    color: #202124;
    font-weight: 400;
    padding: 16px 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
    .el-radio {
      display: flex;
      width: inherit;
      height: 40px;
      :deep(.el-radio__input) {
        margin: auto;
      }
      :deep(.el-radio__label) {
        width: 100%;
        input {
          width: 100%;
        }
      }
    }
    .remove-btn {
      float: right;
      cursor: pointer;
      font-size: 20px;
      color: #5f6368;
      margin: auto;
    }

    .add-anwser-btn {
      cursor: pointer;
      font-size: 20px;
      color: #5f6368;
      padding: 0;
    }
  }

  &__operators {
    display: flex;
    align-items: center;
    justify-content: space-between;

    &--points {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;

      input {
        font-size: 18px;
      }
      i {
        font-size: 20px;
      }
    }

    &--others {
      font-size: 20px;
      gap: 10px;
      color: #5f6368;
      cursor: pointer;
      display: none;
    }
  }

  &:focus-within &__operators--others {
    display: flex;
  }

  &:focus-within &__answers {
    .remove-btn {
      display: block;
    }
  }
}
@import "@/assets/scss/main.scss";
</style>
