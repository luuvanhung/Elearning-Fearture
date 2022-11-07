<template>
  <div class="my-2">
    <div class="bg-light">
      <el-col :xs="24" :sm="24" :md="8" :lg="4" :xl="4" class="pr-2">
        <el-row style="height: 60px"> </el-row>
        <el-row>
          <div class="text-center">
            <el-dropdown placement="top-end">
              <div class="text-center mb-3 mx-2">
                <el-button class="btn_lunch" type="primary">
                  SET LUNCH
                </el-button>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="dialog = true">
                  Range
                </el-dropdown-item>
                <el-dropdown-item @click.native="setToday">
                  Today
                </el-dropdown-item>
                <el-dropdown-item
                  v-if="!userVeggie"
                  @click.native="setVeggieLunch()"
                >
                  Veggie
                </el-dropdown-item>
                <restricted-view :scope="['user_lunch:edit_all_user_lunch']">
                  <template #default>
                    <el-dropdown-item
                      @click.native="dialogLunchSaturday = true"
                    >
                      Saturday
                    </el-dropdown-item>
                  </template>
                </restricted-view>
              </el-dropdown-menu>
            </el-dropdown>
            <el-dropdown>
              <div class="text-center mx-2">
                <el-button class="btn_lunch" type="danger">
                  CANCEL LUNCH
                </el-button>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="cancelSetVeggieLunch()">
                  Veggie
                </el-dropdown-item>
                <el-dropdown-item @click.native="deleteMany()">
                  Set
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
          <div class="group-checkbox">
            <div class="checkbox-calendar d-flex justify-content-center mt-3">
              <el-checkbox
                v-model="userVeggie"
                label="Auto Veggie"
                size="medium"
                @change="updateVeggieOfUser"
              >
              </el-checkbox>
            </div>
            <div class="checkbox-calendar d-flex justify-content-center">
              <el-checkbox
                v-model="autoBooking"
                label="Auto Booking"
                size="medium"
                @change="updateStatusAutoBooking"
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
                round
                type="warning"
                class="btn_lunch"
                disabled
                style="background-color: #feab30"
                >Descriptions</el-button
              >
            </div>
            <div class="description-detail">
              <div class="box-description-lunar ml-5"></div>
              <small class="ml-3">Lunar Day</small>
            </div>
            <div class="description-detail">
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
      <el-dialog title="SET LUNCH RANGE" :visible.sync="dialog" max-width="500">
        <el-card>
          <el-container>
            <el-form>
              <div class="d-flex flex-row">
                From
                <flat-pickr
                  v-model="startDate"
                  class="bg-white ml-3 mb-2 mr-3"
                  placeholder="Select date"
                  :config="{
                    altInput: true,
                    altFormat: 'd-m-Y',
                    minDate: this.today,
                    dateFormat: 'Y-m-d',
                    locale: { firstDayOfWeek: 1 },
                  }"
                />
                To
                <flat-pickr
                  v-model="endDate"
                  class="bg-white ml-3 mb-2"
                  placeholder="Select date"
                  :config="{
                    altInput: true,
                    altFormat: 'd-m-Y',
                    minDate: this.startDate ? this.startDate : this.today,
                    dateFormat: 'Y-m-d',
                    locale: { firstDayOfWeek: 1 },
                  }"
                />
                <p class="ml-3">Has Veggie</p>
                <font-awesome-icon
                  :icon="['fas', 'leaf']"
                  class="text-success fa-fw"
                />
                <input
                  v-model="has_veggie"
                  type="checkbox"
                  class="form-check-input ml-2"
                />
                <span class="checkmark" />
              </div>

              <div class="d-flex justify-content-end">
                <el-button class="btn_submit ml-2" @click="addEvent()">
                  Create Lunch
                </el-button>
              </div>
            </el-form>
          </el-container>
        </el-card>
      </el-dialog>
      <el-dialog :visible.sync="dialogDetail" max-width="300">
        <el-card
          v-if="
            selectedEvent.title === 'Lunch' ||
            selectedEvent.title === 'Veggie Lunch'
          "
        >
          <div slot="header">
            <span>{{ selectedEvent.title }}</span>
          </div>
          <div class="d-flex flex-row">
            <p class="mt-3">Do you want to cancel lunch today ?</p>
            <el-button
              class="ml-3"
              type="danger"
              @click="deleteEvent(selectedEvent)"
            >
              <em class="el-icon-delete"></em>
            </el-button>
            <div v-if="checkLunarDay() === true">
              <el-checkbox class="mt-3 ml-4" v-model="selectedEvent.has_veggie">
                Has veggie
              </el-checkbox>
              <font-awesome-icon :icon="['fas', 'leaf']" class="mt-3 ml-3" />
              <el-button
                class="ml-3"
                type="primary"
                @click="updateEvent(selectedEvent)"
              >
                Update
              </el-button>
            </div>
          </div>
        </el-card>
      </el-dialog>
      <el-dialog
        title="Set Lunch Saturday"
        :visible.sync="dialogLunchSaturday"
        max-width="500"
      >
        <el-card>
          <el-container>
            <el-form style="width: 100%">
              <div class="d-flex align-items-center justify-content-between">
                <div>
                  <flat-pickr
                    v-model="setLunchSaturday"
                    class="bg-white w-50 p-2"
                    placeholder="Select date"
                    :config="{
                      altInput: true,
                      altFormat: 'd-m-Y',
                      minDate: this.today,
                      dateFormat: 'Y-m-d',
                      locale: { firstDayOfWeek: 1 },
                      enable: [
                        function (date) {
                          return date.getDay() === 6;
                        },
                      ],
                    }"
                  />
                </div>
                <div class="d-flex">
                  <el-checkbox
                    class="form-check-input ml-2"
                    v-model="allVeggieSaturday"
                    @change="toggleAllVeggieSaturday"
                  ></el-checkbox>
                  <p
                    class="ml-2"
                    style="display: inline-block; font-size: 1rem"
                  >
                    Has Veggie
                  </p>
                  <font-awesome-icon
                    :icon="['fas', 'leaf']"
                    class="text-success fa-fw"
                  />
                </div>
                <div class="d-flex justify-content-end">
                  <el-button
                    :disabled="btnRemoveAll"
                    @click="removeAllListSaturday()"
                    class="btn_submit ml-2"
                  >
                    Remove all
                  </el-button>
                </div>
                <div class="d-flex justify-content-end">
                  <el-button
                    :disabled="btnRemoveAll"
                    @click="createListUserSaturday()"
                    class="btn_submit ml-3"
                  >
                    Create Lunch
                  </el-button>
                </div>
              </div>
            </el-form>
          </el-container>
        </el-card>
        <el-card>
          <div>
            <p
              class="d-block w-100 py-2 badge my-2 badge-pill"
              style="font-size: 1.1rem"
            >
              Registers
            </p>
          </div>
          <el-table
            :data="listUserLunchSaturday.shows"
            stripe
            header-cell-class-name="bg-header-table"
            style="width: 100%"
          >
            <el-table-column prop="profile.name" label="Name" align="center">
              <template #default="table">
                <router-link
                  :to="`/profile/${table.row.id}`"
                  title="Click to move to Profile page"
                  tag="a"
                  prop="profile.name"
                >
                  <strong>{{ table.row.profile.name }}</strong>
                </router-link>
              </template>
            </el-table-column>

            <el-table-column prop="profile.email" label="Email" align="center">
              <template #default="table">
                <strong>
                  {{ table.row.profile.personal_email }}
                </strong>
              </template>
            </el-table-column>

            <el-table-column label="Veggie" align="center">
              <template #default="table">
                <el-checkbox
                  v-model="table.row.checkVeggie"
                  @change="toggleListUserLunchVeggie(table.row)"
                  class="form-check-input ml-2"
                >
                </el-checkbox>
              </template>
            </el-table-column>
            <el-table-column label="Action" align="center">
              <template #default="table">
                <img
                  :src="require('@/static/images/IconDelete.svg')"
                  class="ml-1"
                  @click="removeListUserLunchRegister(table.row)"
                  alt="delete"
                />
              </template>
            </el-table-column>
          </el-table>
          <div class="d-flex justify-content-center mt-5">
            <el-pagination
              background
              layout="prev, pager, next"
              :page-size="page_size"
              :page-count="listUserLunchSaturday.totalPage"
              :current-page="listUserLunchSaturday.currentPage"
              :total="listUserLunchSaturday.count"
              @current-change="setPageRegister"
            >
            </el-pagination>
          </div>
        </el-card>
        <el-card>
          <div style="margin-bottom: 10px">
            <p
              class="d-inline-block py-2 badge my-2 badge-pill"
              style="width: 35%; font-size: 1.1rem"
            >
              Employee List
            </p>
            <el-input
              placeholder="Search name or email"
              v-model="contentSearch.name"
              @keyup.enter.native="searchUserByNameOrEmail(1)"
              clearable
              style="width: 30%"
            />
          </div>
          <el-table
            :data="listProfileUser.rows"
            stripe
            header-cell-class-name="bg-header-table"
            style="width: 100%"
          >
            <el-table-column prop="profile.name" label="Name" align="center">
              <template #default="table">
                <router-link
                  :to="`/profile/${table.row.id}`"
                  title="Click to move to Profile page"
                  tag="a"
                  prop="profile.name"
                >
                  <strong>{{ table.row.profile.name }}</strong>
                </router-link>
              </template>
            </el-table-column>
            <el-table-column prop="profile.email" label="Email" align="center">
              <template #default="table">
                <strong>
                  {{ table.row.profile.personal_email }}
                </strong>
              </template>
            </el-table-column>
            <el-table-column label="Action" align="center">
              <template #default="table">
                <img
                  :src="require('@/static/images/IconAdd.svg')"
                  @click="addListUserLunchRegister(table.row)"
                  style="width: 1.6rem; height: 1.6rem"
                  alt="Add"
                />
              </template>
            </el-table-column>
          </el-table>
          <div class="d-flex justify-content-center mt-5">
            <el-pagination
              background
              layout="prev, pager, next"
              :page-size="page_size"
              :page-count="listProfileUser.totalPage"
              :current-page="listProfileUser.currentPage"
              @current-change="setPage"
            >
            </el-pagination>
          </div>
        </el-card>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import FullCalendar from "@fullcalendar/vue";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import UserLunchService from "@/services/company_calendar/user-lunch";
import ProfileService from "@/services/profile/profile";
import flatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import moment from "moment";
import "moment-lunar";
import GetUserService from "@/services/user/getUser";
import RestrictedView from "@/components/RestrictedView";

const { getLunarDays } = require("../../utils/handleCalender");

export default {
  name: "LunchCalendar",
  middleware: "authentication",
  components: {
    FullCalendar,
    flatPickr,
    RestrictedView,
  },
  data() {
    return {
      lunch: true,
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
      selectedEvent: {},
      content: "",
      eventsLunch: [],
      today: new Date().toISOString().substring(0, 10),
      focus: new Date().toISOString().substring(0, 10),
      name: "Lunch",
      start: null,
      userVeggie: false, // using when user want to set auto has veggie in lunar day
      has_veggie: false, // using in lunar day
      end: null,
      color: "#20B2AA", // default event color
      dialog: false,
      startDate: new Date().toISOString().substring(0, 10),
      endDate: null,
      dialogDetail: false,
      lunarDay: [],
      autoBooking: false,
      profile: "",
      btnRemoveAll: true,
      dialogLunchSaturday: false,
      allVeggieSaturday: false,
      page_size: 4,
      contentSearch: {
        name: "",
      },
      listProfileUser: {
        searching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
      },
      setLunchSaturday: null,
      listUserLunchSaturday: {
        rows: [],
        currentPage: 1,
        totalPage: 1,
        shows: [],
      },
    };
  },

  watch: {
    "contentSearch.name": function () {
      if (!this.contentSearch.name) this.getListUser(1);
    },
    "listUserLunchSaturday.rows": function () {
      this.btnRemoveAll = this.listUserLunchSaturday.rows.length === 0;
      let obj = this.listUserLunchSaturday;
      if (!(!obj.rows || obj.rows.length === 0)) {
        obj.totalPage =
          Math.floor(obj.rows.length / this.page_size) <
          obj.rows.length / this.page_size
            ? Math.floor(obj.rows.length / this.page_size) + 1
            : obj.rows.length / this.page_size;

        if (obj.currentPage > obj.totalPage) {
          obj.currentPage = obj.totalPage;
        } else {
          obj.shows = [
            ...obj.rows.slice(
              (obj.currentPage - 1) * this.page_size,
              (obj.currentPage - 1) * this.page_size + this.page_size
            ),
          ];
        }
      }
    },
    "listUserLunchSaturday.currentPage": function () {
      this.listUserLunchSaturday.shows = [
        ...this.listUserLunchSaturday.rows.slice(
          (this.listUserLunchSaturday.currentPage - 1) * this.page_size,
          (this.listUserLunchSaturday.currentPage - 1) * this.page_size +
            this.page_size
        ),
      ];
    },
    dialogLunchSaturday: async function () {
      this.listUserLunchSaturday.rows = [];
      this.listUserLunchSaturday.currentPage = 1;
      this.listUserLunchSaturday.totalPage = 1;
      this.listUserLunchSaturday.shows = [];
      this.setLunchSaturday = null;
      if (this.dialogLunchSaturday === true) await this.getListUser(1);
    },
  },

  async mounted() {
    this.lunarDays();
    await this.getEvents();
    await this.getMyProfile();
    await this.getListUser(1);
  },

  methods: {
    // set saturday lunch
    async createListUserSaturday() {
      try {
        if (!this.listUserLunchSaturday.rows) {
          this.$toast.error("No one register");
        } else if (!this.setLunchSaturday) {
          this.$toast.error("Date has not been selected");
        } else {
          const listCreate = this.listUserLunchSaturday.rows.map((data) => {
            return {
              profile: data.profile.id,
              has_veggie: data.checkVeggie,
              date: this.setLunchSaturday,
            };
          });
          const response = await UserLunchService.adminCreate(listCreate);
          await this.getEvents();
          if (response && response.data.msg) {
            const content = response.data.msg;
            if (response.data.status === 1) this.$toast.success(content);
            else this.$toast.warning(content);
          }
        }
      } catch (e) {
        this.$toast.error("Create Failed");
      }
    },

    toggleAllVeggieSaturday() {
      let results = this.listUserLunchSaturday.rows;
      this.listUserLunchSaturday.rows = [];
      this.listUserLunchSaturday.rows = results.map((data) => {
        return { ...data, checkVeggie: this.allVeggieSaturday };
      });
    },

    toggleListUserLunchVeggie(user) {
      this.listUserLunchSaturday.rows = this.listUserLunchSaturday.rows.map(
        (data) => {
          if (data.profile === user.profile) {
            data.checkVeggie = user.checkVeggie;
          }
          return { ...data };
        }
      );
    },

    addListUserLunchRegister(user) {
      user.checkVeggie = this.allVeggieSaturday ? true : user.profile.veggie;
      if (
        !this.listUserLunchSaturday.rows.find((data) => {
          return data.profile.id === user.profile.id;
        })
      ) {
        this.listUserLunchSaturday.rows.unshift(user);
      } else {
        this.$toast.error("Already existed");
      }
    },

    removeListUserLunchRegister(user) {
      this.listUserLunchSaturday.rows.splice(
        this.listUserLunchSaturday.rows.indexOf(user),
        1
      );
      if (!this.listUserLunchSaturday.rows === false)
        this.listUserLunchSaturday.shows = [];
    },

    removeAllListSaturday() {
      this.listUserLunchSaturday.rows = [];
      this.listUserLunchSaturday.currentPage = 1;
      this.listUserLunchSaturday.totalPage = 1;
      this.listUserLunchSaturday.shows = [];
      this.allVeggieSaturday = false;
    },

    async searchUserByNameOrEmail(page = 1, active = 1) {
      let name = this.contentSearch.name.trim();
      const responseData = await GetUserService.searchUserByNameOrEmail(
        name,
        page,
        this.page_size,
        active
      );
      if (responseData && responseData.data) this.loadData(responseData, true);
    },

    format_date(value) {
      if (value) {
        return moment(String(value)).format("YYYY-MM-DD");
      }
    },

    async getListUser(page = 1, page_size = this.page_size) {
      if (!this.listProfileUser.searching) {
        let responseData = await GetUserService.get(page_size, page, 1);
        if (responseData && responseData.data) {
          this.loadData(responseData, false);
        }
      } else {
        await this.searchUserByNameOrEmail(page, 1);
      }
    },

    setPage(page) {
      this.getListUser(page);
    },

    setPageRegister(page) {
      this.listUserLunchSaturday.currentPage = page;
    },

    loadData(responseData, isSearching) {
      this.listProfileUser.searching = isSearching;
      this.listProfileUser.rows = responseData.data.results;
      this.listProfileUser.totalPage = responseData.data.page_number;
      this.listProfileUser.currentPage = responseData.data.current;
    },
    //end: set saturday lunch
    lunarDays() {
      let calendarApi = this.$refs.fullCalendar.getApi();
      let lunarDays = getLunarDays(calendarApi);
      this.lunarDay.push(...lunarDays);
    },

    checkLunarDay() {
      const date = moment(this.selectedEvent.start).lunar().format("DD");
      return date === "01" || date === "15";
    },

    async getEvents() {
      this.eventsLunch = await this.$store.dispatch("event/getUserLunches");
      this.calendarOptions.events = this.eventsLunch.concat(this.lunarDay);
    },

    handleEventClick(e) {
      this.selectedEvent = this.calendarOptions.events.find(
        (item) => item.id === e.event.id
      );
      this.dialogDetail = true;
    },
    async deleteMany() {
      const data = {
        date: this.today,
      };
      const userLunch = await UserLunchService.deleteMany(data);
      await this.getEvents();
      if (userLunch && userLunch.data.msg) {
        const content = userLunch.data.msg;
        this.$toast.success(content);
      }
    },

    async setVeggieLunch() {
      const date = new Date();
      const hours = date.getHours();
      if (hours >= 9) {
        return this.$toast.error("Out of time to set lunch");
      }
      const data = {
        date: this.today,
      };
      const userLunch = await UserLunchService.setVeggieMonth(data);
      const contentRes = "Not found lunar day";
      await this.getEvents();
      if (userLunch && userLunch.data.msg !== contentRes) {
        const content = userLunch.data.msg;
        this.$toast.success(content);
        this.userVeggie = true;
      }
      if (userLunch && userLunch.data.msg === contentRes) {
        this.$toast.error(contentRes);
      }
    },

    async cancelSetVeggieLunch() {
      const data = {
        date: this.today,
      };
      const userLunch = await UserLunchService.cancelSetVeggieMonth(data);
      await this.getEvents();
      if (userLunch && userLunch.data.msg) {
        const content = userLunch.data.msg;
        this.$toast.success(content);
      }
    },

    async setToday() {
      const date = new Date();
      const hours = date.getHours();
      if (hours >= 9) {
        return this.$toast.error("Out of time to set lunch");
      }
      this.focus = this.today;
      const data = {
        name: this.name,
        has_veggie: this.has_veggie || false,
        date: this.today,
      };
      const userLunch = await UserLunchService.create(data);
      await this.getEvents();
      if (userLunch && userLunch.data.date) {
        this.$toast.success("You have setted lunch for today");
      }
      if (userLunch && userLunch.data.error_msg) {
        this.$toast.error(userLunch.data.error_msg);
      }
    },

    async addEvent() {
      this.dialog = false;
      const date = new Date();
      const hours = date.getHours();
      const today = moment();
      if (this.startDate > this.endDate) {
        return this.$toast.error("End day must be greater than start day");
      }
      if (this.startDate < this.today) {
        return this.$toast.error("Start day must be greater than today");
      }
      if (this.startDate === this.today && hours >= 9) {
        this.startDate = moment(today).add(1, "days").format("YYYY-MM-DD");
      }
      if (this.startDate && this.endDate) {
        const data = {
          name: this.name,
          has_veggie: this.has_veggie,
          list_dates: this.getDatesUnRange(this.startDate, this.endDate),
        };
        const userLunches = await UserLunchService.createMany(data);
        await this.getEvents();
        if (userLunches && userLunches.data.msg) {
          const content = userLunches.data.msg;
          this.$toast.success(content);
        }
      } else alert("You must enter start and end time");
    },

    async updateEvent(ev) {
      const date = new Date();
      const hours = date.getHours();
      if (hours >= 9 && ev.start <= this.today) {
        return this.$toast.error("Out of time to update lunch");
      }
      const data = {
        has_veggie: ev.has_veggie,
      };
      const response = await UserLunchService.update({ data, id: ev.id });
      if (response) {
        this.$toast.success("Updated Successfully");
        await this.getEvents();
        this.dialogDetail = false;
      } else {
        this.$toast.error("Update Failed");
      }
    },

    async deleteEvent(ev) {
      const date = new Date();
      const hours = date.getHours();
      if (hours >= 9 && ev.start <= this.today) {
        return this.$toast.error("Out of time to cancel lunch");
      }
      const userLunch = await UserLunchService.delete(ev.id);
      await this.getEvents();
      if (userLunch && userLunch.data.msg) {
        const content = userLunch.data.msg;
        this.$toast.success(content);
      }
      this.dialogDetail = false;
    },

    getDatesUnRange(startDate, stopDate) {
      const dateArray = [];
      let currentDate = moment(startDate);
      let endDate = moment(stopDate);
      while (currentDate <= endDate) {
        dateArray.push(moment(currentDate).format("YYYY-MM-DD"));
        currentDate = moment(currentDate).add(1, "days");
      }
      return dateArray;
    },

    async getMyProfile() {
      const user = this.$store.state.user.currentUser;
      const res = await ProfileService.getOneProfile(user.profile_id);
      this.profile = res.data;
      this.autoBooking = this.profile.auto_booking_lunch;
      this.userVeggie = this.profile.veggie;
    },

    async updateStatusAutoBooking() {
      try {
        const data = {
          auto_booking_lunch: this.autoBooking,
        };
        const date = new Date();
        const hours = date.getHours();
        const today = moment();
        await ProfileService.updateAutoBookingLunch(this.profile.id, data);
        this.$toast.success("Updated Successfully");
        if (this.autoBooking === true) {
          this.startDate = this.today;
          if (hours >= 9) {
            this.startDate = moment(today).add(1, "days").format("YYYY-MM-DD");
          }
          this.endDate = moment().endOf("month").format("YYYY-MM-DD");
          const dataSetLunch = {
            name: this.name,
            has_veggie: this.userVeggie,
            list_dates: this.getDatesUnRange(this.startDate, this.endDate),
          };
          const userLunches = await UserLunchService.createMany(dataSetLunch);
          await this.getEvents();
          if (userLunches && userLunches.data.msg) {
            const content = userLunches.data.msg;
            this.$toast.success(content);
          }
        }
      } catch (e) {
        this.$toast.error("Update Failed");
      }
    },

    async updateVeggieOfUser() {
      const data = {
        veggie: this.userVeggie,
      };
      await ProfileService.updateUserVeggie(this.profile.id, data).then(
        async (res) => {
          try {
            if (res.status === 204) {
              for (const date in this.lunarDay) {
                let userLunch = this.calendarOptions.events.find(
                  (item) =>
                    item.start === this.lunarDay[date].start &&
                    new Date(item.start).getDate() >
                      new Date(this.today).getDate()
                );
                if (userLunch) {
                  const dataLunch = {
                    has_veggie: this.userVeggie,
                  };
                  const response = await UserLunchService.update(
                    dataLunch,
                    userLunch.id
                  );
                  if (response) {
                    await this.getEvents();
                  }
                }
              }
              this.$toast.success("Updated Successfully");
            }
          } catch (e) {
            let error = "Update Failed";
            if (e.response && e.response.data.error !== "") {
              error = e.response.data.error;
            }
            this.$toast.error(error);
          }
        }
      );
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
