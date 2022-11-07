<template>
  <div class="bg-light">
    <div v-if="isLoadingMask" class="lmask" ref="loading-mask"></div>
    <div :style="{ visibility: !isLoadingMask ? 'visible' : 'hidden' }">
      <el-form :inline="true" class="m-3">
        <div class="d-flex flex-row">
          <el-form-item label="Team : ">
            <el-select v-model="searchData.team" @change="changeTeam()">
              <el-option
                v-for="item in teams"
                :key="item.id"
                :label="item.team_name"
                :value="item.id"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Member : ">
            <el-select
              v-model="searchData.member"
              placeholder="Pick a member"
              clearable
            >
              <el-option
                v-for="item in teamChooseMembers"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              >
                {{ item.name }}
                <span v-if="item.user_id == teamChoose.team_leader">
                  (Leader)
                </span>
              </el-option>
            </el-select>
          </el-form-item>
          <div>
            <el-form-item label="Month : ">
              <el-date-picker
                v-model="dateSearch"
                type="monthrange"
                range-separator="-"
                start-placeholder="Start month"
                end-placeholder="End month"
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
          </div>
        </div>
      </el-form>
      <div v-if="leaveUser.length > 0 && series.length > 0">
        <div>
          <apexchart
            type="bar"
            height="450"
            :options="chartOptions"
            :series="series"
          >
          </apexchart>
        </div>
      </div>
      <div v-else class="text-center">
        <h2 class="text-danger">No data to show.</h2>
      </div>
    </div>
  </div>
</template>

<script>
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";
import StatisticDateOffService from "@/services/leave_management/statisticDateOffService";
import moment from "moment";
import TeamServices from "@/services/team/team.services";

export default {
  name: "TeamReport",
  data() {
    return {
      isLoadingMask: true,
      leaveUser: [],
      listTypeOff: [],
      teams: [],
      teamChoose: {},
      teamChooseMembers: [],
      listTotalLeaveDays: [],
      headers: [],
      json_fields: {
        Name: "name",
        Email: "email",
        Holidays: "holidays",
      },
      searchData: {
        profile: localStorage.getItem("profile_id"),
        team: "",
        member: "",
      },
      dateSearch: [new Date(), new Date()],
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
    };
  },
  watch: {
    "searchData.member": function () {
      this.memberChange();
    },
    dateSearch: function () {
      this.getData();
    },
  },
  computed: {
    nameExportFile() {
      if (this.dateSearch) {
        return `Team_report_${this.dates[0]}_to_${this.dates[1]}`;
      }
      return "Team_report_all_day";
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
  async created() {
    setTimeout(this.disableMask, 500);
    await this.getTypeOff();
    await this.getTeams();
    await this.getData();
    await this.getItemForExportTotal();
  },
  methods: {
    changeTeam() {
      const team = this.teams.find((data) => data.id == this.searchData.team);
      this.teamChooseMembers = team.members;
      this.teamChoose = team;
      this.searchData.team = team.team_name;
      this.searchData.member = "";
      this.getData();
    },

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

    async getTeams() {
      const res = await TeamServices.getMyTeams();
      if (res) {
        this.teams = res.data;
        this.searchData.team = this.teams[0].team_name;
        this.teamChooseMembers = this.teams[0].members;
        this.teamChoose = this.teams[0];
      } else {
        this.$toast.error("Error loading user's teams");
      }
    },

    async getData() {
      this.series = [];
      this.leaveUser = [];
      this.listTotalLeaveDays.fill(0);
      const [start_date, end_date] = this.dates;
      const res = await StatisticDateOffService.getMyTeam({
        ...this.searchData,
        start_date,
        end_date,
      });
      if (res.data) {
        this.leaveUser = res.data;
        await this.memberChange();
      }
    },

    getDetailData(name, value) {
      return this.leaveUser.find((data) => data.name === name)[value];
    },

    memberChange() {
      this.series = [];
      if (this.searchData.member) {
        const detailUser = this.leaveUser.find(
          (data) => data.id === this.searchData.member
        );
        const holidays = {
          name: "Holidays",
          data: [detailUser.holidays, 0],
        };
        this.series = [
          holidays,
          ...this.headers.map((header) => {
            return {
              name: header.detail,
              data: [0, detailUser[header.value]],
            };
          }),
        ];
      } else {
        this.getDataChange();
      }
    },

    getDataChange() {
      const holidayTotal = this.leaveUser.reduce(
        (res, detail) => res + detail.holidays,
        0
      );
      this.headers.forEach((header, index) => {
        this.listTotalLeaveDays[index] = this.leaveUser.reduce(
          (res, detail) => res + detail[header.value],
          0
        );
      });
      // add data to series
      const holidays = {
        name: "Holidays",
        data: [holidayTotal / (this.teamChooseMembers.length - 1), 0],
      };
      this.series = [
        holidays,
        ...this.headers.map((header, index) => {
          return {
            name: header.detail,
            data: [0, this.listTotalLeaveDays[index]],
          };
        }),
      ];
    },

    async fetchDataForExportExcel() {
      if (this.leaveUser.length) {
        return this.leaveUser;
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
