<template>
  <div class="row my-2">
    <div class="col-6 col-md-2">
      <el-input
        class="pt-0"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
        clearable
        v-model="searchData.nameOrEmail"
        placeholder="Enter Name or Email"
        @keyup.enter.native="search(1)"
      >
      </el-input>
    </div>
    <div class="col-6 col-md-2">
      <el-select
        v-model="searchData.birthdayMonth"
        :options="this.MONTHS"
        @change="search(1)"
        placeholder="Birthday"
        clearable
      >
        <el-option
          v-for="(item, index) in this.MONTHS"
          :key="index"
          :label="item.value"
          :value="item.value"
        >
        </el-option>
      </el-select>
    </div>
    <div class="col-6 col-md-2">
      <el-date-picker
        v-model="searchData.joinDate"
        type="month"
        placeholder="Join date"
        name="date"
        clearable
      >
      </el-date-picker>
    </div>
    <div class="col-6 col-md-1">
      <el-select
        v-model="searchData.gender"
        :options="GENDERS"
        @change="search(1)"
        placeholder="Gender"
        clearable
      >
        <el-option
          v-for="item in GENDERS"
          :key="item.value"
          :label="item.text"
          :value="item.value"
        >
        </el-option>
      </el-select>
    </div>
    <div class="col-6 col-md-2">
      <el-select
        v-model="searchData.title"
        @change="search(1)"
        placeholder="Position"
        clearable
      >
        <el-option
          v-for="title in titles"
          :key="title.id"
          :label="title.title"
          :value="title.id"
        >
        </el-option>
      </el-select>
    </div>
    <div class="col-6 col-md-2">
      <el-select
        v-model="searchData.team"
        :options="optionsTeam"
        @change="search(1)"
        placeholder="Team"
        clearable
      >
        <el-option
          v-for="item in optionsTeam"
          :key="item"
          :label="item"
          :value="item"
        >
        </el-option>
      </el-select>
    </div>
    <div
      class="col-6 col-md-1 d-flex justify-content-center align-items-center"
    >
      <el-switch
        style="display: block"
        v-model="searchData.active"
        active-color="#13ce66"
        inactive-color="#ff4949"
        active-text="Active"
      >
      </el-switch>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import SearchUserService from "@/services/user/searchUser";
import { MONTHS } from "@/const/months";
import { GENDERS } from "@/const/genders";
import "vue2-datepicker/index.css";
import moment from "moment";
import monthSelectPlugin from "flatpickr/dist/plugins/monthSelect/index";
import "flatpickr/dist/plugins/monthSelect/style.css";

const { validateEmail } = require("../../utils/validation");

export default {
  name: "FilterBox",

  props: ["page_size"],
  data() {
    return {
      flatpickrConfig: {
        plugins: [
          new monthSelectPlugin({
            shorthand: true, //defaults to false
          }),
        ],
      },
      searchData: {
        nameOrEmail: "",
        birthdayMonth: null,
        joinDate: "",
        gender: null,
        team: null,
        title: "",
        active: true,
      },
      optionsTeam: [],
    };
  },
  watch: {
    "searchData.joinDate": function () {
      this.search(1);
    },
    "searchData.active": function () {
      this.search(1);
    },
    "searchData.nameOrEmail": function () {
      if (!this.searchData.nameOrEmail) this.search(1);
    },
  },
  created() {
    this.fetchTitles();
    this.setOptionTeam();
    if (GENDERS.length < 4) {
      GENDERS.push({
        text: "All",
        value: "",
      });
    }
  },
  computed: {
    ...mapState("probation", ["titles"]),

    MONTHS: function () {
      return MONTHS;
    },
    GENDERS: function () {
      return GENDERS;
    },
  },
  methods: {
    ...mapActions("probation", ["fetchTitles"]),

    getSearchData() {
      return this.searchData;
    },

    async setOptionTeam() {
      let data = await SearchUserService.getTeamOption();
      if (data && data.data) {
        data.data.data.forEach((row) => this.optionsTeam.push(row.team_name));
        this.optionsTeam.push("All");
      }
    },
    async search(page = 1) {
      const joindate = this.format_date(this.searchData.joinDate);
      const responseData = await SearchUserService.get(
        this.searchData.nameOrEmail,
        this.searchData.birthdayMonth,
        joindate,
        this.searchData.gender,
        this.searchData.title,
        this.searchData.team,
        this.searchData.active,
        page,
        this.page_size
      );
      if (responseData && responseData.data) {
        this.$emit("loadData", responseData, true);
      }
    },
    async clearFilter() {
      this.searchData = {
        name: "",
        email: "",
        birthdayMonth: null,
        joinDate: "",
        gender: null,
        team: null,
        title: null,
        active: true,
      };
      this.$emit("getData");
    },
    format_date(value) {
      if (value) {
        return moment(String(value)).format("YYYY-MM");
      }
    },
  },
};
</script>
<style scoped>
@import "filter.scss";
</style>
