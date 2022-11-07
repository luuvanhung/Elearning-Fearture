<template>
  <div>
    <TitleBar
      :title="`Edit lesson: ${currentLesson.title}`"
      v-show="currentLesson"
    ></TitleBar>
    <el-card style="color: black; overflow: unset">
      <el-form
        :key="lesson.id"
        ref="formLesson"
        label-position="top"
        label-width="auto"
        size="large"
        :model="lesson"
        :rules="formRules"
        @submit.native.prevent="save()"
        v-loading="lessonLoading"
      >
        <el-form-item label="Lesson" prop="title">
          <el-input
            placeholder="Lesson's title"
            v-model="lesson.title"
          ></el-input>
        </el-form-item>
        <el-form-item label="Prerequisite lesson">
          <el-tooltip
            effect="dark"
            :content="TOOLTIPS.prerequisite_lesson"
            placement="top"
          >
            <el-select
              filterable
              clearable
              remote
              reserve-keyword
              v-model="lesson.previous_lesson"
              value-key="title"
              style="width: 100%"
            >
              <el-option
                v-for="lesson in lessonsInCurrentChapter"
                :key="lesson.id"
                :label="lesson.title"
                :value="lesson"
              ></el-option>
            </el-select>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="Content">
          <quill-editor v-model="lesson.content" />
        </el-form-item>
        <el-form-item label="Attachments">
          <el-scrollbar always :key="lesson.attachments.length">
            <div style="display: flex">
              <span
                v-for="item in lesson.attachments"
                :key="item.id"
                class="scrollbar-demo-item"
              >
                <el-card :body-style="{ padding: '0px' }">
                  <div style="padding: 14px">
                    <el-row>
                      <el-col>
                        <img
                          :src="
                            require(`@/static/images/mime_type-${getImageType(
                              item.mine_type
                            )}.svg`)
                          "
                          class="filter icon"
                          alt="word"
                        />
                        <span>
                          <a :href="item.file" target="_blank">{{
                            item.original_name
                          }}</a>
                        </span>
                      </el-col>
                    </el-row>
                    <el-row>
                      <span>{{ formatBytes(item.length) }}</span>
                      <div style="float: right">
                        <el-tooltip
                          effect="light"
                          content="Must read"
                          class="for-editing"
                          placement="bottom"
                        >
                          <el-switch
                            v-model="item.forced_read"
                            class="ml-2"
                            style="
                              --el-switch-on-color: #13ce66;
                              --el-switch-off-color: #ff4949;
                            "
                            @change="changeForcedRead(item)"
                          />
                        </el-tooltip>
                        <el-popover
                          ref="popover"
                          title="Embed Url"
                          :width="400"
                          trigger="click"
                        >
                          <template #reference>
                            <el-tooltip
                              effect="light"
                              content="Get attachment's embed url"
                              class="for-editing"
                              placement="bottom"
                            >
                              <el-button
                                type="text"
                                size="medium"
                                @click="embingUrl(item)"
                              >
                                <font-awesome-icon :icon="['fas', 'code']" />
                              </el-button>
                            </el-tooltip>
                          </template>
                          <template #default>
                            <el-input
                              :autosize="{ minRows: 2, maxRows: 4 }"
                              v-model="embedUrl"
                            >
                              <template #append>
                                <el-button
                                  icon="el-icon-paperclip"
                                  @click="copyToClipboard"
                                ></el-button>
                              </template>
                            </el-input>
                          </template>
                        </el-popover>
                        <el-popconfirm
                          confirm-button-text="Remove"
                          cancel-button-text="Cancel"
                          title="Remove this file?"
                          @confirm="deleteFile(item.id)"
                        >
                          <template slot="reference">
                            <el-button
                              type="text"
                              size="large"
                              icon="el-icon-delete"
                            ></el-button>
                          </template>
                        </el-popconfirm>
                      </div>
                    </el-row>
                  </div>
                </el-card>
              </span>
            </div>
          </el-scrollbar>
          <el-upload
            class="upload-demo"
            style="padding-top: 10px"
            :limit="20"
            :file-list="filesList"
            :on-success="handleSuccess"
            :accept="ACCEPTEDTYPES"
            drag
            action
          >
            <el-icon class="el-icon-upload">
              <upload-filled />
            </el-icon>
            <div class="el-upload__text">
              Drop file here or
              <em>click to upload</em>
            </div>
          </el-upload>
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
            <el-button @click="cancel">Cancel</el-button>
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
          :quizLessonId="lesson.id"
          :currentQuiz="currentQuiz"
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
import { MIMETYPES, ACCEPTEDTYPES } from "@/const/MimeTypes";
import { formatBytes } from "@/utils/convertBytes";
import AttachmentsService from "@/services/e-learning/attachment";
import LessonService from "@/services/e-learning/lesson";
import TitleBar from "@/components/TitleBar.vue";
import QuizDetail from "@/pages/elearningCourses/Quizzes";
const TOOLTIPS = {
  prerequisite_lesson:
    "Select lesson that must be accomplished before approach current lesson",
};

var hash = require("object-hash");

export default {
  props: ["currentLesson", "currentChapter"],
  components: {
    TitleBar,
    QuizDetail,
  },
  data() {
    return {
      TOOLTIPS: TOOLTIPS,
      ACCEPTEDTYPES: ACCEPTEDTYPES,
      lesson: Object.assign({}, this.currentLesson),
      course_id: null,
      courseHash: null,
      filesList: [],
      lessonLoading: false,
      embedUrl: null,
      formRules: {
        title: [
          {
            required: true,
            message: "Please input title",
            trigger: "blur",
          },
        ],
      },
      changed: false,
      last_hash: null,
      quiz_last_hash: null,
      quizzes: [],
      quizIndex: 1,
      viewAddQuiz: false,
    };
  },
  watch: {
    lesson: {
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
  async created() {
    this.last_hash = hash(this.lesson);
    this.course_id = this.$route.params.id;
    this.quizzes = this.lesson.lesson_quizzes;
  },
  computed: {
    ...mapState("elearning", ["question_types"]),
    totalQuizzes() {
      return this.quizzes.length;
    },
    currentQuiz() {
      return this.totalQuizzes ? this.quizzes[this.quizIndex - 1] : null;
    },
    lessonsInCurrentChapter() {
      let lessons = [];
      for (const lesson of this.currentChapter.lessons) {
        if (lesson.id === this.currentLesson.id) break;
        lessons.push({ id: lesson.id, title: lesson.title });
      }
      return lessons;
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
      const newQuiz = {
        title: "Untitled quiz",
        description: "",
        shuffled: false,
        threshold: 1,
        quiz_questions: [
          {
            content: "New question",
            score: 0,
            order: 1,
            type: this.question_types[0],
            question_answers: [
              {
                content: "New answer",
                is_correct: true,
              },
            ],
          },
        ],
      };
      this.quizzes.push(newQuiz);
      this.quizIndex = this.totalQuizzes;
      this.viewAddQuiz = false;
    },
    changePages(page) {
      this.quizIndex = page;
    },
    formatBytes,
    async changeForcedRead(item) {
      const response = await AttachmentsService.update(
        {
          course_id: this.course_id,
          chapter_id: this.lesson.chapter,
          lesson_id: this.lesson.id,
          id: item.id,
        },
        {
          mine_type: item.mine_type,
          original_name: item.original_name,
          forced_read: item.forced_read,
        }
      );
    },
    getImageType(mimeType) {
      let image = "unknown";
      if (MIMETYPES.videos.indexOf(mimeType) >= 0) image = "video";
      else if (MIMETYPES.words.indexOf(mimeType) >= 0) image = "word";
      else if (MIMETYPES.pdfs.indexOf(mimeType) >= 0) image = "pdf";
      else if (MIMETYPES.powerpoints.indexOf(mimeType) >= 0) image = "ppt";
      return image;
    },
    async handleSuccess(res, file) {
      const formData = new FormData();
      formData.append("file", file.raw);
      formData.append("mine_type", file.raw.type);
      formData.append("chapter", this.lesson.chapter);
      formData.append("lesson", this.lesson.id);
      formData.append("length", file.raw.size);
      const response = await AttachmentsService.create(
        {
          course_id: this.course_id,
          chapter_id: this.lesson.chapter,
          lesson_id: this.lesson.id,
        },
        formData
      );
      if (response.data) {
        this.lesson.attachments.push(response.data);
        this.filesList = [];
      }
    },
    download(src) {
      window.open(src, "Download");
    },
    embingUrl(item) {
      this.embedUrl = `${window.location.origin}/embed/${item.id}`;
    },
    async deleteFile(id) {
      const response = await AttachmentsService.delete({
        course_id: this.course_id,
        chapter_id: this.lesson.chapter,
        lesson_id: this.lesson.id,
        id: id,
      });
      if (response) {
        this.lesson.attachments = this.lesson.attachments.filter(
          (data) => data.id != id
        );
      }
    },
    copyToClipboard() {
      navigator.clipboard.writeText(this.embedUrl);
      this.$toast.info("Copied");
    },
    async save() {
      this.$refs.formLesson.validate(async (valid, obj) => {
        if (valid) {
          let data = {
            title: this.lesson.title,
            content: this.lesson.content,
            previous_lesson_id: this.lesson.previous_lesson
              ? this.lesson.previous_lesson.id
              : null,
          };
          const response = await LessonService.update(
            {
              course_id: this.course_id,
              chapter_id: this.lesson.chapter,
              id: this.lesson.id,
            },
            data
          );
          if (response) {
            this.$toast.success("Lesson updated!");
            this.lesson = { ...response.data, chapter: this.lesson.chapter };
            this.$emit("viewEditLesson", this.lesson);
            this.last_hash = hash(this.lesson);
            this.changed = false;
          }
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
.quill-editor {
  min-height: 600px;
  max-height: fit-content;
  :deep(iframe) {
    pointer-events: none;
  }
  :deep(.ql-editor) {
    min-height: 600px !important;
  }
}
.scrollbar-demo-item {
  flex-shrink: 0;
  display: flex;
  margin: 5px;
  margin-bottom: 5px;
  border-radius: 4px;
}
.el-scrollbar {
  :deep(.el_scrollbar__thumb) {
    background-color: #25c9d0 !important;
  }
}
@import "@/assets/scss/main.scss";
</style>
