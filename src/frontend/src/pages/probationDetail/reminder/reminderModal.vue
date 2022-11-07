<template>
  <div>
    <restricted-view :scopes="['probation:create']">
      <el-button
        type="success"
        @click="isShow = true"
        icon="el-icon-message-solid"
      >
        <span class="mr-2">Reminder Settings</span>
      </el-button>
    </restricted-view>
    <el-dialog title="REMINDER" :visible.sync="isShow" class="reminder-dialog">
      <el-form class="reminder-form ml-3">
        <ReminderComponent
          :reminders="reminders"
          :getReminderDate="getReminderDate"
          :timeUnits="timeUnits"
          :probationEndDate="probationEndDate"
        />
        <el-button type="text" class="add-reminder-row" @click="addReminder"
          >Add reminder
        </el-button>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="isShow = false">Cancel</el-button>
        <el-button type="primary" @click="saveReminder">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import ReminderComponent from "./reminderComponent";
import ProbationReminderService from "@/services/probation_management/reminder.service";
import { TIME_UNIT } from "@/const/probationReminder";
import moment from "moment";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "ReminderModal",
  components: {
    ReminderComponent,
    RestrictedView,
  },
  props: {
    probationEndDate: String,
  },
  async created() {
    this.timeUnits = TIME_UNIT;
    await this.getReminders();
  },
  data() {
    return {
      isShow: false,
      activeIndex: "1",
      reminders: [],
      isCreated: true,
      timeUnits: [],
      newReminders: [],
      maxReminderDate: "",
    };
  },
  watch: {
    isShow() {
      if (!this.isShow) setTimeout(this.resetDialog, 300);
    },
  },
  methods: {
    addReminder() {
      if (this.reminders.length < 5) {
        const reminderObj = {
          reminder_date: this.getReminderDate(),
        };
        this.newReminders.push(reminderObj);
        this.reminders = [...this.reminders, reminderObj];
      } else {
        this.$nextTick(() => {
          this.$toast.warning("You can only add up to 5 reminders!");
        });
      }
    },
    getReminderDate(duration = 1) {
      const date = new Date(this.probationEndDate);
      const reminderMoment = moment(date.setDate(date.getDate() - duration));
      return reminderMoment.format("YYYY-MM-DD");
    },
    async getReminders() {
      const res = await ProbationReminderService.getReminders(
        this.$route.params.id
      );
      if (res.data && res.data.length) {
        this.reminders = [...res.data];
        const reminderDates = this.reminders.map(
          (item) => new Date(item.reminder_date)
        );
        this.$emit(
          "maxReminderDate",
          moment(new Date(Math.max(...reminderDates))).format("YYYY-MM-DD")
        );
      } else {
        this.isCreated = false;
      }
    },
    resetDialog() {
      this.isShow = false;
      this.$nextTick(async () => {
        await this.getReminders();
      });
      this.reminders = [];
      this.newReminders = [];
    },
    isExistsReminderDate() {
      let unique = [
        ...new Set(this.reminders.map((item) => item.reminder_date)),
      ];
      return unique.length < this.reminders.length;
    },
    async saveReminder() {
      if (!this.isExistsReminderDate()) {
        if (!this.isCreated && this.reminders.length) {
          await ProbationReminderService.create(
            this.newReminders,
            this.$route.params.id
          )
            .then((res) => {
              if (res.status === 201) {
                this.$nextTick(() => {
                  this.$toast.success("Set reminder time successfully");
                });
              }
            })
            .catch((e) => {
              const error = e.response.data.error;
              this.$toast.error(error);
            });
          this.isCreated = true;
        } else if (this.isCreated) {
          this.isShow = false;
          await ProbationReminderService.update(
            this.reminders,
            this.$route.params.id
          )
            .then((res) => {
              if (res.status === 200) {
                this.$nextTick(() => {
                  this.$toast.success("Set reminder time successfully");
                });
              }
            })
            .catch((e) => {
              const error = e.response.data.error;
              this.$toast.error(error);
            });
        }
        this.isShow = false;
        this.resetDialog();
      } else {
        this.$toast.error("There already exists reminder date");
      }
    },
  },
};
</script>

<style lang="scss">
@import "./reminder.scss";
</style>
