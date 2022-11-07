<template>
  <div class="my-3">
    <el-row :gutter="20" v-loading="loading">
      <el-col :span="18">
        <courseProfile
          :disabled="disabled"
          :currentCourse="course"
          @doneSave="doneSave"
        ></courseProfile>
      </el-col>
      <el-col :span="6" class="footer-right">
        <el-card style="color: black">
          <h2
            class="highlight-title"
            :class="{ 'view-course': viewCourse }"
            style="cursor: pointer; max-width: fit-content"
          >
            {{ course.title }}
          </h2>
          <chapters
            :key="last_hash"
            v-if="course.chapters"
            :disabled="disabled"
            :initialChapters="course.chapters"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapState } from "vuex";
import courseProfile from "@/pages/elearningCourses/create/components/courseProfile.vue";
import chapters from "@/pages/elearningCourses/create/components/chapters.vue";

export default {
  components: {
    courseProfile,
    chapters,
  },
  data() {
    return {
      loading: false,
      course: {
        created_at: null,
        updated_at: null,
        title: null,
        description: null,
        short_des: null,
        instructor: null,
        cover_image: null,
        topics: [],
        chapters: [],
      },
      viewCourse: true,
      changed: false,
      disabled: true,
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
  computed: {
    ...mapState("elearning", ["topics"]),
  },
  methods: {
    updateCourse(course) {
      this.course = course;
    },
    doneSave(check) {
      this.disabled = check;
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
// .view-course {}
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
