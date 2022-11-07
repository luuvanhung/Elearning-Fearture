<template>
  <div class="row my-2">
    <div class="col-6 col-md-auto">
      <el-input
        class="pt-0"
        append-icon="mdi-magnify"
        label="Search"
        v-model="searchData.nameOrEmail"
        placeholder="Enter Name or Email"
        @keyup.enter.native="search()"
        clearable
      >
      </el-input>
    </div>
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
    <div class="col-6 col-md-auto">
      <el-select
        v-model="searchData.typeLeave"
        placeholder="Leave Type"
        clearable
        @change="search()"
      >
        <div v-for="typeOff in listTypeOff" v-bind:key="typeOff.id">
          <div class="background">
            <strong class="ml-3"> {{ typeOff.name }} </strong>
          </div>
          <el-option
            v-for="typeOffDetail in typeOff.data"
            :key="typeOffDetail.index"
            :value="typeOffDetail.id"
            :label="typeOffDetail.name"
          >
          </el-option>
        </div>
      </el-select>
    </div>
    <div class="col-6 col-md-auto">
      <el-select
        v-model="searchData.status"
        @change="search()"
        placeholder="Status"
        clearable
      >
        <div v-for="(color, status, index) in listStatus" v-bind:key="index">
          <el-option :key="index" :value="status" :label="status"> </el-option>
        </div>
      </el-select>
    </div>
  </div>
</template>

<script>
import "vue2-datepicker/index.css";
import "flatpickr/dist/plugins/monthSelect/style.css";
import _ from "lodash";
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";

export default {
  name: "FilterBox",

  props: ["page_size", "searchData"],
  data() {
    return {
      listTypeOff: [],
      listStatus: {
        Pending: "#e6a23c",
        Approved: "#67c23a",
        Rejected: "#f56c6c",
        Canceling: "#e6a23c",
        Canceled: "#909399",
      },
    };
  },
  watch: {
    "searchData.date": function () {
      this.search();
    },
    "searchData.nameOrEmail": function () {
      if (!this.searchData.nameOrEmail) this.search();
    },
  },
  created: async function () {
    await TypeOffAdminServices.getTypeOffUser().then((res) => {
      this.listTypeOff = this.handleDataAPI(res.data);
    });
  },
  methods: {
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
    search(page = 1) {
      this.$emit("searchRequest", page, this.searchData);
    },
  },
};
</script>
<style scoped>
@import "filter.scss";
</style>
