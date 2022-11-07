<template>
  <div class="mt-3">
    <el-card class="find-employee-box my-3">
      <div slot="header" class="clearfix">
        <span>Find assignment</span>
      </div>
      <el-form @submit.native.prevent="search" :inline="true">
        <el-row :gutter="100">
          <el-col :span="6" class="keyword-box d-flex flex-column mt-3">
            <el-input placeholder="Search" v-model="filter.keyword" clearable>
              <i slot="prefix" class="el-input__icon el-icon-search"></i>
            </el-input>
          </el-col>
          <el-col :span="6" class="d-flex flex-column mb-3">
            <span>From date</span>
            <el-date-picker
              type="date"
              v-model="filter.from_date"
              placeholder="Pick a day"
              value-format="yyyy-MM-dd"
            />
          </el-col>
          <el-col :span="6" class="d-flex flex-column mb-3">
            <span>To date</span>
            <el-date-picker
              type="date"
              v-model="filter.to_date"
              placeholder="Pick a day"
              value-format="yyyy-MM-dd"
            />
          </el-col>
          <el-col :span="6" class="d-flex flex-column mb-3">
            <span>Status</span>
            <div>
              <el-checkbox
                @change="onSelectAllStatuses"
                :indeterminate="isIndeterminateStatusesSeleted"
                v-model="selectedAllStatus"
                >All</el-checkbox
              >
              <el-checkbox-group
                v-model="filter.statuses"
                @change="onSelectedStatusesChange"
              >
                <el-checkbox
                  v-for="status in STATUSES"
                  :key="status"
                  :label="status"
                  :value="status"
                  >{{ status }}</el-checkbox
                >
              </el-checkbox-group>
            </div>
          </el-col>
        </el-row>
        <el-row>
          <el-button
            native-type="submit"
            type="primary"
            icon="el-icon-search"
            round
            >Search
          </el-button>
        </el-row>
      </el-form>
    </el-card>
    <restricted-view :scopes="['elearning_assignment:edit']">
      <el-row type="flex" justify="end" class="r-add">
        <el-button
          type="primary"
          icon="el-icon-plus"
          round
          :disabled="loading"
          @click="handleNewAssignment"
        >
          New assignments
        </el-button>
      </el-row>
      <assigmentsTable
        :assignments="assignments"
        :loading="loading"
        @del="delAssignment()"
      />
      <el-row type="flex" justify="center">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="+query.page_size"
          :current-page="+query.page"
          :page-count="+pageCount"
          @current-change="setPage"
        />
      </el-row>
    </restricted-view>
  </div>
</template>

<script>
import assigmentsTable from "@/pages/assignments/components/assigmentsTable.vue";
import AssignService from "@/services/e-learning/assignment.js";
import CourseService from "@/services/e-learning/course.js";
import { ASSIGNMENT_STATUSES } from "@/const/AssignmentDetail.js";
import { mapGetters } from "vuex";
import RestrictedView from "../../components/RestrictedView.vue";
export default {
  props: ["id"],
  components: {
    assigmentsTable,
    RestrictedView,
  },
  data() {
    return {
      loading: false,
      STATUSES: Object.keys(ASSIGNMENT_STATUSES),
      add: false,
      assignments: [],
      courses: [],
      total: 0,
      query: {
        page: 1,
        page_size: 12,
      },
      pageCount: 0,
      filter: {
        keyword: null,
        statuses: [],
        from_date: null,
        to_date: null,
      },
      selectedAllStatus: false,
    };
  },
  created() {
    this.fetchCourses();
    this.fetchAssignments();
  },
  methods: {
    handleNewAssignment() {
      const h = this.$createElement;
      this.$msgbox({
        title: "New assignments",
        customClass: "new",
        message: h(
          "NewAssignment",
          {
            props: {
              allUsers: this.allUsers,
              courses: this.courses,
            },
            on: {},
          },
          []
        ),
        roundButton: true,
        beforeClose: (action, instances, done) => {
          if (action === "confirm") {
            instances.$children[2].$refs["assignmentForm"].validate((valid) => {
              if (valid) {
                instances.$children[2].handleAssignUser();
                this.add = true;
                done();
              }
            });
          } else {
            done();
          }
        },
      }).then(() => {
        if (this.add) {
          setTimeout(this.fetchAssignments, 500);
          this.add = false;
        }
      });
    },
    delAssignment() {
      if (
        (this.total - 1) % this.query.page_size === 0 &&
        this.query.page !== 1 &&
        this.query.page === this.pageCount
      ) {
        this.query.page = this.query.page - 1;
      }
      this.fetchAssignments();
    },
    onSelectedStatusesChange(val) {
      this.selectedAllStatus = val.length === this.STATUSES.length;
    },
    onSelectAllStatuses(value) {
      this.filter.statuses = value ? this.STATUSES : [];
    },
    setPage(page) {
      this.query.page = page;
      this.fetchAssignments();
    },
    async fetchAssignments() {
      this.loading = true;
      const response = await AssignService.getAssignments(this.query);
      if (response) {
        this.assignments = response.results;
        this.pageCount = response.page_number;
        this.total = response.count;
        this.loading = false;
      }
    },
    selectAllChange(value) {
      if (value) {
        this.filter.statuses = this.STATUSES;
      } else {
        this.filter.statuses = [];
      }
    },
    async fetchCourses() {
      const res = await CourseService.getAll();
      if (res) {
        this.courses = res.map((course) => ({
          title: course.title,
          id: course.id,
        }));
      }
    },
    search() {
      this.query.page = 1;
      this.query = {
        ...this.query,
        from_date: this.filter.from_date,
        to_date: this.filter.to_date,
        keyword: this.filter.keyword,
        statuses: this.filter.statuses.join(","),
      };
      this.fetchAssignments();
    },
  },
  computed: {
    ...mapGetters({ allUsers: "user/allUsers" }),
    isIndeterminateStatusesSeleted() {
      const noOfSelected = this.filter.statuses.length;
      const result = noOfSelected > 0 && noOfSelected < this.STATUSES.length;
      return result;
    },
  },
};
</script>

<style lang="scss">
.keyword-box {
  padding-top: 3px;
}
.el-date-editor.el-input {
  position: relative !important;
  font-size: 14px !important;
  display: inline-block !important;
  width: 100% !important;
}
.r-add {
  padding: 10px;
}
.new {
  min-width: 550px !important;
  .el-message-box__content {
    display: flex !important;
    justify-content: center !important;
  }
}
@media screen and (max-width: 1000px) {
  .el-col-6 {
    width: 100% !important;
    margin-top: 0 !important;
  }
}
</style>
