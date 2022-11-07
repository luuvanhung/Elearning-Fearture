<template>
  <div class="container my-3" v-loading="loading" v-if="filtered_assignments">
    <div>
      <el-form :inline="true" class="demo-form-inline container">
        <el-form-item label="Course">
          <el-input
            clearable
            v-model="search_title"
            placeholder="Enter course title"
          />
        </el-form-item>
        <el-form-item label="Topic">
          <el-select
            v-model="search_topics"
            placeholder="Select topics"
            multiple
            filterable
            clearable
          >
            <el-option
              v-for="topic in topics"
              :key="topic.id"
              :label="topic.title"
              :value="topic.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Status">
          <el-select
            v-model="search_status"
            placeholder="Select Assignment's Status"
            clearable
          >
            <el-option
              v-for="status in statuses"
              :key="status.value"
              :label="status.label"
              :value="status.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    <div class="card-wrapper" v-loading="loading">
      <el-popover
        v-for="assignment in paginated_assignments[current_page - 1]"
        :key="assignment.id"
        placement="right"
        trigger="hover"
      >
        <el-card>
          <h1 class="title">{{ assignment.title }}</h1>
          <div class="description">
            <p>
              <small
                >{{ assignment.number_of_chapters }} Chapters |
                {{ assignment.number_of_lessons }} Lessons |
                {{ assignment.number_of_attachments }} Attachments</small
              >
            </p>
            <span style="color: #1e6055"
              >Assigned
              <strong>{{
                getTimeAgo(assignment.assignment.assigned_at)
              }}</strong></span
            >
            <span style="color: #ff7f3f"
              >Due Date:
              <strong>{{
                assignment.assignment.due_date
                  ? assignment.assignment.due_date.slice(0, 10)
                  : `Currently Not`
              }}</strong></span
            >
            <span style="color: #25c9d0"
              >Status:
              <strong>{{
                assignment_statuses[assignment.assignment.status].detail
              }}</strong></span
            >
            <el-progress
              style="margin-top: 5px"
              :text-inside="true"
              :stroke-width="16"
              :percentage="
                assignment.number_of_chapters &&
                Math.round(
                  (assignment.assignment.number_of_completed_chapters /
                    assignment.number_of_chapters) *
                    100
                )
              "
            ></el-progress>
            <p class="short-des">{{ assignment.short_des }}</p>
          </div>
          <el-button
            type="primary"
            @click="
              $router.push({
                name: 'Assignment',
                params: { id: assignment.assignment_id },
              })
            "
            >Study Now</el-button
          >
        </el-card>
        <div
          class="card"
          slot="reference"
          @click="
            $router.push({
              name: 'Assignment',
              params: { id: assignment.assignment_id },
            })
          "
        >
          <div class="card-image">
            <img
              :src="
                assignment.cover_image ||
                `https://vnpi-hcm.vn/wp-content/uploads/2018/01/no-image-800x600.png`
              "
            />
          </div>
          <div class="card-description">
            <p class="card-description__title">{{ assignment.title }}</p>
            <div v-if="assignment.instructor">
              <img
                v-if="assignment.instructor.profile.image"
                class="img-instructor"
                :src="assignment.instructor.profile.image"
              />
              <img
                v-else
                class="img-instructor"
                src="@/static/images/icon-whitebg.jpg"
                alt="profile default"
              />
              <div class="d-flex justify-content-between pt-2 pb-2">
                <span class="card-description__instructor">{{
                  assignment.instructor.profile.name
                }}</span>
                <el-tooltip
                  class="item"
                  effect="light"
                  :content="
                    assignment_statuses[assignment.assignment.status].tooltip
                  "
                  placement="left"
                  style="padding: 0"
                >
                  <i
                    style="font-size: 20px; color: #25c9d0"
                    :class="
                      assignment_statuses[assignment.assignment.status].icon
                    "
                  ></i>
                </el-tooltip>
              </div>
            </div>
            <p class="card-description__short-des">
              {{ assignment.short_des }}
            </p>
          </div>
          <div
            class="topic-group"
            :class="{
              'grid-4': assignment.topics.length > 6,
            }"
          >
            <el-tag
              v-for="topic in assignment.topics"
              :key="topic.id"
              effect="dark"
            >
              {{ topic.title }}
            </el-tag>
          </div>
        </div>
      </el-popover>
    </div>
    <el-pagination
      class="pagination"
      background
      layout="prev, pager, next"
      :current-page="current_page"
      :page-size="page_size"
      :total="total"
      @prev-click="current_page -= 1"
      @next-click="current_page += 1"
      @current-change="current_page = $event"
    ></el-pagination>
  </div>
  <div
    v-else
    class="container mt-4 d-flex align-items-center justify-content-center"
  >
    <p>Currently, You have no assignment!</p>
  </div>
</template>

<script>
import AssignmentService from "@/services/e-learning/assignment";
import TimeAgo from "javascript-time-ago";
import en from "javascript-time-ago/locale/en";
import { TOOLTIPS, ASSIGNMENT_STATUSES } from "@/const/AssignmentDetail";
import { mapState } from "vuex";

export default {
  components: {},
  data() {
    return {
      assignments: null,
      loading: false,
      search_title: "",
      search_topics: [],
      search_status: "",
      courses: null,
      current_page: 1,
      page_size: 6,
    };
  },
  async created() {
    await this.getAssignments();
  },
  methods: {
    async getAssignments() {
      this.loading = true;
      const result = await AssignmentService.getMyAssignments();
      if (result) {
        this.assignments = result.results;
        this.assignments.forEach((assignment) => {
          assignment["topic_ids"] = [];
          if (assignment.topics.length) {
            assignment.topics.forEach((topic) => {
              assignment["topic_ids"].push(topic.id);
            });
          }
        });
      }
      this.loading = false;
    },
    getTimeAgo(dateTime) {
      TimeAgo.addLocale(en);
      const timeAgo = new TimeAgo("en-US");
      return timeAgo.format(new Date(dateTime).getTime());
    },
  },
  computed: {
    ...mapState("elearning", ["topics"]),
    filtered_by_title_assignments() {
      if (this.search_title) {
        return this.assignments.filter((assignment) =>
          assignment.title
            .toLowerCase()
            .includes(this.search_title.toLowerCase())
        );
      } else return this.assignments;
    },
    filtered_by_topics_assignments() {
      if (this.search_topics.length) {
        return this.assignments.filter((assignment) =>
          this.search_topics.every((topic) =>
            assignment.topic_ids.includes(topic)
          )
        );
      } else return this.assignments;
    },
    filtered_by_status_assignments() {
      if (this.search_status) {
        return this.assignments.filter(
          (assignment) => assignment.assignment.status === this.search_status
        );
      } else return this.assignments;
    },
    filtered_assignments() {
      return (
        !this.loading &&
        this.filtered_by_title_assignments
          .filter((assignment) =>
            this.filtered_by_topics_assignments.includes(assignment)
          )
          .filter((assignment) =>
            this.filtered_by_status_assignments.includes(assignment)
          )
      );
    },
    total() {
      return this.filtered_assignments.length;
    },
    paginated_assignments() {
      const paginated_assignments = [];
      for (
        let i = 0;
        i < this.filtered_assignments.length;
        i += this.page_size
      ) {
        paginated_assignments.push(
          this.filtered_assignments.slice(i, i + this.page_size)
        );
      }
      return paginated_assignments;
    },
    attachment_tooltips() {
      return TOOLTIPS;
    },
    assignment_statuses() {
      return ASSIGNMENT_STATUSES;
    },
    statuses() {
      let statuses = [];
      for (const property in ASSIGNMENT_STATUSES) {
        statuses.push({
          value: property,
          label: ASSIGNMENT_STATUSES[property].detail,
        });
      }
      return statuses;
    },
  },
};
</script>

<style lang="scss" scoped>
.img-instructor {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}
.pagination {
  text-align: center;
  margin-top: 35px;
}
.el-form {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
}

.container {
  max-width: 1288px;
}

.el-card {
  width: 340px;
  box-shadow: 0 0 0 1px #d1d7dc, 0 2px 4px rgba(0, 0, 0, 0.08),
    0 4px 12px rgba(0, 0, 0, 0.08);
  color: #1c1d1f;

  h1 {
    font-size: 19px;
    line-height: 21px;
    font-weight: 700;
    padding-bottom: 16px;
  }
  small {
    color: #6a6f73;
  }

  .description {
    * {
      padding-bottom: 10px;
    }
    span {
      padding-bottom: 5px;
      display: block;
    }
    .short-des {
      margin-top: 5px;
    }
  }
  .el-button {
    width: 100%;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
}

.card-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  padding: 20px 40px;
  gap: 60px 60px;

  .card {
    height: 500px;
    width: 360px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 10px 10px 8px #d8d5d5;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    cursor: pointer;
  }

  .card-image {
    width: 100%;
    height: 240px;
    border-bottom: 1px solid #ccc;
    img {
      height: 100%;
      width: 100%;
      object-fit: cover;
      display: block;
    }
  }

  .card-description {
    padding: 0 20px;
    color: #1c1d1f;
    span {
      display: block;
    }

    &__title {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      margin: 5px 0px;
      font-weight: 600;
      font-size: 18px;
      line-height: 19px;
    }
    &__instructor {
      padding-bottom: 12px;
      font-size: 12px;
      line-height: 16px;
      color: #6a6f73;
    }
    &__short-des {
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }

  .topic-group {
    margin-bottom: 5px;
    padding: 10px 20px 14px;
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
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}
@media screen and (max-width: 1524px) {
  .card-wrapper {
    grid-template-columns: 1fr 1fr;
  }
}
@media screen and (max-width: 1100px) {
  .card-wrapper {
    grid-template-columns: 1fr;
  }
}
</style>
