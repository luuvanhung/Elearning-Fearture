<template>
  <div class="sync-buttons">
    <el-form :model="syncForm" :rules="syncRules" :inline="true" ref="syncForm">
      <el-form-item prop="date" label="Sync to Company Calendar">
        <el-date-picker
          v-model="syncForm.date"
          type="daterange"
          range-separator="-"
          start-placeholder="Start date"
          end-placeholder="End date"
        >
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          icon="el-icon-refresh"
          @click="handleSyncData"
        ></el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import WorkdayCalendarService from "@/services/leave_management/workdayCalendarService.js";

export default {
  data() {
    var requiredDate = (rule, value, callback) => {
      if (Object.keys(value).length === 0)
        return callback(new Error("Please pick a date"));

      return callback();
    };
    return {
      dateSync: [],
      syncForm: {
        date: [],
      },
      syncRules: {
        date: [{ validator: requiredDate, trigger: "change" }],
      },
    };
  },
  methods: {
    handleSyncData() {
      this.$refs.syncForm.validate(this._handleSyncData);
    },
    async _handleSyncData(valid) {
      if (!valid) return;

      const res = await WorkdayCalendarService.syncData(this.dateSyncISOString);
      if (res && res.status == 200) {
        await this.$emit("asyncDataActive");
        await this.$toast.info("Data syncing...");
      } else {
        this.$toast.console.error("Sync leave request fail");
      }
    },
    resetForm(formName) {
      this.$refs.syncForm.resetFields();
    },
  },
  computed: {
    dateSyncISOString() {
      return this.syncForm.date.map((date) =>
        new Date(
          date.getTime() - date.getTimezoneOffset() * 60000
        ).toISOString()
      );
    },
  },
};
</script>

<style lang="scss">
.sync-buttons {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}
</style>
