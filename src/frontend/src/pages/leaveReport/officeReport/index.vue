<template>
  <div>
    <el-card>
      <el-row :gutter="12" class="mb-3">
        <el-col :span="6">
          <el-input
            v-model="searchData.search"
            placeholder="Search name or email"
            @change="getData(1)"
            clearable
          />
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="dateSearch"
            type="monthrange"
            range-separator="-"
            start-placeholder="Start month"
            end-placeholder="End month"
            @change="getData(1)"
            style="width: 100%"
          >
          </el-date-picker>
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="searchData.leave_types"
            placeholder="Leave type"
            @change="getData(1)"
            style="width: 100%"
            multiple
          >
            <el-option
              v-for="data in leaveTypes"
              :label="data"
              :value="data"
              :key="data"
            >
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="3">
          <download-excel
            :fetch="fetchDataForExportExcel"
            :fields="json_fields"
            :worksheet="nameExportFile"
            title="Export Excel"
            :name="nameExportFile + '.xlsx'"
          >
            <el-button type="primary">
              <font-awesome-icon :icon="['fas', 'file-export']" />
              Export Data
            </el-button>
          </download-excel>
        </el-col>
      </el-row>
      <el-table
        highlight-current-row
        :data="officeReportData.results"
        header-cell-class-name="bg-header-table"
        border
        style="width: 100%"
      >
        <el-table-column
          v-for="(item, key) in headers"
          :key="key"
          :prop="item.value"
          :label="item.text"
          :width="item.text.length > 18 ? 300 : 200"
          sortable
          align="center"
        >
        </el-table-column>
      </el-table>
      <div class="d-flex justify-content-center mt-5">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="officeReportData.page_size"
          :page-count="officeReportData.page_number"
          :current-page="officeReportData.current"
          @current-change="setPage"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";
import StatisticDateOffService from "@/services/leave_management/statisticDateOffService";
import moment from "moment";

export default {
  name: "OfficeReport",
  data() {
    return {
      searchData: {
        search: "",
        leave_types: [],
        page: 1,
        page_size: 12,
      },
      dateSearch: [new Date(), new Date()],
      officeReportData: {},
      leaveTypes: [],
      json_fields: {
        Name: "name",
        Email: "email",
        Holidays: "holidays",
      },
      headers: [],
    };
  },
  async created() {
    await this.getTypeOff();
    await this.getData(1);
  },
  watch: {
    "searchData.search": function () {
      if (this.searchData.search.trim() === "") {
        this.getData(1);
      }
    },
  },
  computed: {
    nameExportFile() {
      if (this.dateSearch) {
        return `Office_report_${this.dates[0]}_to_${this.dates[1]}`;
      } else {
        return "Office_report_all_day";
      }
    },
    dates() {
      if (this.dateSearch) {
        return [
          moment(this.dateSearch[0]).startOf("M").format("YYYY-MM-DD"),
          moment(this.dateSearch[1]).endOf("M").format("YYYY-MM-DD"),
        ];
      } else {
        return [];
      }
    },
  },
  methods: {
    async setPage(page) {
      await this.getData(page);
    },
    async getTypeOff() {
      const res = await TypeOffAdminServices.getTypeOff();
      if (res.data) {
        this.leaveTypes = res.data.map((data) => data.name);
      }
    },
    updateHeaders() {
      const listType = this.searchData.leave_types.length
        ? this.searchData.leave_types
        : this.leaveTypes;
      this.headers = [
        {
          text: "Name",
          value: "name",
        },
        {
          text: "Email",
          sortable: false,
          value: "email",
        },
        {
          text: "Holidays",
          value: "holidays",
        },
        ...listType.map((type) => {
          return {
            text: `${type} days`,
            value: `number_${type}`,
            detail: `${type}`,
            class: "specialClass-1",
          };
        }),
      ];
    },
    getItemForExportTotal() {
      const listType = this.searchData.leave_types.length
        ? this.searchData.leave_types
        : this.leaveTypes;
      for (let i = 0; i < listType.length; i++) {
        this.json_fields[
          `Number of ${listType[i]} days`
        ] = `number_${listType[i]}`;
        this.json_fields[`${listType[i]} days detail`] = {
          field: `${listType[i]}`,
          callback: (value) => {
            return this.getCallBack(value);
          },
        };
      }
    },
    getCallBack(value) {
      const data = [];
      for (let i = 0; i < value.length; i++) {
        let detailData = `${i + 1}: ${value[i].date} - ${value[i].type}`;
        if (value[i].lunch) {
          detailData = detailData + " - Have eat lunch";
        } else {
          detailData = detailData + " - Don't have eat lunch";
        }
        data.push(detailData);
      }
      return data;
    },
    async fetchDataForExportExcel() {
      await this.getItemForExportTotal();
      this.searchData.page_size = this.officeReportData.count;
      const [start_date, end_date] = this.dates;
      const res = await StatisticDateOffService.getByAdmin({
        ...this.searchData,
        start_date,
        end_date,
      });
      this.searchData.page_size = 12;
      if (res.data.results.length) {
        return res.data.results;
      } else {
        this.$toast.error("No data to export");
      }
    },
    async getData(page) {
      this.searchData.page = page;
      const [start_date, end_date] = this.dates;
      const res = await StatisticDateOffService.getByAdmin({
        ...this.searchData,
        start_date,
        end_date,
      });
      if (res.data) {
        this.updateHeaders();
        this.officeReportData = res.data;
      }
    },
  },
};
</script>

<style></style>
