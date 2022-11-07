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
        v-model="search_name_local"
        placeholder="Enter Name or Email"
      >
      </el-input>
    </div>
    <div class="col-6 col-md-2">
      <el-select
        v-model="search_team_local"
        :options="optionsTeam"
        placeholder="Teams"
        clearable
      >
        <el-option
          v-for="(item, index) in optionsTeam"
          :key="index"
          :label="item"
          :value="item"
        >
        </el-option>
      </el-select>
    </div>
  </div>
</template>

<script>
import SearchUserService from "@/services/user/searchUser";
import { GENDERS } from "@/const/genders";
import "vue2-datepicker/index.css";
import moment from "moment";
import monthSelectPlugin from "flatpickr/dist/plugins/monthSelect/index";
import "flatpickr/dist/plugins/monthSelect/style.css";

export default {
  name: "FilterBonusLeave",

  props: {
    page_size: Number,
    search_name: String,
    search_team: String,
  },
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
        name: "",
        email: "",
        birthdayMonth: null,
        joinDate: "",
        gender: null,
        team: null,
        title: "",
      },
      optionsTeam: [],
    };
  },
  created() {
    this.setOptionTeam();
    if (GENDERS.length < 4) {
      GENDERS.push({
        text: "All",
        value: "",
      });
    }
  },
  computed: {
    search_name_local: {
      get: function () {
        return this.search_name;
      },
      set: function (value) {
        this.$emit("ud_search_name", value);
      },
    },
    search_team_local: {
      get: function () {
        return this.search_team;
      },
      set: function (value) {
        this.$emit("ud_search_team", value);
      },
    },
  },
  methods: {
    async setOptionTeam() {
      let data = await SearchUserService.getTeamOption();
      if (data && data.data) {
        data.data.data.forEach((row) => this.optionsTeam.push(row.team_name));
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
<style scoped></style>
