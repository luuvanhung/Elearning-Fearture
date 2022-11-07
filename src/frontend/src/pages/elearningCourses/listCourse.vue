<template>
  <div class>
    <div class="d-flex justify-content-between">
      <el-form
        :inline="true"
        class="demo-form-inline"
        @submit.native.prevent="getListCourses"
      >
        <el-form-item label="Course">
          <el-input
            clearable
            v-model="query.title"
            placeholder="Enter course title"
          />
        </el-form-item>
        <el-form-item label="Topics">
          <el-select
            v-model="query.topics"
            placeholder="Select topic"
            filterable
            clearable
            multiple
          >
            <el-option
              v-for="topic in topics"
              :label="topic.title"
              :value="topic.title"
              :key="topic.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" icon="el-icon-search"
            >Search</el-button
          >
        </el-form-item>
      </el-form>
      <restricted-view :scope="['elearning_course:create']">
        <div class="mr-5 bd-highlight">
          <el-button
            type="primary"
            icon="el-icon-circle-plus"
            @click="createNewCourse"
            size="medium"
            >Add Course</el-button
          >
        </div>
      </restricted-view>
    </div>
    <div v-loading="loading">
      <el-row class="list-library">
        <el-col v-for="course in currentListCourse" :key="course.id">
          <el-card :body-style="{ padding: '0px' }">
            <div
              class="image-container"
              @click="
                $router.push({
                  name: 'CourseDetail',
                  params: { id: course.id },
                })
              "
            >
              <img :src="course.cover_image" class="image" />
            </div>
            <div class="main-courses">
              <div class="content-courses">
                <h3>{{ course.title }}</h3>
                <div v-if="course.instructor">
                  <img
                    v-if="course.instructor.profile.image"
                    class="img-instructor"
                    :src="course.instructor.profile.image"
                  />
                  <img
                    v-else
                    class="img-instructor"
                    src="@/static/images/icon-whitebg.jpg"
                    alt="profile default"
                  />
                  <p v-if="course.instructor" class="instructor">
                    {{ course.instructor.profile.name }}
                  </p>
                </div>
                <span v-html="course.short_des"></span>
                <div
                  class="topic-group"
                  :class="{ 'grid-4': course.topics.length > 6 }"
                >
                  <el-tag
                    v-for="topic in course.topics"
                    :key="topic.id"
                    effect="dark"
                  >
                    {{ topic.title }}
                  </el-tag>
                </div>
              </div>
              <div class="footer-courses align-items-center">
                <restricted-view :scope="['elearning_course:destroy']">
                  <el-tooltip
                    effect="light"
                    :content="TOOLTIPS.delete_course"
                    placement="bottom"
                  >
                    <el-button
                      type="text"
                      style="font-size: 20px"
                      icon="el-icon-delete"
                      @click="handleDeleteCourse(course.id)"
                    ></el-button>
                  </el-tooltip>
                </restricted-view>
                <restricted-view :scope="['elearning_course:edit']">
                  <el-tooltip
                    effect="light"
                    :content="TOOLTIPS.edit_course"
                    placement="bottom"
                  >
                    <el-button
                      type="text"
                      style="font-size: 20px"
                      icon="el-icon-edit"
                      @click="handleUpdateCourse(course.id)"
                    ></el-button>
                  </el-tooltip>
                </restricted-view>
                <el-tooltip
                  effect="light"
                  :content="TOOLTIPS.course_detail"
                  placement="bottom"
                >
                  <el-button
                    type="text"
                    style="float: right; font-size: 20px"
                    icon="el-icon-info"
                    @click="
                      $router.push({
                        name: 'CourseDetail',
                        params: { id: course.id },
                      })
                    "
                  ></el-button>
                </el-tooltip>
                <el-tooltip
                  effect="light"
                  :content="TOOLTIPS.study_course"
                  placement="bottom"
                >
                  <el-button
                    type="text"
                    style="float: right; font-size: 20px"
                    icon="el-icon-video-play"
                    @click="handleStudyCourse(course.id)"
                  ></el-button>
                </el-tooltip>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <el-pagination
      class="pagination"
      background
      layout="prev, pager, next"
      :current-page="+query.page"
      :page-size="+query.page_size"
      @current-change="changePages"
      :total="total"
    ></el-pagination>
  </div>
</template>

<script>
import RestrictedView from "@/components/RestrictedView.vue";
import { mapActions, mapState } from "vuex";
import _ from "lodash";
import AssignmentService from "@/services/e-learning/assignment";
import CourseService from "@/services/e-learning/course";

const TOOLTIPS = {
  edit_course: "Edit this course",
  delete_course: "Delete this course",
  course_detail: "Course's detail",
  study_course: "Study this course",
};

export default {
  components: {
    RestrictedView,
  },
  data() {
    return {
      TOOLTIPS: TOOLTIPS,
      dialogAddCourse: false,
      loading: true,
      searchQuery: "",
      total: 0,
      query: {
        page: 1,
        page_size: 12,
      },
      currentListCourse: [],
    };
  },
  async created() {
    this.query = { ...this.query, ...this.$route.query };
  },
  methods: {
    ...mapActions("elearning", ["deleteCourse", "addCourse"]),
    async enrollCourse(id) {
      const assignment = await AssignmentService.getOrCreateAssignment({
        course_id: id,
      });
      if (assignment) {
        this.$router.push({
          name: "Assignment",
          params: { id: assignment.id },
        });
      }
    },
    async createNewCourse() {
      this.$router.push({ name: "CourseCreate" });
    },
    async getListCourses() {
      this.loading = true;
      let topic_ids = [];
      this.topics.map((topic) => {
        if (this.query.topics.includes(topic.title)) {
          topic_ids.push(topic.id);
        }
      });
      const data = _.omit(this.query, "topics");
      const response = await CourseService.search({
        ...data,
        topic_ids: topic_ids.join(","),
      });
      if (response) {
        this.total = response.count;
        this.currentListCourse = response.results;
      }
      this.loading = false;
    },
    async changePages(newPage) {
      this.query.page = newPage;
    },
    async handleStudyCourse(course_id) {
      await this.$confirm("Study this course?")
        .then(async (_) => {
          await this.enrollCourse(course_id);
        })
        .catch((_) => {});
    },
    async handleDeleteCourse(course_id) {
      await this.$confirm("Are you sure to delete this course?")
        .then(async (_) => {
          await this.deleteCourse(course_id);
          await this.getListCourses();
        })
        .catch((_) => {});
    },
    handleUpdateCourse(course_id) {
      this.$router.push({
        name: "CourseEdit",
        params: { id: course_id },
      });
    },
  },
  watch: {
    query: {
      deep: true,
      handler: function () {
        this.getListCourses();
        this.$router.replace({ query: this.query }).catch((err) => err);
      },
    },
    dialogAddCourse(newValue, oldValue) {
      if (oldValue && !newValue) {
        this.query.page = 1;
        this.getListCourses();
      }
    },
  },
  computed: {
    ...mapState("elearning", ["topics"]),
  },
};
</script>

<style scoped lang="scss">
.img-instructor {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.el-card {
  border-radius: 10px;
}

.pagination {
  text-align: center;
  margin-top: 35px;
}

.list-library {
  margin-left: 40px;
}

.el-carousel__item {
  margin-left: 100px !important;
}

.filter-icon {
  width: 20px;
  height: 23px;
  filter: invert(64%) sepia(94%) saturate(370%) hue-rotate(141deg)
    brightness(82%) contrast(88%);
}

.el-col {
  margin: 30px;
  width: 360px;
}

.footer-courses {
  padding: 0px 22px 0px 22px;
  height: fit-content;
}

.main-courses {
  color: black;
}

.instructor {
  /* padding-bottom: 8px; */
  font-size: 12px;
  line-height: 14px;
  color: #6a6f73;
}

.content-courses {
  margin: 20px;
  height: 230px;
  color: rgb(63, 63, 63);
}

.content-courses span {
  display: -webkit-box;
  /* height: 90px; */
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.content-courses h3 {
  /* height: 50px; */
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.image-container {
  width: 100%;
  height: 260px;
}

.image {
  width: 100%;
  height: 100%;
  display: block;
}

.time {
  font-size: 13px;
  color: #30b4c8;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.el-button--text {
  font-size: larger;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.topic-group {
  margin-bottom: 5px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 5px;
  .el-tag {
    text-align: center;
  }
  .el-tag + .el-tag {
    margin-left: 0;
  }
  .grid-4 {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}
</style>
