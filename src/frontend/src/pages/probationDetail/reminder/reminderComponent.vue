<template>
  <div>
    <el-row
      class="d-flex mb-2"
      v-for="(reminder, index) in reminders"
      :key="index"
      style="border: 1px solid #6792a7c9; margin: 3px; padding: 3px"
    >
      <el-col :span="2">
        <i class="el-icon-bell"></i>
      </el-col>
      <el-col :span="4">
        <h3>Remind people</h3>
      </el-col>
      <el-col :span="3">
        <el-input-number
          v-model="listDuration[index]"
          size="small"
          controls-position="right"
          @change="
            changeReminderDate(listDuration[index], listTimeUnit[index], index)
          "
          :min="1"
          :max="10"
          defau
        >
        </el-input-number>
      </el-col>
      <el-col :span="3">
        <el-select
          v-model="listTimeUnit[index]"
          size="small"
          @change="
            changeReminderDate(listDuration[index], listTimeUnit[index], index)
          "
        >
          <el-option
            v-for="(item, key, index) in timeUnits"
            :key="index"
            :label="key"
            :value="key"
          >
          </el-option>
        </el-select>
      </el-col>

      <el-col :span="7">
        <span>before the end of the probation period</span>
      </el-col>
      <el-col :span="3" class="mr-2">
        <el-input v-model="reminder.reminder_date" disabled></el-input>
      </el-col>
      <el-col :span="1">
        <el-button
          class="btn-icon ml-2"
          type="danger"
          size="small"
          icon="el-icon-close"
          @click="deleteReminder(index)"
        ></el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "ReminderComponent",
  props: {
    reminders: Array,
    timeUnits: Object,
    getReminderDate: Function,
    probationEndDate: String,
  },
  data() {
    return {
      isChange: false,
      listDuration: [],
      listTimeUnit: [],
      dayUnit: "days",
      weekUnit: "weeks",
    };
  },
  methods: {
    changeReminderDate(duration, timeUnitKey, index) {
      this.reminders[index].reminder_date = this.getReminderDate(
        this.timeUnits[timeUnitKey].value * duration
      );
    },
    deleteReminder(index) {
      if (this.reminders.length >= 1) this.reminders.splice(index, 1);
    },
    getListDuration(reminders) {
      let listDuration = [];
      let listTimeUnit = [];
      for (let i = 0; i < reminders.length; i++) {
        let subDays =
          new Date(this.probationEndDate).getDate() -
          new Date(reminders[i].reminder_date).getDate();
        listDuration.push(subDays);
        if (subDays <= 7) listTimeUnit.push(this.dayUnit);
        else if (subDays > 7) listTimeUnit.push(this.weekUnit);
      }
      this.listDuration = listDuration;
      this.listTimeUnit = listTimeUnit;
    },
  },
  watch: {
    reminders() {
      this.getListDuration(this.reminders);
    },
  },
  created() {
    this.getListDuration(this.reminders);
  },
};
</script>

<style lang="scss">
@import "./reminder.scss";
</style>
