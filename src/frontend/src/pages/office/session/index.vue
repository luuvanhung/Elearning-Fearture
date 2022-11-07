<template>
  <div>
    <el-row :gutter="24">
      <el-col :xl="3" :lg="4" :sm="12" v-for="day in daysOfWeek" :key="day.dow">
        <el-card shadow="always" class="text-center mt-2">
          <h3>{{ day.name }}</h3>
          <div v-if="typeof sessions[day.dow] !== 'undefined'">
            <div
              v-for="item in sessions[day.dow].data"
              :key="item.id"
              :id="!showAddSession ? 'session-item' : 'session-item-unHover'"
            >
              <div @click="editData(item)">
                {{ item.start_time.slice(0, 5) }} -
                {{ item.end_time.slice(0, 5) }}
              </div>
              <img
                @click="deleteData(day.dow, item.id)"
                :src="require('@/static/images/IconCancel.svg')"
                class="img-delete"
              />
            </div>
          </div>
          <div class="d-flex justify-content-end" v-if="!showAddSession">
            <img
              @click="addData(day)"
              :src="require('@/static/images/IconAdd.svg')"
              class="img-add"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog
      :visible.sync="dialogAdd"
      :before-close="handleClose"
      destroy-on-close
    >
      <addSession
        :sessions="sessions"
        :dayAddSession="dayAddSession"
        @update-data="emitData"
      />
    </el-dialog>
    <el-dialog
      :visible.sync="dialogEdit"
      :before-close="handleClose"
      destroy-on-close
    >
      <edit-session :sessionEdit="sessionEdit" />
    </el-dialog>
  </div>
</template>

<script>
import addSession from "./addSession";
import Session from "@/services/office/office.session";
import editSession from "./editSession";
import { daysOfWeek } from "@/const/daysOfWeek";
import { handleDataAPI } from "./utils";

export default {
  name: "session",
  components: { addSession, editSession },
  props: {
    showAddSession: Boolean,
  },
  data() {
    return {
      dialogAdd: false,
      dialogEdit: false,
      dialogDelete: false,
      sessionEdit: "",
      sessions: [],
      sessionUpdate: [],
      daysOfWeek,
      dayAddSession: "",
    };
  },
  created() {
    this.getData();
  },
  methods: {
    addData(day) {
      this.dialogAdd = true;
      this.dayAddSession = day;
    },
    emitData(data) {
      this.sessionUpdate.push(data);
      this.sessions = handleDataAPI(this.sessionUpdate);
    },
    async getData() {
      const res = await Session.getAll(this.$route.params.id);
      this.sessionUpdate = res.data;
      this.sessions = handleDataAPI(res.data);
    },
    async deleteData(dayDow, session_id) {
      try {
        const res = await Session.deleteById(session_id);
        if (res.status === 204) {
          const indexSessions = this.sessions[dayDow].data.findIndex(
            (e) => e.id === session_id
          );
          const indexSessionUpdate = this.sessionUpdate.findIndex(
            (e) => e.id === session_id
          );
          this.sessions[dayDow].data.splice(indexSessions, 1);
          this.sessionUpdate.splice(indexSessionUpdate, 1);
          this.$toast.success("Deleted Successfully");
        }
      } catch (err) {
        const myJSX = <span>{err.response.data.detail}</span>;
        this.$toast.error(myJSX);
      }
    },
    editData(session) {
      this.sessionEdit = session;
      this.dialogEdit = true;
    },
    handleClose(done) {
      this.$confirm("Are you sure to close this dialog?")
        .then(() => {
          done();
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
@import "style.scss";

.img-add {
  width: 20px;
}

#session-item {
  color: #707070;
  margin: 10% auto;
  box-shadow: 0 2px 4px #c6c6c6;
  padding: 5%;
  width: auto;
  border-radius: 5px;
  cursor: pointer;
}

#session-item .img-delete {
  display: none;
}

#session-item:hover {
  background: #def3f4;
  color: #707070;
  position: relative;
}

#session-item:hover .img-delete {
  display: inline-block;
  position: absolute;
  top: 5px;
  right: 10px;
  width: 10px;
}

#session-item-unHover {
  color: #707070;
  margin: 10% auto;
  box-shadow: 0 2px 4px #c6c6c6;
  padding: 5%;
  width: auto;
  border-radius: 5px;
  pointer-events: none;
}

#session-item-unHover .img-delete {
  display: none;
}

button {
  width: 130px;
  height: 45px;
  color: #ffffff;
  background: #25c9d0;
  font-weight: bold;
  font-family: "Times New Roman", Times, serif;
  border: none;
  font-size: 16px;
  cursor: pointer;
  border-radius: 10px;
}
</style>
