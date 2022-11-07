<template>
  <div v-if="course.id" class="my-3">
    <TitleBar
      :title="`Edit course: ${course.title}`"
      v-show="course.title"
    ></TitleBar>
    <el-row :gutter="20" v-loading="loading">
      <el-col :span="18">
        <courseProfile
          v-if="viewCourse"
          :currentCourse="course"
          @updateCourse="updateCourse"
        ></courseProfile>
        <editLesson
          v-else-if="viewLesson"
          :key="currentLesson.id"
          :currentLesson="currentLesson"
          :currentChapter="currentChapter"
          @viewEditLesson="viewEditLesson"
          @viewEditCourse="viewEditCourse"
        />
        <editChapter
          v-else-if="viewChapter"
          :key="currentChapter.id"
          :initialChapters="course.chapters"
          :currentChapter="currentChapter"
          @viewEditChapter="viewEditChapter"
          @viewEditCourse="viewEditCourse"
        />
        <createChapter
          v-else-if="chapterViewCreate"
          :chapters="course.chapters"
          @viewEditChapter="viewEditChapter"
          @viewEditCourse="viewEditCourse"
        />
        <createLesson
          v-else-if="lessonViewCreate"
          :key="currentLesson.id"
          :currentLesson="currentLesson"
          :currentChapter="currentChapter"
          @viewEditLesson="viewEditLesson"
          @viewEditCourse="viewEditCourse"
        />
      </el-col>
      <el-col :span="6" class="footer-right">
        <el-card style="color: black">
          <h2
            class="highlight-title"
            :class="{ 'view-course': viewCourse }"
            style="cursor: pointer; max-width: fit-content"
            @click="viewEditCourse"
          >
            {{ course.title }}
          </h2>
          <chapters
            :key="last_hash"
            v-if="course.chapters"
            :initialChapters="course.chapters"
            :course_id="courseId"
            :currentLesson="currentLesson"
            :currentChapter="currentChapter"
            :lessonViewCreate="lessonViewCreate"
            @updateChapters="updateChapters"
            @viewCreateLesson="viewCreateLesson"
            @viewEditLesson="viewEditLesson"
            @viewCreateChapter="viewCreateChapter"
            @viewEditChapter="viewEditChapter"
            @viewEditCourse="viewEditCourse"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import CourseService from "@/services/e-learning/course";
import { mapState, mapGetters } from "vuex";
import TitleBar from "@/components/TitleBar.vue";
import courseProfile from "@/pages/elearningCourses/edit/components/courseProfile.vue";
import chapters from "@/pages/elearningCourses/edit/components/chapters.vue";
import editLesson from "@/pages/elearningCourses/edit/components/editLesson.vue";
import createLesson from "@/pages/elearningCourses/edit/components/createLesson.vue";
import editChapter from "@/pages/elearningCourses/edit/components/editChapter.vue";
import createChapter from "@/pages/elearningCourses/edit/components/createChapter.vue";
var hash = require("object-hash");
export default {
  props: {
    courseId: String,
  },
  components: {
    TitleBar,
    courseProfile,
    chapters,
    editLesson,
    createLesson,
    editChapter,
    createChapter,
  },
  data() {
    return {
      loading: false,
      course: {},
      currentLesson: {},
      currentChapter: {},
      viewCourse: true,
      viewChapter: false,
      viewLesson: false,
      chapterViewCreate: false,
      lessonViewCreate: false,
      original_topics_length: null,
      changed: false,
      selectedTopic: null,
      coverImageFile: null,
      rules: {
        title: [
          {
            required: true,
            message: "Please input Title",
            trigger: "blur",
          },
        ],
        instructor: [
          {
            required: true,
            message: "Please input Instructor",
            trigger: "blur",
          },
        ],
      },
      last_hash: null,
    };
  },
  created() {
    this.fetchCurrentCourse();
  },
  computed: {
    ...mapState("elearning", ["topics"]),
    ...mapGetters({ allUsers: "user/allUsers" }),
  },
  watch: {
    course: {
      deep: true,
      handler(newValue, oldValue) {
        const newHash = hash(newValue);
        if (oldValue.id && newHash != this.last_hash) {
          this.changed = true;
        }
        this.last_hash = newHash;
      },
    },
  },
  methods: {
    updateChapters(chapters) {
      this.course.chapters = chapters;
    },
    viewCreateLesson(chapter, lesson) {
      this.currentLesson = lesson;
      this.currentChapter = chapter;
      this.lessonViewCreate = true;
      this.chapterViewCreate = false;
      this.viewLesson = false;
      this.viewCourse = false;
      this.viewChapter = false;
    },
    viewCreateChapter() {
      this.chapterViewCreate = true;
      this.lessonViewCreate = false;
      this.viewLesson = false;
      this.viewCourse = false;
      this.viewChapter = false;
    },
    viewEditChapter(currentChapter) {
      this.viewChapter = true;
      this.viewCourse = false;
      this.viewLesson = false;
      this.chapterViewCreate = false;
      this.lessonViewCreate = false;
      this.currentChapter = currentChapter;
      const chapterIndex = this.course.chapters.findIndex(
        (chapter) => chapter.id === currentChapter.id
      );
      if (chapterIndex != -1)
        this.course.chapters[chapterIndex] = currentChapter;
      else this.course.chapters.push(currentChapter);
      this.last_hash = hash(this.course);
    },
    viewEditLesson(lesson) {
      this.currentLesson = lesson;
      this.viewLesson = true;
      this.viewCourse = false;
      this.viewChapter = false;
      this.chapterViewCreate = false;
      this.lessonViewCreate = false;
      this.course.chapters.forEach((chapter) => {
        if (chapter.id === lesson.chapter) {
          for (let i = 0; i < chapter.lessons.length; i++) {
            if (lesson.id === chapter.lessons[i].id) {
              chapter.lessons[i] = lesson;
              this.currentChapter = chapter;
              this.last_hash = hash(this.course);
              return;
            }
          }
          chapter.lessons.push(lesson);
        }
      });
    },
    viewEditCourse() {
      this.viewCourse = true;
      this.viewLesson = false;
      this.lessonViewCreate = false;
      this.chapterViewCreate = false;
      this.viewChapter = false;
    },
    updateCourse(course) {
      this.course = course;
    },
    async fetchCurrentCourse() {
      this.loading = true;
      const response = await CourseService.getDetail(this.courseId);
      if (response) {
        this.course = Object.assign({}, response);
        this.original_topics_length = this.course.topics.length;
      }
      this.change = false;
      this.loading = false;
    },
  },
};
</script>
<style lang="scss" scoped>
.highlight-title {
  &:hover {
    color: #25c9d0;
  }
}
.quill-editor {
  min-height: 600px;
  max-height: fit-content;
  :deep(.ql-editor) {
    min-height: 600px !important;
    color: black;
  }
}
.footer-right {
  position: sticky;
  top: 57px;
  align-self: flex-start;
}
</style>
