<template>
  <div class="my-2">
    <div class="bg-light">
      <el-col :xs="24" :sm="24" :md="8" :lg="4" :xl="4" class="pr-2">
        <el-row style="height: 60px"></el-row>
        <el-row>
          <div>
            <div class="text-center">
              <el-button
                type="danger"
                round
                class="btn-calendar"
                disabled
                style="background-color: #f05252"
                >Calendar Type</el-button
              >
            </div>
            <br />
            <div class="text-center">
              <el-checkbox
                v-model="leave"
                label="Show Leave"
                @change="checkBox"
              >
              </el-checkbox>
            </div>
            <div class="text-center">
              <el-checkbox
                v-model="lunch"
                label="Show Lunch"
                @change="checkBox"
              >
              </el-checkbox>
            </div>
          </div>
          <el-divider class="mr-2"
            ><em class="el-icon-star-on"></em
          ></el-divider>
          <div>
            <div class="text-center mb-3">
              <el-button
                type="primary"
                round
                class="btn-calendar"
                disabled
                style="background-color: #25c9d0"
                >Today Information</el-button
              >
            </div>
            <div class="description-detail mt-1">
              <div class="box-description-leave ml-5"></div>
              <small class="ml-4"> {{ leavesToday }} - Leave</small>
            </div>
            <div class="description-detail mt-1">
              <div class="box-description-lunch ml-5"></div>
              <small class="ml-4">{{ lunchesToday }} - Lunch</small>
            </div>
            <div class="description-detail mt-1">
              <div class="box-description-veggie ml-5"></div>
              <small class="ml-4">{{ veggiesToday }} - Veggie</small>
            </div>
          </div>
          <el-divider class="mr-2"
            ><em class="el-icon-star-on"></em
          ></el-divider>
          <div>
            <div class="text-center mb-3">
              <el-button
                round
                type="warning"
                class="btn-calendar"
                disabled
                style="background-color: #feab30"
                >Descriptions</el-button
              >
            </div>
            <div class="description-detail mt-1">
              <div class="box-description-lunar ml-5"></div>
              <small class="ml-3">Lunar Day</small>
            </div>
            <div class="description-detail mt-1">
              <div class="box-description-current ml-5"></div>
              <small class="ml-3">Current Day</small>
            </div>
          </div>
        </el-row>
      </el-col>
      <el-col :xs="24" :sm="24" :md="16" :lg="20" :xl="20">
        <el-card class="mp-3">
          <FullCalendar ref="fullCalendar" :options="calendarOptions" />
        </el-card>
      </el-col>
      <el-dialog
        :visible.sync="dialogDetail"
        :title="selectedEvent.title"
        max-width="400"
      >
        <el-card v-if="selectedEvent.has_veggie != null">
          <el-row class="mb-3">
            <el-col :span="16">
              <el-input
                placeholder="Search by name or email"
                v-model="searchProfile"
                style="width: 50%"
              ></el-input>
            </el-col>
            <restricted-view :scopes="['user_lunch:edit_all_user_lunch']">
              <el-col :span="4">
                <el-button
                  type="danger"
                  :disabled="listUserLunchUpdate.length === 0"
                  @click="dialogConfirmDelete = true"
                >
                  Delete
                </el-button>
              </el-col>
              <el-col :span="4">
                <el-button
                  type="primary"
                  :disabled="
                    listUserLunchUpdate.length === 0 || !isDateLunarDay
                  "
                  @click="updateVeggieUserLunch()"
                >
                  <span v-if="selectedEvent.has_veggie"> Cancel Veggie </span>
                  <span v-else> Update Veggie </span>
                </el-button>
              </el-col>
            </restricted-view>
          </el-row>
          <el-table
            :data="dataTable"
            style="width: 100%"
            @selection-change="changeListUserLunchUpdate"
          >
            <el-table-column type="index" label="No." width="50">
            </el-table-column>
            <restricted-view :scopes="['user_lunch:edit_all_user_lunch']">
              <el-table-column type="selection" width="50"> </el-table-column>
            </restricted-view>
            <el-table-column label="Name" prop="profile.name">
              <template v-slot="scope">
                {{ scope.row.profile.name }}
              </template>
            </el-table-column>
            <el-table-column
              label="Personal email"
              prop="profile.personal_email"
            >
              <template v-slot="scope">
                {{ scope.row.profile.personal_email }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        <el-card v-else>
          <div v-for="(item, index) in selectedEvent.detail" :key="index">
            {{ index + 1 }} - {{ item.name }} - {{ item.typeOff }} -
            {{ item.timeType }}
          </div>
        </el-card>
      </el-dialog>
      <el-dialog :visible.sync="dialogConfirmDelete" max-width="400">
        <h2 class="text-center text-danger">
          Do you want to delete the lunches of these employees at
          {{ selectedEvent.start }}?
        </h2>
        <div class="mt-3 text-center">
          <el-button type="danger" @click="deleteUserLunch()">
            Delete
          </el-button>
          <el-button type="info" @click="dialogConfirmDelete = false">
            Cancel
          </el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import "vue-cal/dist/vuecal.css";
import CalendarAdminServices from "@/services/company_calendar/company_calendar.services";
import UserLunchService from "@/services/company_calendar/user-lunch";
import FullCalendar from "@fullcalendar/vue";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import moment from "moment";
import RestrictedView from "@/components/RestrictedView";

const { getLunarDays } = require("../../utils/handleCalender");

export default {
  name: "companyCalendar",
  components: {
    FullCalendar,
    RestrictedView,
  },
  middleware: "authentication",
  data() {
    return {
      selectedEvent: {},
      title: "",
      today: new Date().toISOString().substring(0, 10),
      dialogDetail: false,
      lunch: true,
      leave: true,
      showDialog: false,
      calendarOptions: {
        themeSystem: "bootstrap",
        firstDay: 1,
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin, // needed for dateClick
        ],
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay",
        },
        buttonText: {
          today: "Today",
          month: "Month",
          week: "Week",
          day: "Day",
        },
        contentHeight: 950,
        events: [],
        eventClick: this.handleEventClick,
      },
      leaveEvents: [],
      lunchEvents: [],
      lunarDay: [],
      leavesToday: 0,
      lunchesToday: 0,
      veggiesToday: 0,
      dialogConfirmDelete: false,
      searchProfile: "",
      listUserLunchUpdate: [],
    };
  },

  async mounted() {
    this.lunarDays();
    await this.getLeave();
    await this.getUserLunches();
  },

  computed: {
    dataTable() {
      return this.selectedEvent.detail.filter(
        (data) =>
          data.profile.name
            .toLowerCase()
            .includes(this.searchProfile.toLowerCase()) ||
          data.profile.personal_email
            .toLowerCase()
            .includes(this.searchProfile.toLowerCase())
      );
    },
    isDateLunarDay() {
      const date = +moment(this.selectedEvent.start).lunar().format("DD");
      return date === 1 || date === 15;
    },
  },

  methods: {
    lunarDays() {
      let calendarApi = this.$refs.fullCalendar.getApi();
      let lunarDays = getLunarDays(calendarApi);
      this.lunarDay.push(...lunarDays);
    },

    async getLeave() {
      await CalendarAdminServices.getCalendar().then((res) => {
        let off = [];
        for (const element of res) {
          element.title = "Days off";
          element.color = "#25c9d0";
          off.push(element);
        }
        this.leaveEvents = this.changeFormatLeave(off);
      });
    },

    checkBox() {
      if (this.leave === false && this.lunch === true) {
        this.calendarOptions.events = this.lunchEvents.concat(this.lunarDay);
      } else if (this.leave === false && this.lunch === false) {
        this.calendarOptions.events = this.lunarDay;
      } else if (this.leave === true && this.lunch === false) {
        this.calendarOptions.events = this.leaveEvents.concat(this.lunarDay);
      } else {
        this.calendarOptions.events = this.leaveEvents.concat(
          this.lunchEvents,
          this.lunarDay
        );
      }
    },

    handleEventClick(e) {
      this.selectedEvent = this.calendarOptions.events.find(
        (item) => item.id === e.event.id
      );
      this.dialogDetail = true;
    },

    changeFormatLunch(arr) {
      let dataArr = arr.map((item) => {
        return [item.date, item];
      });
      let mapArr = new Map(dataArr);
      let result = [...mapArr.values()];
      return result.map((item) => {
        let len = [];
        for (const element of arr) {
          if (item.date === element.date) {
            len.push(element);
            if (element.date === this.today) {
              if (!item.has_veggie) this.lunchesToday += 1;
              else this.veggiesToday += 1;
            }
          }
        }
        return {
          title: item.has_veggie
            ? `Veggie Lunch : ${len.length}`
            : `Lunch: ${len.length}`,
          id: item.id,
          detail: len,
          start: item.date,
          end: item.date,
          has_veggie: item.has_veggie,
          color: item.has_veggie ? "#90BE6D" : "#F9C74F",
        };
      });
    },

    changeFormatLeave(arr) {
      let dataArr = arr.map((item) => {
        return [item.start, item];
      });
      let mapArr = new Map(dataArr);
      let result = [...mapArr.values()];
      return result.map((item) => {
        let len = [];
        for (const element of arr) {
          if (item.start === element.start) {
            len.push(element);
            if (element.start === this.today) this.leavesToday += 1;
          }
        }
        return {
          title: item.title + ": " + len.length,
          id: item.id,
          detail: len,
          start: item.start,
          end: item.end,
          color: item.color,
        };
      });
    },

    async getUserLunches() {
      const userLunches = await UserLunchService.getAll();
      let notVeg = userLunches.data.filter((item) => item.has_veggie === false);
      let hasVeg = userLunches.data.filter((item) => item.has_veggie === true);
      let newNotVeg = this.changeFormatLunch(notVeg);
      let newHasVeg = this.changeFormatLunch(hasVeg);
      this.lunchEvents = newNotVeg.concat(newHasVeg);
      this.calendarOptions.events = this.leaveEvents.concat(
        this.lunchEvents,
        this.lunarDay
      );
    },

    changeListUserLunchUpdate(val) {
      this.listUserLunchUpdate = val;
    },

    async deleteUserLunch() {
      const data = {
        user_lunch_ids: this.listUserLunchUpdate.map((item) => item.id),
      };
      const response = await UserLunchService.deleteManyForEmployees(data);
      if (response) {
        this.$toast.success("Deleted Successfully");
        this.dialogDetail = false;
        this.searchProfile = "";
        this.dialogConfirmDelete = false;
        await this.getUserLunches();
      } else {
        this.$toast.error("Delete Failed");
      }
    },

    async updateVeggieUserLunch() {
      const data = {
        data_user_lunches: this.listUserLunchUpdate.map((item) => ({
          ["id"]: item.id,
          ["has_veggie"]: item.has_veggie,
        })),
      };
      const response = await UserLunchService.updateManyForEmployees(data);
      if (response) {
        this.$toast.success("Updated Successfully");
        this.searchProfile = "";
        this.dialogDetail = false;
        await this.getUserLunches();
      } else {
        this.$toast.error("Update Failed");
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
