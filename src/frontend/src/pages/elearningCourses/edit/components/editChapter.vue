<template>
  <div>
    <TitleBar
      :title="`Edit chapter: ${currentChapter.title}`"
      v-show="currentChapter"
    />
    <el-card style="color: black">
      <el-form
        ref="formChapter"
        label-position="top"
        label-width="auto"
        size="large"
        :model="chapter"
        :rules="formRules"
        v-loading="chapterLoading"
        @submit.native.prevent="saveChapter(chapter)"
      >
        <el-form-item label="Chapter" prop="title">
          <el-input placeholder="Chapter's title" v-model="chapter.title" />
        </el-form-item>
        <el-form-item label="Prerequisite chapter">
          <el-tooltip
            effect="dark"
            :content="TOOLTIPS.prerequisite_chapter"
            placement="top"
          >
            <el-select
              filterable
              clearable
              remote
              reserve-keyword
              v-model="chapter.previous_chapter"
              value-key="title"
              style="width: 100%"
            >
              <el-option
                v-for="chap in availablePreviousChapters(chapter)"
                :key="chap.id"
                :label="chap.title"
                :value="chap"
              ></el-option>
            </el-select>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="Description" prop="description">
          <el-input type="textarea" :rows="3" v-model="chapter.description" />
        </el-form-item>
        <el-form-item>
          <div style="display: flex; flex-flow: row">
            <el-tooltip
              :disabled="changed"
              effect="light"
              content="Can only click when data change"
              placement="bottom"
              style="margin-right: 10px"
            >
              <div>
                <el-button
                  type="primary"
                  native-type="submit"
                  :disabled="!changed"
                  >Save</el-button
                >
              </div>
            </el-tooltip>
            <el-button @click="$emit('viewEditCourse')">Cancel</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
    <el-divider border-style="double" />
    <TitleBar title="Quiz" />
    <el-container>
      <el-main style="padding: 0px; overflow: unset" v-loading="viewAddQuiz">
        <QuizDetail
          :key="quiz_last_hash"
          :quizCourseId="course_id"
          :quizChapterId="currentChapter.id"
          :currentQuiz="quizzes[quizIndex - 1]"
          :quizIndex="quizIndex"
          @removeQuiz="removeQuiz"
          @changeQuiz="changeQuiz"
        ></QuizDetail>
      </el-main>
      <el-footer class="pagination-quiz my-3">
        <el-pagination
          background
          layout="prev, pager, next"
          :hide-on-single-page="true"
          :current-page="quizIndex"
          :page-size="1"
          @current-change="changePages"
          :total="totalQuizzes"
        ></el-pagination>
        <el-button
          style="height: fit-content"
          icon="el-icon-circle-plus"
          type="primary"
          @click="addQuiz"
        >
          Add Quiz
        </el-button>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
import TitleBar from "@/components/TitleBar.vue";
import QuizDetail from "@/pages/elearningCourses/Quizzes";
import ChapterService from "@/services/e-learning/chapter";
const TOOLTIPS = {
  prerequisite_chapter:
    "Select chapter that must be accomplished before approach current chapter",
};
var hash = require("object-hash");

export default {
  props: {
    currentChapter: Object,
    initialChapters: Array,
  },
  components: {
    TitleBar,
    QuizDetail,
  },
  data() {
    return {
      TOOLTIPS: TOOLTIPS,
      course_id: null,
      formRules: {
        title: [
          {
            required: true,
            message: "Please input title",
            trigger: "blur",
          },
        ],
      },
      chapter: Object.assign({}, this.currentChapter),
      chapters: this.initialChapters,
      chapterLoading: false,
      last_hash: null,
      changed: false,
      quiz_last_hash: null,
      quizzes: [],
      quizIndex: 1,
      viewAddQuiz: false,
    };
  },
  watch: {
    chapter: {
      deep: true,
      handler(newValue, oldValue) {
        const newHash = hash(newValue);
        if (oldValue && newHash != this.last_hash) {
          this.changed = true;
        }
        this.last_hash = newHash;
      },
    },
    currentQuiz: {
      deep: true,
      handler(newValue, oldValue) {
        const newHash = hash(newValue);
        this.quiz_last_hash = newHash;
      },
    },
  },
  created() {
    this.course_id = this.$route.params.id;
    this.quizzes = this.chapter.chapter_quizzes;
  },
  computed: {
    ...mapState("elearning", ["question_types"]),
    totalQuizzes() {
      return this.quizzes.length;
    },
    currentQuiz() {
      return this.totalQuizzes ? this.quizzes[this.quizIndex - 1] : null;
    },
  },
  methods: {
    changeQuiz(quiz) {
      const quizIndex = this.quizzes.findIndex((q) => q.id === quiz.id);
      this.quizzes[quizIndex] = quiz;
    },
    removeQuiz(index) {
      this.quizzes.splice(index - 1, 1);
      this.quizIndex = 1;
      this.viewAdddQuiz = true;
    },
    async addQuiz() {
      this.viewAddQuiz = true;
      const newQuiz = {
        title: "Untitled quiz",
        description: "",
        shuffled: false,
        threshold: 1,
        quiz_questions: [],
      };
      this.quizzes.push(newQuiz);
      this.quizIndex = this.totalQuizzes;
      this.viewAddQuiz = false;
    },
    changePages(page) {
      this.quizIndex = page;
    },
    availablePreviousChapters(currentChapter) {
      let listChapter = [];
      for (const element of this.chapters) {
        if (element.id === currentChapter.id) break;
        listChapter.push({ id: element.id, title: element.title });
      }
      return listChapter;
    },
    async saveChapter(data) {
      this.$refs.formChapter.validate(async (valid, obj) => {
        if (valid) {
          this.chapterLoading = true;
          const response = await ChapterService.update(
            {
              id: data.id,
              course_id: this.course_id,
            },
            {
              title: data.title,
              description: data.description,
              previous_chapter_id: data.previous_chapter
                ? data.previous_chapter.id
                : null,
            }
          );
          this.last_hash = hash(this.chapter);
          this.changed = false;
          this.$emit("viewEditChapter", response.data);
          this.chapterLoading = false;
        }
      });
    },
    async cancel() {
      this.$emit("viewEditCourse");
    },
  },
};
</script>

<style lang="scss" scoped>
.pagination-quiz {
  display: flex;
  justify-content: center;
  flex-direction: row;
}
</style>
