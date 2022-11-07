<template>
  <form @submit.prevent="editData(currentSession)">
    <h5 class="header">Add Session</h5>
    <div class="col p-4 content">
      <div class="d-flex justify-content-center align-items-center">
        <span class="input-label">Time range:</span>
        <el-time-select
          placeholder="Start time"
          v-model="currentSession.start_time"
          :picker-options="{
            start: '00:00',
            step: '00:30',
            end: '24:00',
          }"
        >
        </el-time-select>
        <span class="mr-2 ml-2">To</span>
        <el-time-select
          placeholder="End time"
          v-model="currentSession.end_time"
          :picker-options="{
            start: '00:00',
            step: '00:30',
            end: '24:00',
            minTime: currentSession.start_time,
          }"
        >
        </el-time-select>
      </div>
      <button
        type="submit"
        class="d-flex justify-content-center align-items-center addData"
      >
        Save
      </button>
    </div>
  </form>
</template>

<script>
import Session from "@/services/office/office.session";

export default {
  name: "editSession",
  middleware: "authentication",
  props: {
    sessionEdit: Object,
  },
  data() {
    return {
      currentSession: {
        start_time: this.sessionEdit.start_time,
        end_time: this.sessionEdit.end_time,
      },
      editDaysOfWeek: [],
    };
  },
  watch: {
    sessionEdit: function (day) {
      this.currentSession.start_time = day.start_time;
      this.currentSession.end_time = day.end_time;
    },
  },
  methods: {
    async editData(currentSession) {
      let data = {
        dow: this.sessionEdit.dow,
        start_time: currentSession.start_time,
        end_time: currentSession.end_time,
        office: this.sessionEdit.office,
      };
      try {
        const res = await Session.update(this.sessionEdit.id, data);
        if (res.status === 200) {
          this.sessionEdit.start_time = currentSession.start_time;
          this.sessionEdit.end_time = currentSession.end_time;
          this.$toast.success("Edited Successfully");
        }
      } catch (err) {
        const myJSX = <span>{err.response.data.detail}</span>;
        this.$toast.error(myJSX);
      }
    },
  },
};
</script>

<style scoped>
table {
  margin-top: 4%;
  width: 100%;
  border-collapse: collapse;
}

form {
  margin: auto;
}

.input-label {
  display: inline-block;
  width: 20%;
}
</style>
