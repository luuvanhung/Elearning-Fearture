<template>
  <div>
    <el-card>
      <div class="main-leaves row">
        <el-form
          class="bg-white px-4 text-info mb-2"
          label-width="200px"
          style="width: 100%"
        >
          <el-form-item label="Name">
            <el-input
              v-model="userName"
              placeholder="Your User Name"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item label="Available leave days">
            <el-input
              v-model="leaveDayNumber"
              placeholder="Leave days remaining"
              disabled
            ></el-input>
          </el-form-item>
          <el-form-item label="Types">
            <el-select v-model="typeLeave" @change="getTypeLeave">
              <div v-for="typeOff in listTypeOff" v-bind:key="typeOff.id">
                <div class="background">
                  <strong class="ml-3"> {{ typeOff.name }} </strong>
                </div>
                <el-option
                  v-for="typeOffDetail in typeOff.data"
                  :key="typeOffDetail.index"
                  :value="typeOffDetail.id"
                  :label="typeOffDetail.name"
                  v-bind:disabled="leaveDayNumber === 0"
                >
                  {{ typeOffDetail.name }}
                  {{
                    Number(typeOffDetail.days) !== maxDayOff
                      ? `(maximum: ${typeOffDetail.days} days)`
                      : ""
                  }}
                </el-option>
              </div>
            </el-select>
            <div v-if="typeLeave !== ''" class="mt-2">
              <el-table
                stripe
                header-cell-class-name="bg-header-table"
                border
                style="width: 100%"
                :data="typeLeaveTable"
              >
                <el-table-column
                  prop="name"
                  label="Name"
                  width="200"
                  align="center"
                ></el-table-column>
                <el-table-column
                  prop="is_count"
                  label="Counted"
                  width="80"
                  align="center"
                >
                  <template slot-scope="scope">
                    <div v-if="scope.row.is_count === true">Yes</div>
                    <div v-else>No</div>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="days"
                  label="Limit Days"
                  width="100"
                  align="center"
                  v-if="maxLeaveDays !== maxDayOff"
                ></el-table-column>
                <el-table-column
                  prop="descriptions"
                  label="Descriptions"
                  align="center"
                >
                  <template slot-scope="scope">
                    <div class="dont-break-out">
                      {{ scope.row.descriptions }}
                    </div>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="approval_title_name"
                  label="Approval Title Suggestion"
                  width="300"
                  align="center"
                ></el-table-column>
              </el-table>
              <div class="mt-2">
                You have {{ totalTypeOffLeaves }} date off using this request
              </div>
            </div>
          </el-form-item>
          <div class="d-flex flex-row">
            <el-form-item label="Approver">
              <el-select
                v-model="assignApproval"
                filterable
                remote
                :remote-method="remoteMethod"
              >
                <div v-for="group in listData" :key="group.title.title">
                  <div class="background">
                    <div class="ml-3">{{ group.title.title }}</div>
                  </div>
                  <el-option
                    v-if="group.profiles.length === 0"
                    :value="NO_DATA"
                    :label="NO_DATA"
                    disabled
                  ></el-option>

                  <el-option
                    v-for="member in group.profiles"
                    :key="member.index"
                    :value="member.id"
                    :label="member.profile.name"
                  >
                    <span style="float: left">{{ member.profile.name }}</span>
                    <span style="float: right; color: #8c8c8c; font-size: 11px">
                      {{ member.profile.personal_email }}
                    </span>
                  </el-option>
                </div>
              </el-select>
            </el-form-item>
            <div class="align-self-start">
              <el-radio-group v-model="searchByNameOrTitle">
                <el-radio-button label="Title" />
                <el-radio-button label="Name" />
              </el-radio-group>
            </div>
          </div>
          <el-form-item label="Days" v-if="isValidDate">
            <div>
              From
              <flat-pickr
                v-model="startDay"
                :config="{
                  altInput: true,
                  altFormat: 'd-m-Y',
                  minDate: this.joinDate,
                  dateFormat: 'Y-m-d',
                  locale: { firstDayOfWeek: 1 },
                  disable: this.disable(),
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
                  minDate: this.startDay,
                  locale: { firstDayOfWeek: 1 },
                  disable: this.disable(),
                }"
                class="mr-2 ml-2"
                placeholder="Select date"
                name="date"
                @input="getDays()"
              />

              <div class="border-top rounded text-secondary">
                <div v-if="days.length > 0">
                  <table class="table">
                    <caption></caption>
                    <thead class="thead-light">
                      <tr>
                        <th scope="col" class="stt">No</th>
                        <th scope="col" class="date">Date</th>
                        <th scope="col" class="session">Session</th>
                        <th scope="col" class="lunch">Lunch</th>
                        <th scope="col" class="action">Action</th>
                      </tr>
                    </thead>
                    <tbody
                      v-for="(item, index) in paginateDayOffs()"
                      :key="index"
                    >
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
                              v-model="item.lunch"
                              :disabled="item.disableEditLunch"
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
                  <div class="d-flex justify-content-center mt-2">
                    <el-pagination
                      background
                      layout="prev, pager, next"
                      :page-size="pageSize"
                      :page-count="totalPage"
                      :current-page="page"
                      @current-change="setPage"
                    >
                    </el-pagination>
                  </div>
                </div>
              </div>
              <div v-if="totalLeaveCheck">
                Total Leave Days : {{ numberDaysOff }}
              </div>
              <div v-if="errorRequest">
                <div class="text-danger">
                  {{ errorMessage }}
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
              maxlength="256"
            />
          </el-form-item>
          <div class="d-flex justify-content-end">
            <div>
              <el-button
                @click="openDialog"
                type="primary"
                :disabled="sendCheck || assigned()"
              >
                SEND
              </el-button>
            </div>

            <router-link to="/leaves/" class="ml-3">
              <el-button type="danger"> CANCEL </el-button>
            </router-link>
          </div>
        </el-form>
        <el-dialog
          :visible.sync="dialog"
          title="Leave Request"
          class="font-weight-bold"
        >
          <div class="justify-content-between">
            <div><strong>User Name :</strong> {{ this.userName }}</div>
            <br />
            <div>
              <strong>Type :</strong>
              {{
                this.tempListTypeOff.find((item) => item.id === this.typeLeave)
                  ? this.tempListTypeOff.find(
                      (item) => item.id === this.typeLeave
                    ).name
                  : ""
              }}
            </div>
            <br />
            <el-table
              :data="paginateDayOffs()"
              header-cell-class-name="bg-header-table"
              border
            >
              <el-table-column prop="date" label="Day Off">
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
            <div class="d-flex justify-content-center mt-2">
              <el-pagination
                background
                layout="prev, pager, next"
                :page-size="pageSize"
                :page-count="totalPage"
                :current-page="page"
                @current-change="setPage"
              >
              </el-pagination>
            </div>
            <br />
            <div><strong>Total Leave Days : </strong> {{ numberDaysOff }}</div>
            <br />
            <div><strong>Reason :</strong> {{ this.reason }}</div>
          </div>

          <div id="user-lunch-modal-bottom">
            <div id="modify-button">
              <div class="row">
                <el-button
                  class="mt-3 mx-auto col-4"
                  type="primary"
                  :disabled="isSending"
                  @click="submit"
                >
                  Send
                </el-button>
                <el-button
                  class="mt-3 mx-auto col-4"
                  type="danger"
                  @click="closeDialog"
                >
                  Cancel
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
import RequestOffService from "@/services/leave_management/request_off/request_off.services";
import DateOffService from "@/services/leave_management/request_off/date_off.services";
import holidayServices from "@/services/office/holiday.service";
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";
import RemainLeaveService from "@/services/leave_management/remain_leave/remain_leave.services";
import officeSessionService from "@/services/office/office.session";
import moment from "moment";
import { MAX_DAY_OFF, AFTERNOON, MORNING, ALL_DAY } from "@/const/leaveDays";
import "vue-cal/dist/vuecal.css";
import flatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import { mapGetters } from "vuex";
import { formatDate } from "@/utils/time";
import _ from "lodash";
import { ROLES } from "@/const/roles";
import UserLunchService from "@/services/company_calendar/user-lunch";
const NO_DATA = "No data";

export default {
  name: "AddNewRequest",
  middleware: "authentication",
  components: {
    flatPickr,
  },
  data() {
    return {
      days: [],
      holidays: [],
      userName: "",
      startDay: null,
      endDay: null,
      joinDate: null,
      typeLeave: "",
      typeLeaveTable: [],
      listTypeOff: [],
      tempListTypeOff: [],
      reason: "",
      leaveDayNumber: "",
      assignApproval: "",
      approver: "",
      remainDay: 0,
      annualLeave: 0,
      annualLeaveLastYear: 0,
      currentDaysOff: 0,
      month: moment().year(),
      dialog: false,
      sessionTimes: [],
      profileID: "",
      year: new Date().getFullYear(),
      totalTypeOffLeaves: 0,
      maxLeaveDays: 1,
      sendCheck: true,
      totalLeaveCheck: false,
      errorRequest: false,
      isCount: true,
      officeID: "",
      monthExpiredAnnualLeave: 0,
      isSending: false,
      maxDayOff: MAX_DAY_OFF,
      currentTypeOffLeave: null,
      numberDaysOff: 0,
      profileGroupTitles: [],
      listData: [],
      searchByNameOrTitle: "Title",
      dateOffData: [],
      errorMessage: "",
      page: 1,
      pageSize: 10,
      totalPage: 1,
      dateHadLunch: [],
      NO_DATA,
    };
  },
  computed: {
    ...mapGetters({
      showNotification: "showNotification",
      allUsersExcludeCurrentUser: "user/allUsersExcludeCurrentUser",
      listTitle: "title/listTitle",
    }),
    isValidDate() {
      if (this.currentTypeOffLeave != null) {
        if (
          this.currentTypeOffLeave.is_company_pay &&
          this.currentTypeOffLeave.is_insurance_pay === false
        ) {
          return (
            (this.isCount && this.currentDaysOff > 0) || this.isCount === false
          );
        }
        if (
          this.currentTypeOffLeave.is_insurance_pay &&
          this.currentTypeOffLeave.is_company_pay === false
        ) {
          return (
            (this.isCount && this.totalTypeOffLeaves < this.maxLeaveDays) ||
            this.isCount === false
          );
        } else {
          return true;
        }
      } else {
        return false;
      }
    },
  },
  created: async function () {
    await RemainLeaveService.getRetrieveDate().then((res) => {
      this.annualLeave = res.data.annual_leave;
      this.currentDaysOff = res.data.current_days_off;
      this.annualLeaveLastYear = res.data.annual_leave_last_year;
      this.userName = res.data.profile.name;
      this.profileID = res.data.profile.id;
      this.officeID = res.data.profile.office;
      this.joinDate = new Date(res.data.profile.join_date).toISOString();
      this.monthExpiredAnnualLeave = res.data.month;
      this.getTotalLeaveDays();
    });
    await holidayServices.get(this.officeID).then((res) => {
      this.holidays = res.data.results;
    });
    await TypeOffAdminServices.getTypeOffUser().then((res) => {
      this.tempListTypeOff = res.data;
      this.listTypeOff = this.handleDataAPI(res.data);
    });
    await DateOffService.getDateOffUserEffect().then((resData) => {
      this.dateOffData = resData;
      this.handleDateOffData();
    });
    await this.getSessionTimes();
    await this.profileGroupTitle();
    const res = await UserLunchService.get();
    if (res.data) {
      const entries = res.data.map((lunch) => [lunch.date, true]);
      this.dateHadLunch = Object.fromEntries(entries);
    }
  },
  methods: {
    formatDate,
    remoteMethod(query) {
      const keyword = query.toLowerCase();
      if (this.searchByNameOrTitle === "Title") {
        this.listData = this.profileGroupTitles.filter((item) => {
          return item.title.title.toLowerCase().includes(keyword);
        });
      } else {
        this.listData = this.profileGroupTitles.map((item) => {
          return {
            title: item.title,
            profiles: item.profiles.filter((profile) => {
              return profile.profile.name.toLowerCase().includes(keyword);
            }),
          };
        });
      }
    },

    profileGroupTitle(titleSuggest = ROLES.TEAM_LEADER) {
      this.profileGroupTitles = [];
      let allUsers = [...this.allUsersExcludeCurrentUser];
      let allTitles = [...this.listTitle];
      allTitles = allTitles.filter((title) => {
        return title.title !== titleSuggest;
      });

      let groupNoneTitle = {
        title: {
          title: "Other",
        },
        profiles: [],
      };
      let groupSuggestTitle = {
        title: {
          title: titleSuggest,
        },
        profiles: [],
      };

      for (let title of allTitles) {
        let groupTitle = {
          title: title,
          profiles: [],
        };

        for (let user of allUsers) {
          if (user.title.length <= 0) {
            groupNoneTitle.profiles.push(user);
            this.removeItem(allUsers, user);
          }
          if (user.title.some((item) => item.title === titleSuggest)) {
            if (!groupSuggestTitle.profiles.includes(user)) {
              groupSuggestTitle.profiles.push(user);
            }
          }
          if (user.title.some((item) => item.title === title.title)) {
            groupTitle.profiles.push(user);
          }
        }

        this.profileGroupTitles.push(groupTitle);
      }

      this.profileGroupTitles.unshift(groupSuggestTitle);
      this.profileGroupTitles.push(groupNoneTitle);
      this.listData = this.profileGroupTitles;
    },

    removeItem(array, item) {
      return array.splice(array.indexOf(item), 1);
    },

    disable() {
      if (this.typeLeave !== "") {
        if (this.tempListTypeOff.find((item) => item.id === this.typeLeave)) {
          return [this.datePicker];
        } else {
          return [this.datePickerEnable];
        }
      } else {
        return [this.datePickerUnEnable];
      }
    },

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
      this.handleSendCheckButton();
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
        this.handleSendCheckButton();
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
        type_id: this.typeLeave,
        reason: this.reason,
        date: listDates,
        total_leaves: this.numberDaysOff,
        approver: this.approver,
        assign_approval: this.assignApproval,
      };

      await RequestOffService.create(data)
        .then(async (response) => {
          if (response.status === 201) {
            await RemainLeaveService.getRetrieveDate().then((res) => {
              this.annualLeave = res.data.annual_leave;
              this.currentDaysOff = res.data.current_days_off;
              this.annualLeaveLastYear = res.data.annual_leave_last_year;
              this.userName = res.data.profile.name;
              this.joinDate = new Date(
                res.data.profile.join_date
              ).toISOString();
              this.monthExpiredAnnualLeave = res.data.month;
              this.getTotalLeaveDays();
            });
            this.$nextTick(() => {
              this.$toast.success("Sent Successfully");
            });
          }
          this.isSending = false;
          listDates = [];
          await this.$router.push("/leaves");
        })
        .catch((e) => {
          let error = "Sent Failed";
          if (e.response && e.response.data.error !== "") {
            error = e.response.data.error;
          }
          this.$toast.error(error);
        });
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

    datePickerUnEnable: function (date = true) {
      return date;
    },

    datePickerEnable: function (date = false) {
      return date;
    },

    getTotalLeaveDays() {
      this.leaveDayNumber = `${this.currentDaysOff} days`;
    },

    getDays() {
      this.days = [];
      this.getTotalLeaveDays();
      this.remainDay = this.currentDaysOff;
      if (this.startDay !== null && this.endDay !== null) {
        let endDay = new Date(this.endDay);
        let start = new Date(this.startDay);
        while (start <= endDay) {
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
            const dateFormat = moment(date).format("YYYY-MM-DD");
            const today = new Date();
            const todayFormat = moment(today).format("YYYY-MM-DD");
            const hasLunch = !!this.dateHadLunch[dateFormat];
            const disableEditLunch =
              today.getHours() >= 9
                ? dateFormat <= todayFormat
                : dateFormat < todayFormat;
            this.days.push({
              date,
              type: "All day",
              lunch: hasLunch,
              disableEditLunch,
              offMorning: true,
              offAfternoon: true,
            });
          }
          start.setDate(start.getDate() + 1);
        }
      }
      if (this.days.length > 0) this.totalLeaveCheck = true;
      this.isSending = false;
      this.handleSendCheckButton();
    },

    handleSendCheckButton() {
      this.getNumberDayOffs();
      if (this.checkOverLapDateOff() && !this.sendCheck) {
        this.sendCheck = true;
        this.errorRequest = this.sendCheck;
        this.errorMessage =
          "There was a request for this date! Please choose another.";
      }
      this.totalPage = Math.ceil(this.days.length / this.pageSize);
      this.errorMessage = this.errorRequest ? this.errorMessage : "";
    },

    checkOverLapDateOff() {
      for (let i = 0; i < this.dateOffData.length; i++) {
        for (let j = 0; j < this.days.length; j++) {
          if (
            this.formatDate(this.days[j].date).valueOf() ===
            this.dateOffData[i].date.valueOf()
          ) {
            if (
              this.days[j].offAfternoon === this.dateOffData[i].offAfternoon ||
              this.days[j].offMorning === this.dateOffData[i].offMorning
            )
              return true;
          }
        }
      }
      return false;
    },

    getNumberDayOffs() {
      let number = 0;
      if (this.totalLeaveCheck) {
        this.days.forEach((item) => {
          if (item.type === "All day") number += 1;
          else number += 0.5;
        });
        this.sendCheck = true;
        if (
          this.currentTypeOffLeave.is_company_pay &&
          this.currentTypeOffLeave.is_insurance_pay === false
        ) {
          if (this.isCount) {
            this.sendCheck = !(
              number <= this.maxLeaveDays && number <= this.currentDaysOff
            );
          } else {
            this.sendCheck = number > this.maxLeaveDays;
          }
        }
        if (
          this.currentTypeOffLeave.is_insurance_pay &&
          this.currentTypeOffLeave.is_company_pay === false
        ) {
          if (this.isCount) {
            this.sendCheck =
              number + this.totalTypeOffLeaves > this.maxLeaveDays;
          } else {
            this.sendCheck = number > this.maxLeaveDays;
          }
        }
        if (
          this.currentTypeOffLeave.is_company_pay === 1 &&
          this.currentTypeOffLeave.is_insurance_pay === 1
        ) {
          if (this.isCount) {
            //tinh available and current
            this.sendCheck = !(
              number <= this.maxLeaveDays &&
              number + this.totalTypeOffLeaves <= this.maxLeaveDays &&
              number <= this.currentDaysOff
            );
          } else {
            //k tinh available and k check limit
            this.sendCheck = number > this.maxLeaveDays;
          }
        } else if (
          this.currentTypeOffLeave.is_company_pay === 0 &&
          this.currentTypeOffLeave.is_insurance_pay === 0
        ) {
          this.sendCheck = number > this.maxLeaveDays;
        }
        this.errorMessage = "Reach maximum days. Please choose another.";
        this.errorRequest = this.sendCheck;
        this.numberDaysOff = number;
      }
    },

    openDialog() {
      if (this.days.length === 0) {
        this.$toast.error("No days off yet");
      } else if (
        this.currentTypeOffLeave.is_company_pay &&
        this.isCount === true &&
        this.numberDaysOff > this.remainDay
      ) {
        this.$toast.error("Total leave days can not more Available leave days");
      } else {
        this.page = 1;
        this.dialog = true;
      }
    },

    closeDialog() {
      this.dialog = false;
    },

    async getTypeLeave() {
      if (this.typeLeave !== "") {
        const tempTypeLeave = this.tempListTypeOff.find(
          (item) => item.id === this.typeLeave
        );
        this.profileGroupTitle(tempTypeLeave.approval_title_name);
        this.currentTypeOffLeave = tempTypeLeave;
        this.typeLeaveTable = [tempTypeLeave];
        this.approver = tempTypeLeave.approval_title;
        this.maxLeaveDays = tempTypeLeave.days;
        this.isCount = tempTypeLeave.is_count;
        const res = await RequestOffService.countTotalTypeOffDays(
          this.profileID,
          this.typeLeave,
          this.year
        );
        this.totalTypeOffLeaves = res.total_leaves;
        this.isSending = false;
      }
      this.handleSendCheckButton();
    },

    async getSessionTimes() {
      this.sessionTimes = await officeSessionService.getSessionTimesByProfile();
    },

    formatSessionTime(value) {
      if (value) {
        const data = this.sessionTimes.filter(
          (item) => item.dow === new Date(value).getDay() - 1
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
      const uniqueGroup = _.uniqBy(dataAPI, "leave_type_group");
      return uniqueGroup.map((typeOff) => {
        const newData = {
          id: typeOff.id,
          group: typeOff.leave_type_group,
          name: typeOff.name_type,
          data: [],
        };
        dataAPI.forEach((item) => {
          if (item.leave_type_group === typeOff.leave_type_group) {
            newData.data.push(item);
          }
        });
        return newData;
      });
    },

    handleDateOffData() {
      this.dateOffData.forEach((data) => {
        if (data.type === MORNING) {
          data.offMorning = true;
          data.offAfternoon = false;
        }
        if (data.type === AFTERNOON) {
          data.offMorning = false;
          data.offAfternoon = true;
        }
        if (data.type === ALL_DAY) {
          data.offAfternoon = true;
          data.offMorning = true;
        }
      });
    },

    assigned() {
      return this.assignApproval.trim() === "";
    },

    setPage(page) {
      this.page = page;
    },

    paginateDayOffs() {
      // human-readable page numbers usually start with 1, so we reduce 1 in the first argument
      return this.days.slice(
        (this.page - 1) * this.pageSize,
        this.page * this.pageSize
      );
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./addNewRequest.scss";
</style>
