<template>
  <div>
    <el-card>
      <div class="main-wfh row">
        <el-form
          class="bg-white px-4 text-info mb-2"
          label-width="200px"
          style="width: 100%"
        >
          <el-form-item label="Name">
            <el-input
              :value="currentUser.name"
              placeholder="Your User Name"
              disabled
            />
          </el-form-item>
          <el-form-item label="Days">
            <div>
              From
              <flat-pickr
                v-model="startDay"
                :config="{
                  altInput: true,
                  altFormat: 'd-m-Y',
                  dateFormat: 'Y-m-d',
                  locale: { firstDayOfWeek: 1 },
                }"
                class="mr-2 ml-2"
                placeholder="Select date"
                name="date"
                @input="getDays()"
              />
              To
              <flat-pickr
                v-model="endDay"
                :config="{
                  altInput: true,
                  altFormat: 'd-m-Y',
                  dateFormat: 'Y-m-d',
                  locale: { firstDayOfWeek: 1 },
                }"
                class="mr-2 ml-2"
                placeholder="Select date"
                name="date"
                @input="getDays()"
              />

              <div class="border-top rounded text-secondary">
                <div v-if="days.length > 0">
                  <table class="table">
                    <thead class="thead-light">
                      <tr>
                        <th scope="col" class="stt">No</th>
                        <th scope="col" class="date">Date</th>
                        <th scope="col" class="session">Session</th>
                        <th scope="col" class="lunch">Lunch</th>
                        <th scope="col" class="action">Action</th>
                      </tr>
                    </thead>
                    <tbody v-for="(item, index) in days" :key="item.startDay">
                      <tr>
                        <td>
                          <div class="text-center">
                            {{ index + 1 }}
                          </div>
                        </td>
                        <td>
                          <div class="text-center">
                            {{ formatDate(item.date) }}
                          </div>
                        </td>
                        <td>
                          <div class="text-center">
                            <el-checkbox
                              v-model="item.offMorning"
                              @change="changeTypeOff(item, $event)"
                            >
                              {{ formatSessionTime(item.date)[0] }} -
                              {{ formatSessionTime(item.date)[1] }}
                            </el-checkbox>
                            <el-checkbox
                              v-model="item.offAfternoon"
                              @change="changeTypeOff(item, $event)"
                            >
                              {{ formatSessionTime(item.date)[2] }} -
                              {{ formatSessionTime(item.date)[3] }}
                            </el-checkbox>
                          </div>
                        </td>
                        <td>
                          <div class="text-center">
                            <input
                              type="checkbox"
                              class="form-check-input"
                              v-on:click="changeLunch(item)"
                            />
                          </div>
                        </td>
                        <td>
                          <div class="text-center">
                            <font-awesome-icon
                              v-on:click="removeDay(item)"
                              class="fa-fw"
                              :icon="['fas', 'trash']"
                            />
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </el-form-item>
          <el-form-item label="Reason">
            <el-input
              type="textarea"
              :rows="2"
              v-model="reason"
              form="leaves"
              placeholder="Tell me your reasons"
            />
          </el-form-item>
          <div class="d-flex justify-content-end">
            <div>
              <el-button
                @click="openDialog"
                :disabled="!days.length"
                type="primary"
              >
                SEND
              </el-button>
            </div>
            <router-link to="/workfromhome/" class="ml-3">
              <el-button type="danger"> CANCEL </el-button>
            </router-link>
          </div>
        </el-form>
        <el-dialog
          :visible.sync="dialog"
          title="WFH Request"
          class="font-weight-bold"
        >
          <div class="justify-content-between">
            <div><strong>User Name :</strong> {{ currentUser.name }}</div>
            <br />
            <el-table
              :data="days"
              header-cell-class-name="bg-header-table"
              border
            >
              <el-table-column prop="date" label="Day WFH">
                <template slot-scope="scope">
                  {{ formatDate(scope.row.date) }}
                </template>
              </el-table-column>
              <el-table-column prop="type" label="Session"></el-table-column>
              <el-table-column prop="lunch" label="Lunch">
                <template slot-scope="scope">
                  <div v-if="scope.row.lunch === true">Yes</div>
                  <div v-else>No</div>
                </template>
              </el-table-column>
            </el-table>
            <br />
            <div>
              <strong>Total WFH Days : </strong> {{ getNumberDayOffs() }}
            </div>
            <br />
            <div><strong>Reason :</strong> {{ this.reason }}</div>
          </div>

          <div id="user-lunch-modal-bottom">
            <div id="modify-button">
              <div class="row">
                <el-button
                  class="mt-3 mx-auto col-4"
                  type="danger"
                  @click="closeDialog"
                >
                  Cancel
                </el-button>
                <el-button
                  class="mt-3 mx-auto col-4"
                  type="primary"
                  :disabled="isSending || !days.length"
                  @click="submit()"
                >
                  Send
                </el-button>
              </div>
            </div>
          </div>
        </el-dialog>
      </div>
    </el-card>
  </div>
</template>
<script>
import "vue-cal/dist/vuecal.css";
import flatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import RequestWFHService from "@/services/wfh_management/request_wfh/request_wfh.services";
import officeSessionService from "@/services/office/office.session";
import moment from "moment";
import { mapGetters, mapState } from "vuex";

export default {
  name: "AddNewWFHRequest1",
  middleware: "authentication",
  components: {
    flatPickr,
  },
  computed: {
    ...mapState("user", ["currentUser"]),
    ...mapGetters({
      showNotification: "showNotification",
    }),
  },
  data() {
    return {
      days: [],
      holidays: [],
      startDay: null,
      endDay: null,
      reason: "",
      leaveDayNumber: "",
      remainDay: 0,
      currentDaysOff: 0,
      month: moment().year(),
      dialog: false,
      sessionTimes: [],
      profileID: "",
      year: new Date().getFullYear(),
      totalLeaveCheck: false,
      officeID: "",
      isSending: false,
    };
  },

  created: async function () {
    await this.getSessionTimes();
  },
  methods: {
    changeTypeOff(item) {
      let index = this.days.indexOf(
        this.days.find((i) => i.date === item.date)
      );
      let newType = "All day";
      if (item.offMorning === false && item.offAfternoon === false) {
        this.removeDay(item);
      } else {
        if (item.offMorning === true && item.offAfternoon === false) {
          newType =
            String(this.formatSessionTime(item.date)[0]) +
            "-" +
            String(this.formatSessionTime(item.date)[1]);
        } else if (item.offMorning === false && item.offAfternoon === true) {
          newType =
            String(this.formatSessionTime(item.date)[2]) +
            "-" +
            String(this.formatSessionTime(item.date)[3]);
        }
        this.days = [
          ...this.days.slice(0, index),
          {
            ...item,
            type: newType,
          },
          ...this.days.slice(index + 1),
        ];
      }
    },
    changeLunch(item) {
      let index = this.days.indexOf(
        this.days.find((i) => i.date === item.date)
      );
      this.days = [
        ...this.days.slice(0, index),
        {
          ...item,
          lunch: !item.lunch,
        },
        ...this.days.slice(index + 1),
      ];
    },

    removeDay: function (item) {
      const index = this.days.indexOf(
        this.days.find((i) => i.date === item.date)
      );
      if (index > -1) {
        this.days = [
          ...this.days.slice(0, index),
          ...this.days.slice(index + 1),
        ];
      }
    },

    submit: async function () {
      this.isSending = true;
      let listDates = [];
      this.days.forEach((item) =>
        listDates.push({
          ...item,
          date: item.date.toISOString().slice(0, 10),
        })
      );
      const data = {
        reason: this.reason,
        date: listDates,
        wfh_total: this.getNumberDayOffs(),
      };
      try {
        const response = await RequestWFHService.create(data);
        if (response.status === 201) {
          this.$nextTick(() => {
            this.$toast.success("Sent Successfully");
          });
          this.isSending = false;
          listDates = [];
          this.$router.push("/workfromhome");
        }
      } catch (e) {
        let error = e.response?.data.error
          ? e.response.data.error
          : "Sent Failed";
        this.$toast.error(error);
        this.dialog = false;
        this.isSending = false;
      }
    },

    datePicker: function (date) {
      const holiday = this.holidays.filter(
        (item) =>
          item.start_date <= moment(date).format("YYYY-MM-DD") &&
          item.end_date >= moment(date).format("YYYY-MM-DD")
      );
      if (holiday.length > 0) {
        return true;
      }
      return date.getDay() === 0 || date.getDay() === 6;
    },

    datePickerUnEnable: function (date) {
      date = true;
      return date;
    },

    datePickerEnable: function (date) {
      date = false;
      return date;
    },

    getDays() {
      this.days = [];
      if (this.startDay !== null && this.endDay !== null) {
        let endDay = new Date(this.endDay);
        let start = new Date(this.startDay);
        for (; start <= endDay; ) {
          const holiday = this.holidays.filter(
            (item) =>
              item.start_date <= moment(start).format("YYYY-MM-DD") &&
              item.end_date >= moment(start).format("YYYY-MM-DD")
          );
          if (
            start.getDay() !== 0 &&
            start.getDay() !== 6 &&
            holiday.length === 0
          ) {
            const date = new Date(
              start.getFullYear(),
              start.getMonth(),
              start.getDate(),
              12,
              0
            );
            this.days.push({
              date: date,
              type: "All day",
              lunch: false,
              offMorning: true,
              offAfternoon: true,
            });
          }
          start.setDate(start.getDate() + 1);
        }
      }
      if (this.days.length > 0) this.totalLeaveCheck = true;
    },

    getNumberDayOffs() {
      let number = 0;
      if (this.totalLeaveCheck) {
        this.days.forEach((item) => {
          if (item.type === "All day") number += 1;
          else number += 0.5;
        });
        return number;
      }
    },

    openDialog() {
      this.dialog = true;
    },

    closeDialog() {
      this.dialog = false;
    },

    formatDate(value) {
      if (value) {
        return moment(String(value)).format("MM-DD-YYYY");
      }
    },

    async getSessionTimes() {
      this.sessionTimes = await officeSessionService.getSessionTimesByProfile();
    },

    formatSessionTime(value) {
      if (value) {
        const data = this.sessionTimes.filter(
          (data) => data.dow === new Date(value).getDay() - 1
        );
        const sessionTime = [];
        if (data.length > 0) {
          for (const day in data) {
            sessionTime.push(data[day].start_time.slice(0, 5));
            sessionTime.push(data[day].end_time.slice(0, 5));
          }
          return sessionTime;
        }
      }
      return [];
    },

    handleDataAPI(dataAPI) {
      const newData = {
        data: [],
      };
      dataAPI.forEach((item) => {
        newData.data.push(item);
      });
      return newData;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./addNewWFHRequest.scss";
</style>
