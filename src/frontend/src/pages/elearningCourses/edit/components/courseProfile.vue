<template>
  <el-card style="overflow: unset">
    <el-form
      ref="form"
      :rules="rules"
      :model="course"
      label-width="auto"
      label-position="top"
      size="large"
    >
      <el-form-item prop="title" label="Title">
        <el-input v-model="course.title"></el-input>
      </el-form-item>
      <el-form-item prop="topics" label="Topic">
        <el-select
          style="width: 100%"
          v-model="course.topics"
          value-key="id"
          filterable
          reserve-keyword
          clearable
          multiple
          placeholder="Select"
        >
          <el-option
            v-for="item in topics"
            :key="item.id"
            :label="item.title"
            :value="item"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item prop="instructor" label="Instructor">
        <el-select
          style="width: 100%"
          v-if="course.id"
          v-model="course.instructor"
          value-key="profile.name"
          filterable
          clearable
          remote
          reserve-keyword
          placeholder="Select instructor"
        >
          <el-option
            v-for="item in allUsers"
            :key="item.id"
            :label="item.profile.name"
            :value="item"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Short Description">
        <el-input v-model="course.short_des"></el-input>
      </el-form-item>
      <el-form-item label="Description">
        <quill-editor v-model="course.description" />
      </el-form-item>
      <el-form-item label="Cover Image">
        <el-upload
          class="image-uploader"
          action
          :show-file-list="false"
          :on-change="changeFile"
          :before-upload="beforeImageUpload"
          :on-success="handleImageSuccess"
        >
          <img
            v-if="course.cover_image"
            :src="course.cover_image"
            class="cover-image"
          />
          <i v-else class="el-icon-plus image-uploader-icon"></i>
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
                @click="updateCurrentCourse"
                :disabled="!changed"
                >Save</el-button
              >
            </div>
          </el-tooltip>
          <el-button type="danger" @click="deleteCurrentCourse">
            Delete
          </el-button>
          <el-button @click="handleClose">Cancel</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import CourseService from "@/services/e-learning/course";
import { mapState, mapGetters } from "vuex";
var hash = require("object-hash");
export default {
  props: {
    currentCourse: Object,
  },
  data() {
    return {
      loading: false,
      course: { ...this.currentCourse },
      original_topics_length: null,
      changed: false,
      selectedTopic: [],
      coverImageFile: null,
      rules: {
        title: [
          {
            required: true,
            message: "Please input Title",
            trigger: "blur",
          },
        ],
        topics: [
          {
            required: true,
            message: "Please input Topic",
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
    async updateCurrentCourse() {
      await this.$refs["form"].validate(async (valid, obj) => {
        if (valid) {
          let formData = new FormData();
          formData.append("id", this.course.id);
          formData.append("title", this.course.title);
          formData.append("short_des", this.course.short_des);
          formData.append("description", this.course.description);
          formData.append("instructor_id", this.course.instructor.id);
          if (this.course.topics.length === this.original_topics_length) null;
          else if (this.course.topics.length === 0)
            formData.append("topic_ids", "");
          else
            this.course.topics.map((topic) => {
              formData.append("topic_ids", topic.id);
            });
          this.coverImageFile &&
            formData.append("cover_image", this.coverImageFile.raw);
          const response = await CourseService.update(formData);
          if (response.data) {
            this.$emit("updateCourse", { ...this.course });
            this.changed = false;
          }
        }
      });
    },
    async deleteCurrentCourse() {
      await this.$confirm("Are you sure to delete this course?")
        .then(async (_) => {
          await CourseService.delete(this.course.id);
          this.$router.push({ name: "Courses" });
        })
        .catch((err) => err);
    },
    changeFile(file, fileList) {
      this.coverImageFile = file;
    },
    handleImageSuccess(res, file) {
      this.course.cover_image = URL.createObjectURL(file.raw);
    },
    beforeImageUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isPNG = file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG && !isPNG) {
        this.$toast.error("Avatar picture must be JPG or PNG format!");
      }
      if (!isLt2M) {
        this.$toast.error("Avatar picture size can not exceed 2MB!");
      }
      return (isJPG || isPNG) && isLt2M;
    },
    handleClose() {
      this.$confirm("Stop updating course?")
        .then((_) => {
          this.$router.push({
            name: "Courses",
          });
        })
        .catch((_) => {});
    },
  },
};
</script>

<style lang="scss" scoped>
.quill-editor {
  min-height: 600px;
  max-height: fit-content;
  :deep(iframe) {
    pointer-events: none;
  }
  :deep(.ql-editor) {
    min-height: 600px !important;
    color: black;
  }
}
@import "@/assets/scss/main.scss";
</style>
