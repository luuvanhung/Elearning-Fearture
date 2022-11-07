<template>
  <div class="bg-light">
    <div v-if="isLoadingMask" class="lmask" ref="loading-mask"></div>
    <div :style="{ visibility: !isLoadingMask ? 'visible' : 'hidden' }">
      <div v-if="statisticByMonth === true">
        <el-form :inline="true" class="m-3">
          <el-form-item label="Month : ">
            <el-select
              v-model="searchData.month"
              placeholder="Pick a Month"
              @change="getDataByMonthYear"
            >
              <el-option
                v-for="item in monthInYear"
                :key="item"
                :label="item"
                :value="item"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Year : ">
            <el-date-picker
              v-model="searchData.year"
              type="year"
              placeholder="Pick a Year"
              value-format="yyyy"
              @change="getData"
            >
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <download-excel
              :fetch="fetchDataForExportExcel"
              :fields="json_fields"
              :worksheet="nameExportFile"
              title="Export Excel"
              :name="nameExportFile + '.xls'"
            >
              <el-button type="primary">
                <font-awesome-icon :icon="['fas', 'file-export']" />
                Export Data
              </el-button>
            </download-excel>
          </el-form-item>
        </el-form>
        <el-button class="ml-3" type="primary" @click="statisticChange()">
          {{ titleButton }}
        </el-button>
        <div v-if="leaveUser.length > 0 && series.length > 0">
          <div id="chart" v-if="loaded">
            <apexchart
              type="bar"
              height="450"
              :options="chartOptions"
              :series="series"
            ></apexchart>
          </div>
        </div>
        <div v-else class="text-center">
          <h2 class="text-danger">No data to show.</h2>
        </div>
      </div>
      <div v-else>
        <el-form :inline="true" class="m-3">
          <el-form-item label="Year : ">
            <el-date-picker
              v-model="searchData.year"
              type="year"
              placeholder="Pick a Year"
              value-format="yyyy"
              @change="getData"
            >
            </el-date-picker>
          </el-form-item>
        </el-form>
        <el-button class="ml-3" type="primary" @click="statisticChange()">
          {{ titleButton }}
        </el-button>
        <div v-if="leaveUser.length > 0 && series.length > 0">
          <div v-if="loaded">
            <apexchart
              type="bar"
              height="450"
              :options="chartOptions"
              :series="series"
            ></apexchart>
          </div>
        </div>
        <div v-else class="text-center">
          <h2 class="text-danger">No data to show.</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";
import StatisticDateOffService from "@/services/leave_management/statisticDateOffService";
import moment from "moment";

export default {
  name: "MyReport",
  data: () => ({
    loaded: false,
    isLoadingMask: true,
    searchData: {
      search: localStorage.getItem("name"),
      month: String(new Date().getMonth() + 1), //January is 0
      year: String(new Date().getFullYear()),
    },
    statisticByMonth: true,
    titleButton: "Statistic by Year",
    listTotalLeaveDays: [],
    listTypeOff: [],
    monthInYear: [],
    leaveUser: [],
    detailLeaveUser: [],
    json_fields: {
      Name: "name",
      Email: "email",
      Holidays: "holidays",
    },
    headers: [],
    series: [],
    chartOptions: {
      chart: {
        type: "bar",
        height: 300,
        stacked: true,
        toolbar: {
          show: true,
        },
        zoom: {
          enabled: true,
        },
      },
      responsive: [
        {
          breakpoint: 480,
          options: {
            legend: {
              position: "bottom",
              offsetX: -10,
              offsetY: 0,
            },
          },
        },
      ],
      plotOptions: {
        bar: {
          horizontal: false,
          borderRadius: 10,
        },
      },
      xaxis: {
        categories: ["Holidays", "Lefts Days"],
      },
      legend: {
        position: "right",
        offsetY: 40,
      },
      fill: {
        opacity: 1,
      },
    },
  }),
  computed: {
    nameExportFile() {
      return `My_report_${this.dates[0]}_to_${this.dates[1]}`;
    },
    dates() {
      const date = moment(
        `${this.searchData.year} ${this.searchData.month}`,
        "YYYY MM"
      );
      return [
        date.startOf("M").format("YYYY-MM-DD"),
        date.endOf("M").format("YYYY-MM-DD"),
      ];
    },
  },
  async created() {
    setTimeout(this.disableMask, 500);
    await this.getTypeOff();
    await this.getData();
    await this.getItemForExportTotal();
  },
  methods: {
    disableMask() {
      this.isLoadingMask = false;
    },

    async getTypeOff() {
      const res = await TypeOffAdminServices.getTypeOff();
      this.listTypeOff = res.data;
      for (let i = 0; i < this.listTypeOff.length; i++) {
        if (this.listTypeOff[i].type != 1) {
          let data = {
            text: `${this.listTypeOff[i].name} days in month`,
            value: `number_${this.listTypeOff[i].name}`,
            detail: `${this.listTypeOff[i].name}`,
          };
          this.headers.push(data);
          this.listTotalLeaveDays.push(0);
        }
      }
    },

    async getData() {
      this.monthInYear = [];
      const res = await StatisticDateOffService.getByUser(this.searchData.year);
      if (res.data.length > 0) {
        this.leaveUser = res.data;
        for (const detail in this.leaveUser) {
          this.monthInYear.push(this.leaveUser[detail].month);
        }
        if (this.statisticByMonth === true) {
          this.titleButton = "Statistic by Year";
          this.getDataByMonthYear();
        } else {
          this.titleButton = "Statistic by Month";
          this.getDataByYear();
        }
      } else this.leaveUser = [];
    },

    getDataByMonthYear() {
      this.loaded = false;
      const monthHoliday = {
        name: "Holidays",
        data: [this.getDetailData(this.searchData.month, "holidays"), 0],
      };
      this.series = [];
      this.series.push(monthHoliday);
      for (const header in this.headers) {
        // find number date off of leave type
        const temp = this.getDetailData(
          this.searchData.month,
          this.headers[header].value
        );
        if (temp) {
          const leftsDay = {
            name: this.headers[header].detail,
            data: [0, temp],
          };
          this.series.push(leftsDay);
        } else {
          const leftsDay = {
            name: this.headers[header].detail,
            data: [0, 0],
          };
          this.series.push(leftsDay);
        }
      }
      this.loaded = true;
    },

    getDataByYear() {
      this.loaded = false;
      this.series = [];
      for (let i = 0; i < this.listTypeOff.length; i++) {
        this.listTotalLeaveDays[i] = 0;
      }
      let holidayYear = 0;
      for (const detail in this.leaveUser) {
        holidayYear += this.leaveUser[detail].holidays;
        for (const header in this.headers) {
          this.listTotalLeaveDays[header] +=
            this.leaveUser[detail][this.headers[header].value];
        }
      }
      // add data to series
      const holidayFullYear = {
        name: "Holidays",
        data: [holidayYear, 0],
      };
      this.series.push(holidayFullYear);
      for (const header in this.headers) {
        const leftDay = {
          name: this.headers[header].detail,
          data: [0, this.listTotalLeaveDays[header]],
        };
        this.series.push(leftDay);
      }
      this.loaded = true;
    },

    getDetailData(month, value) {
      return this.leaveUser.find((date) => date.month === parseInt(month))[
        value
      ];
    },

    statisticChange() {
      this.statisticByMonth = !this.statisticByMonth;
      if (this.statisticByMonth === false) {
        this.titleButton = "Statistic by Month";
        this.getDataByYear();
      } else {
        this.titleButton = "Statistic by Year";
        this.getDataByMonthYear();
      }
    },

    async fetchDataForExportExcel() {
      const [start_date, end_date] = this.dates;
      const res = await StatisticDateOffService.getByAdmin({
        ...this.searchData,
        start_date,
        end_date,
      });
      if (res.data.results.length) {
        return res.data.results;
      } else {
        this.$toast.error("No data to export");
      }
    },

    getItemForExportTotal() {
      for (let i = 0; i < this.listTypeOff.length; i++) {
        this.json_fields[
          `Number of ${this.listTypeOff[i].name} days`
        ] = `number_${this.listTypeOff[i].name}`;
        this.json_fields[`${this.listTypeOff[i].name} days detail`] = {
          field: `${this.listTypeOff[i].name}`,
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
  },
};
</script>

<style lang="scss" scoped>
.lmask {
  position: sticky;
  height: calc(100vh - 110px);
  width: 100%;
  bottom: 0;
  left: 0;
  right: 0;
  top: 0;
  z-index: 0;
  opacity: 0.4;

  &.fixed {
    position: fixed;
  }

  &:before {
    content: "";
    background-color: rgba(0, 0, 0, 0);
    border: 5px solid rgba(0, 183, 229, 0.9);
    opacity: 0.9;
    border-right: 5px solid rgba(0, 0, 0, 0);
    border-left: 5px solid rgba(0, 0, 0, 0);
    border-radius: 50px;
    box-shadow: 0 0 35px #2187e7;
    width: 50px;
    height: 50px;
    -moz-animation: spinPulse 1s infinite ease-in-out;
    -webkit-animation: spinPulse 1s infinite linear;

    margin: -25px 0 0 -25px;
    position: absolute;
    top: 50%;
    left: 50%;
  }

  &:after {
    content: "";
    background-color: rgba(0, 0, 0, 0);
    border: 5px solid rgba(0, 183, 229, 0.9);
    opacity: 0.9;
    border-left: 5px solid rgba(0, 0, 0, 0);
    border-right: 5px solid rgba(0, 0, 0, 0);
    border-radius: 50px;
    box-shadow: 0 0 15px #2187e7;
    width: 30px;
    height: 30px;
    -moz-animation: spinoffPulse 1s infinite linear;
    -webkit-animation: spinoffPulse 1s infinite linear;

    margin: -15px 0 0 -15px;
    position: absolute;
    top: 50%;
    left: 50%;
  }
}

@-moz-keyframes spinPulse {
  0% {
    -moz-transform: rotate(160deg);
    opacity: 0;
    box-shadow: 0 0 1px #2187e7;
  }
  50% {
    -moz-transform: rotate(145deg);
    opacity: 1;
  }
  100% {
    -moz-transform: rotate(-320deg);
    opacity: 0;
  }
}

@-moz-keyframes spinoffPulse {
  0% {
    -moz-transform: rotate(0deg);
  }
  100% {
    -moz-transform: rotate(360deg);
  }
}

@-webkit-keyframes spinPulse {
  0% {
    -webkit-transform: rotate(160deg);
    opacity: 0;
    box-shadow: 0 0 1px #2187e7;
  }
  50% {
    -webkit-transform: rotate(145deg);
    opacity: 1;
  }
  100% {
    -webkit-transform: rotate(-320deg);
    opacity: 0;
  }
}

@-webkit-keyframes spinoffPulse {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}
</style>
