<template>
  <div>
    <TitleBar :title="course.title" v-show="course.title"></TitleBar>
    <el-row class="ml-0" :gutter="20" v-loading="loading">
      <el-col :span="18" class="is-always-shadow">
        <el-row class="mt-2">
          <el-col :span="18">
            <el-descriptions class="text-left" direction="vertical" :column="1">
              <el-descriptions-item label="Instructor:">{{
                instructor
              }}</el-descriptions-item>
              <el-descriptions-item label="Topics:">
                <el-tag
                  class="m-1"
                  v-for="topic in course.topics"
                  :key="topic.id"
                  size="small"
                  type="primary"
                  effect="dark"
                  >{{ topic.title }}</el-tag
                >
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
          <el-col :span="6" class="d-flex justify-content-end">
            <restricted-view :scope="['elearning_course:edit']">
              <el-button
                class="m-3"
                type="primary"
                size="primary"
                @click="handleUpdateCourse"
                >Edit</el-button
              >
            </restricted-view>
          </el-col>
        </el-row>
        <div v-if="viewDes">
          <h2>Description:</h2>
          <el-col class="mt-3 mb-3">
            <quill-editor
              class="view-form"
              :disabled="true"
              :options="VIEW_OPTIONS"
              v-model="course.description"
            />
          </el-col>
        </div>
        <lesson-detail v-else :chapters="detailLesson" />
      </el-col>
      <el-col :span="6" class="footer-right">
        <el-card :body-style="{ padding: '0px' }" style="color: black">
          <el-image :src="course.cover_image" fit="contain">
            <template #error>
              <div>
                <el-icon>
                  <icon-picture />
                </el-icon>
              </div>
            </template>
          </el-image>
          <h2
            class="highlight-title"
            style="cursor: pointer; max-width: fit-content"
            @click="backDes"
          >
            {{ course.title }}
          </h2>
          <chapters
            v-if="course.chapters"
            :chapters="course.chapters"
            :courseId="courseId"
            @detailLessons="detailLessons"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import CourseService from "@/services/e-learning/course";
import chapters from "@/pages/elearningCourses/detail/components/chapters.vue";
import LessonDetail from "@/pages/elearningCourses/detail/components/lesson.vue";
import RestrictedView from "@/components/RestrictedView.vue";
import { VIEW_OPTIONS } from "@/const/quillEditorModules.js";
export default {
  props: {
    courseId: String,
  },
  components: {
    chapters,
    TitleBar,
    LessonDetail,
    RestrictedView,
  },
  data() {
    return {
      VIEW_OPTIONS: VIEW_OPTIONS,
      loading: false,
      course: {},
      detailLesson: "",
      viewDes: true,
      instructor: "",
    };
  },
  created() {
    this.fetchCourse();
  },
  methods: {
    async fetchCourse() {
      this.loading = true;
      const response = await CourseService.getDetail(this.courseId);
      if (response) {
        this.course = response;
        this.instructor = response.instructor.profile.name;
      }
      this.loading = false;
    },
    handleUpdateCourse() {
      this.$router.push({ path: `/courses/${this.courseId}/edit` });
    },
    detailLessons(data) {
      this.viewDes = false;
      this.detailLesson = data;
    },
    backDes() {
      this.viewDes = true;
    },
  },
};
</script>

<style lang="scss" scoped>
.is-always-shadow {
  -webkit-box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.highlight-title {
  &:hover {
    color: #25c9d0;
  }
}

.footer-right {
  top: 56px;
  position: sticky;
  align-self: flex-start;
}
@import "@/assets/scss/main.scss";
</style>
