<template>
  <form @submit.prevent="addData(currentSession)">
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
  name: "addSession",
  props: {
    sessions: Array,
    dayAddSession: Object,
  },
  data() {
    return {
      currentSession: {
        start_time: "",
        end_time: "",
        dow: "",
      },
      arrSession: [],
    };
  },
  methods: {
    async addData(currentSession) {
      let data = {
        dow: this.dayAddSession.dow,
        start_time: currentSession.start_time,
        end_time: currentSession.end_time,
        office: this.$route.params.id,
      };
      try {
        const res = await Session.create(data);
        if (res.status === 201) {
          this.$emit("update-data", res.data);
          this.currentSession.start_time = this.currentSession.end_time = "";
          this.arrSession.splice(0, this.arrSession.length);
          this.$toast.success("Saved Successfully");
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
form {
  margin: auto;
}
</style>
