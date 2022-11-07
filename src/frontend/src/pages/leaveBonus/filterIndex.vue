<template>
  <div class="row my-2">
    <div class="col-6 col-md-2">
      <el-select
        v-model="searchData.bonusTypeId"
        :options="optionsBonusType"
        @change="search()"
        placeholder="Types"
        default-first-option
        clearable
      >
        <el-option
          v-for="(item, index) in optionsBonusType"
          :key="index"
          :label="item.name"
          :value="item.id"
        >
        </el-option>
      </el-select>
    </div>
    <div class="col-6 col-md-2">
      <el-input
        class="pt-0"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
        clearable
        v-model="searchData.searchName"
        placeholder="Enter Name or Email"
        @keyup.enter.native="search()"
      >
      </el-input>
    </div>
    <div class="col-6 col-md-2">
      <el-input
        class="pt-0"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
        clearable
        v-model="searchData.reason"
        placeholder="Enter Reason"
        @keyup.enter.native="search()"
      >
      </el-input>
    </div>
    <div class="col-6 col-md-2">
      <el-form :inline="true">
        <el-form-item prop="date">
          <el-date-picker
            v-model="searchData.date"
            type="daterange"
            range-separator="-"
            start-placeholder="Start date"
            end-placeholder="End date"
          >
          </el-date-picker>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import "vue2-datepicker/index.css";
import moment from "moment";
import monthSelectPlugin from "flatpickr/dist/plugins/monthSelect/index";
import "flatpickr/dist/plugins/monthSelect/style.css";

export default {
  name: "FilterIndex",

  props: ["page_size", "optionsBonusType", "searchData"],
  data() {
    return {
      flatpickrConfig: {
        plugins: [
          new monthSelectPlugin({
            shorthand: true, //defaults to false
          }),
        ],
      },
    };
  },
  watch: {
    "searchData.date": function () {
      this.search();
    },
    "searchData.searchName": function () {
      this.search();
    },
    "searchData.reason": function () {
      this.search();
    },
  },

  methods: {
    getSearchData() {
      return this.searchData;
    },
    search(page = 1) {
      this.$emit("searchRequest", page, this.searchData);
    },
    format_date(value) {
      if (value) {
        return moment(String(value)).format("YYYY-MM-DD");
      }
    },
  },
};
</script>
<style scoped></style>
