<template>
  <div class="d-flex form-item">
    <el-form
      :model="assignmentForm"
      label-width="200px"
      ref="assignmentForm"
      :rules="rules"
    >
      <el-form-item label="Course : " prop="course_id" class="assign-form-item">
        <el-select
          v-model="assignmentForm.course_id"
          @change="handleChangeCourse"
          clearable
        >
          <el-option
            v-for="item in courses"
            :key="item.id"
            :label="item.title"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Trainee : " class="assign-form-item" prop="user_ids">
        <el-select
          multiple
          clearable
          filterable
          v-model="assignmentForm.user_ids"
          no-data-text="Please select a course first"
        >
          <el-option
            v-for="item in allUsers"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        label="Estimation time to start : "
        class="assign-form-item"
      >
        <el-date-picker
          value-format="yyyy-MM-dd"
          type="date"
          placeholder="Pick a start date"
          v-model="assignmentForm.start_date"
          :picker-options="pickerOptionsStartDate"
          :clearable="is_allowed_to_clear_date_field"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="Estimation time to end : " class="assign-form-item">
        <el-date-picker
          value-format="yyyy-MM-dd"
          type="date"
          placeholder="Pick a due date "
          v-model="assignmentForm.due_date"
          :picker-options="pickerOptionsDueDate"
          clearable
        ></el-date-picker>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import assignments from "@/services/e-learning/assignment.js";
import CourseService from "@/services/e-learning/course.js";
export default {
  props: ["courses"],
  data() {
    return {
      is_allowed_to_clear_date_field: false,
      allUsers: [],
      data: [],
      pickerOptionsStartDate: {
        disabledDate: this.disabledStartDate,
      },
      pickerOptionsDueDate: {
        disabledDate: this.disabledDueDate,
      },
      loading: false,
      assignmentForm: {
        course_id: null,
        user_ids: [],
        start_date: null,
        due_date: null,
      },
      rules: {
        course_id: [
          { required: true, message: "Please input course", trigger: "change" },
        ],
        user_ids: [
          {
            required: true,
            message: "Please input trainee",
            trigger: "change",
          },
        ],
      },
    };
  },
  computed: {
    assignmentSendForm() {
      let assignmentsSendForm = { ...this.assignmentForm };
      return assignmentsSendForm;
    },
    today() {
      var today = new Date();
      var dd = String(today.getDate()).padStart(2, "0");
      var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
      var yyyy = today.getFullYear();

      today = `${yyyy}-${mm}-${dd}`;
      return today;
    },
  },
  created() {
    this.assignmentForm.start_date = this.today;
  },
  methods: {
    disabledStartDate(time) {
      return time.getTime() < Date.now() - 86400000;
    },
    disabledDueDate(time) {
      if (
        this.assignmentForm.start_date &&
        this.assignmentForm.start_date !== ""
      ) {
        return (
          time.getTime() <
          Math.floor(Date.parse(this.assignmentForm.start_date))
        );
      }
    },
    async handleChangeCourse(value) {
      this.assignmentForm.user_ids = [];
      this.allUsers = await CourseService.getUserExclude(value);
    },
    async handleAssignUser() {
      const data = this.assignmentSendForm;
      const res = await assignments.createNewAssignment(data);
      this.assignmentForm.course_id = null;
      this.assignmentForm.user_ids = [];
      this.assignmentForm.due_date = null;
    },
  },
};
</script>
<style lang="scss">
.center-button {
  margin: auto;
  width: min-content;
  padding-top: 50px;
}
.assign-form-item {
  & .el-form-item__content {
    @media (min-width: 576px) {
      margin-left: auto;
    }
  }
  & .el-form-item__label {
    font-size: 110%;
    color: #070707;
    text-align: start;
  }
}
</style>
