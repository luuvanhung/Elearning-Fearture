<template>
  <div
    class="quiz-container flex flex-column"
    v-if="current_quiz && current_quiz.quiz_questions"
  >
    <!-- IN EDIT MODE -->
    <el-card class="box-card title-card">
      <el-form
        v-loading="loading"
        ref="editForm"
        :model="current_quiz"
        :rules="rules"
        @submit.native.prevent="updateQuiz"
      >
        <!-- Title card -->
        <el-form-item prop="title">
          <textarea
            class="box-card__title"
            :disabled="!is_in_edit_mode"
            type="textarea"
            placeholder="Quiz's title"
            v-model="current_quiz.title"
          />
        </el-form-item>
        <el-row :gutter="30">
          <el-col :span="18">
            <input
              text
              :disabled="!is_in_edit_mode"
              class="box-card__subtitle"
              type="text"
              placeholder="Quiz's description"
              v-model="current_quiz.description"
            />
          </el-col>
          <el-col :span="6" style="text-align: right">
            <!-- For editing -->
            <el-tooltip
              v-if="is_in_edit_mode"
              class="item for-editing"
              effect="light"
              :content="tooltips.quiz_threshold"
              placement="top"
            >
              <el-input-number
                v-model="current_quiz.threshold"
                :min="0"
                :max="1"
                label="Threshold"
                :step="0.1"
                size="large"
                controls-position="right"
              ></el-input-number>
            </el-tooltip>
            <!-- For viewing -->
            <div :class="{ 'for-viewing': is_in_edit_mode }">
              <el-tooltip
                effect="light"
                :content="tooltips.quiz_threshold"
                placement="top"
              >
                <span class="quiz-threshold">{{
                  `${current_quiz.threshold * 100}%`
                }}</span>
              </el-tooltip>
            </div>
            <el-form-item style="font-size: 20px">
              <el-tooltip
                effect="light"
                style="margin-right: 10px"
                :content="tooltips.add_question"
                placement="bottom"
              >
                <el-button
                  icon="el-icon-circle-plus-outline"
                  type="text"
                  class="add-question-btn"
                  @click="addQuestion"
                  style="font-size: 20px"
                ></el-button>
              </el-tooltip>
              <el-tooltip
                effect="light"
                style="margin-right: 10px"
                :content="tooltips.save_quiz"
                placement="bottom"
              >
                <el-button
                  icon="el-icon-check"
                  type="text"
                  native-type="submit"
                  style="font-size: 20px"
                ></el-button>
              </el-tooltip>
              <el-popconfirm
                confirm-button-text="Delete"
                cancel-button-text="No"
                title="Delete this quiz?"
                @confirm="deleteQuiz"
              >
                <template slot="reference">
                  <el-tooltip
                    effect="light"
                    style="margin-right: 10px"
                    :content="tooltips.delete_quiz"
                    placement="bottom"
                  >
                    <el-button
                      icon="el-icon-delete"
                      type="text"
                      size="large"
                      style="font-size: 20px"
                    ></el-button>
                  </el-tooltip>
                </template>
              </el-popconfirm>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    <question
      v-for="(question, index) in current_quiz.quiz_questions"
      class="box-card"
      :key="question.id"
      :question_id="question.id"
      :current_question="question"
      :questionIndex="index"
      :current_quiz="current_quiz"
      @updateCurrentQuestion="updateCurrentQuestion"
      @insertQuestionToCurrentQuiz="insertQuestionToCurrentQuiz"
      @deleteQuestionInCurrentQuiz="deleteQuestionInCurrentQuiz"
    ></question>
  </div>
</template>

<script>
import { TOOLTIPS } from "@/const/quiz";
import { mapState } from "vuex";
import QuizService from "@/services/e-learning/quiz.service";
import question from "@/pages/elearningCourses/Quizzes/components/question.vue";

export default {
  components: {
    question,
  },
  props: {
    quizLessonId: {
      type: String,
      default: null,
    },
    quizChapterId: {
      type: String,
      default: null,
    },
    quizCourseId: {
      type: String,
      default: null,
    },
    currentQuiz: Object,
    quizIndex: Number,
  },
  data() {
    return {
      quiz_id: "",
      loading: false,
      viewQuizz: false,
      tooltips: TOOLTIPS,
      rules: {
        title: [
          {
            required: true,
            message: "Please input title",
            trigger: "blur",
          },
        ],
        description: [
          {
            required: true,
            message: "Please input description",
            trigger: "blur",
          },
        ],
      },
      current_quiz: Object.assign({}, this.currentQuiz),
    };
  },
  watch: {
    current_quiz: {
      deep: true,
      handler(newValue, oldValue) {
        this.$emit("changeQuiz", newValue);
      },
    },
  },
  computed: {
    ...mapState("elearning", ["question_types"]),
    is_in_edit_mode() {
      return this.$route.fullPath.split("/").slice(-1).join("") === "edit";
    },
  },
  methods: {
    updateCurrentQuestion(question) {
      const questionIndex = this.current_quiz.quiz_questions.findIndex(
        (q) => q.order === question.order
      );
      this.current_quiz.quiz_questions[questionIndex] = question;
    },
    addQuestion() {
      const length = this.current_quiz.quiz_questions.length;
      let index = length;
      const newQuestion = {
        content: "New question",
        score: 0,
        order: index + 1,
        type: this.question_types[0],
        question_answers: [
          {
            content: "New answer",
            is_correct: false,
          },
        ],
      };
      this.insertQuestionToCurrentQuiz(index, newQuestion);
    },
    deleteQuestionInCurrentQuiz(index) {
      this.current_quiz.quiz_questions.splice(index, 1);
      for (let i = 0; i < this.current_quiz.quiz_questions.length; i++) {
        this.current_quiz.quiz_questions[i].order = i + 1;
      }
    },
    insertQuestionToCurrentQuiz(index, newQuestion) {
      this.current_quiz.quiz_questions.splice(index + 1, 0, newQuestion);
      for (let i = 0; i < this.current_quiz.quiz_questions.length; i++) {
        this.current_quiz.quiz_questions[i].order = i + 1;
      }
    },
    async updateQuiz() {
      this.$refs.editForm.validate(async (valid, obj) => {
        if (valid) {
          if (!this.current_quiz.quiz_questions.length) {
            this.$toast.warning("This quiz does not have any answer");
            return;
          }
          for (const question of this.current_quiz.quiz_questions) {
            let questionValid = false;
            for (const answer of question.question_answers) {
              if (answer.is_correct) {
                questionValid = true;
                break;
              }
            }
            if (!questionValid) {
              this.$toast.warning(
                `Question ${question.order} must have at least one correct answer!`
              );
              return;
            }
          }
          this.loading = true;
          let response = null;
          if (this.current_quiz.id) {
            response = await QuizService.update({
              ...this.current_quiz,
              id: this.current_quiz.id,
              course_id: this.quizCourseId,
              chapter_id: this.quizChapterId,
              lesson_id: this.quizLessonId,
            });
          } else {
            response = await QuizService.create({
              ...this.current_quiz,
              course_id: this.quizCourseId,
              chapter_id: this.quizChapterId,
              lesson_id: this.quizLessonId,
            });
          }
          if (response) {
            this.current_quiz = response.data;
            this.$emit("changeQuiz", this.current_quiz);
          }
          this.loading = false;
        }
      });
    },
    async deleteQuiz() {
      this.loading = true;
      if (this.current_quiz.id) {
        await QuizService.delete({
          course_id: this.quizCourseId,
          chapter_id: this.quizChapterId,
          lesson_id: this.quizLessonId,
          id: this.current_quiz.id,
        });
      }
      this.$emit("removeQuiz", this.quizIndex);
      this.loading = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.quiz-container {
  transition: all ease-in-out 0.4s;
}
.box-card {
  width: 100%;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
  :deep(.box-card__title) {
    width: 100%;
    height: fit-content;
    border: none !important;
  }
  &.title-card {
    padding: 12px;

    &:focus-within {
      border-left: solid 8px #f7a9c4;
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
      outline: none;
    }
  }

  &__title {
    font-size: 24pt;
    color: #202124;
    padding-bottom: 8px;
  }
  &__subtitle {
    font-size: 11pt;
    line-height: 15pt;
    color: #202124;
  }
  .break-line {
    height: 0.5px;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.24);
  }

  .for-editing {
    display: none;
  }
  .for-viewing {
    text-align: center;
  }

  &:focus-within {
    .for-editing {
      display: block;
    }
    .for-viewing {
      display: none;
    }
  }
  .quiz-threshold {
    display: inline-block;
    text-align: center;
    height: 20px;
    line-height: 20px;
    margin-left: 8px;
    font-size: 20px;
  }
}
.add-question-btn {
  cursor: pointer;
}
</style>
