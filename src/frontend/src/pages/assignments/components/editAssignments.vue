<template>
  <div class="d-flex form-item">
    <el-form :model="assignFormEditClone" label-width="200px" ref="editAssign">
      <el-form-item label="Course : " class="assign-form-item">
        <el-input
          :placeholder="assignFormEditClone.course_name"
          :disabled="true"
        >
        </el-input>
      </el-form-item>
      <el-form-item label="Trainee : " class="assign-form-item">
        <el-input :placeholder="assignFormEditClone.full_name" :disabled="true">
        </el-input>
      </el-form-item>
      <el-form-item
        label="Estimation time to start : "
        class="assign-form-item"
      >
        <el-date-picker
          value-format="yyyy-MM-dd"
          type="date"
          placeholder="Pick a date begin"
          v-model="assignFormEditClone.start_date"
          :picker-options="pickerOptionsStartDate"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="Estimation time to end : " class="assign-form-item">
        <el-date-picker
          value-format="yyyy-MM-dd"
          type="date"
          placeholder="Pick a due date "
          v-model="assignFormEditClone.due_date"
          :picker-options="pickerOptionsDueDate"
        ></el-date-picker>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import assignments from "@/services/e-learning/assignment.js";
export default {
  props: ["assignFormEdit"],
  data() {
    return {
      assignFormEditClone: { ...this.assignFormEdit },
      pickerOptionsStartDate: {
        disabledDate: this.disabledStartDate,
      },
      pickerOptionsDueDate: {
        disabledDate: this.disabledDueDate,
      },
    };
  },
  methods: {
    bindingTotable() {
      this.assignFormEdit.start_date = this.assignFormEditClone.start_date;
      this.assignFormEdit.due_date = this.assignFormEditClone.due_date;
    },
    disabledDueDate(time) {
      if (
        this.assignFormEditClone.start_date &&
        this.assignFormEditClone.start_date !== ""
      ) {
        let start_second = Date.parse(this.assignFormEditClone.start_date);
        let now_second = Date.now();
        return start_second > now_second
          ? time.getTime() < start_second
          : time.getTime() < now_second;
      }
    },
    disabledStartDate(time) {
      return time.getTime() <= Date.now();
    },
    async editAssignment() {
      this.bindingTotable();
      const id = this.assignFormEdit.id;
      const start_date = this.assignFormEdit.start_date;
      const due_date = this.assignFormEdit.due_date;
      const param = {
        start_date:
          start_date !== null
            ? start_date.toString().slice(0, 10) + " 00:00:00"
            : null,
        due_date:
          due_date !== null
            ? due_date.toString().slice(0, 10) + " 00:00:00"
            : null,
      };
      const res = await assignments.editAssignment(id, param);
      if (res) {
        return true;
      } else {
        return false;
      }
    },
  },
  watch: {
    assignFormEdit: {
      deep: true,
      handler: function () {
        this.assignFormEditClone = { ...this.assignFormEdit };
      },
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
