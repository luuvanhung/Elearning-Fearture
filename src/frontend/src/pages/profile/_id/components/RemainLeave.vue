<template>
  <div class="general-infor">
    <el-card class="box-card mb-4 card-detail">
      <div slot="header" class="clearfix">
        <span class="card-title">Remain Leave Information</span>
      </div>
      <el-table
        :data="remainLeaves"
        header-cell-class-name="bg-header-table"
        :cell-class-name="checkAvailableDays"
        stripe
        style="width: 100%"
        border
        class="leaveData"
      >
        <el-table-column label="Last year" align="center">
          <el-table-column label="Remain" align="center">
            <div>{{ remainLeaveLastYear.remain_last_year }}</div>
          </el-table-column>
          <el-table-column label="Taken" align="center">
            <div>{{ remainLeaveLastYear.used_day_off }}</div>
          </el-table-column>
          <el-table-column
            label="Available"
            align="center"
            prop="allowLastYear"
          >
            <el-tooltip
              class="item"
              effect="light"
              :content="`Remain last year is expired!`"
              placement="bottom"
              v-if="remainLeaveLastYear.is_expired"
            >
              <div>{{ remainLeaveLastYear.allowed_day_off }}</div>
            </el-tooltip>
            <div v-else>{{ remainLeaveLastYear.allowed_day_off }}</div>
          </el-table-column>
        </el-table-column>
        <el-table-column
          v-if="visibleBonusLeaveCard"
          label="Bonus leave"
          align="center"
        >
          <el-table-column label="Total bonus" align="center">
            <div>{{ bonusLeaveDetail.total_bonus }}</div>
          </el-table-column>
          <el-table-column label="Taken" align="center">
            <div>{{ bonusLeaveDetail.used_day_off }}</div>
          </el-table-column>
          <el-table-column label="Available" align="center" prop="allowBonus">
            <div>{{ bonusLeaveDetail.allowed_day_off }}</div>
          </el-table-column>
        </el-table-column>
        <el-table-column label="This year" align="center">
          <el-table-column label="Annual leave" align="center">
            <div>{{ leaveCurrentYear.annual_leave }}</div>
          </el-table-column>
          <el-table-column label="Seniority year" align="center">
            <div>{{ leaveCurrentYear.seniority_year }}</div>
          </el-table-column>
          <el-table-column label="Taken" align="center">
            <div>{{ leaveCurrentYear.used_day_off }}</div>
          </el-table-column>
          <el-table-column label="Available" align="center" prop="allowAnnual">
            <div>{{ leaveCurrentYear.allowed_day_off }}</div>
          </el-table-column>
        </el-table-column>
      </el-table>
      <el-card
        class="box-card mb-2 mt-3 card-detail"
        v-show="visibleBonusLeaveCard"
      >
        <div slot="header" class="clearfix">
          <span class="card-title" style="font-size: 20px">Bonus Leave</span>
        </div>
        <el-table
          :data="bonusLeaveData"
          stripe
          header-cell-class-name="bg-header-table"
          style="width: 100%"
          border
        >
          <el-table-column type="index" label="No" width="45" align="center">
          </el-table-column>
          <el-table-column
            prop="bonus_types"
            label="Bonus types"
            sortable
            align="center"
          >
            <template v-slot:default="table">
              {{ table.row.bonus_type.name }}
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="Reason" sortable align="center">
          </el-table-column>
          <el-table-column
            prop="bonus_days"
            label="Bonus Leave Days"
            sortable
            align="center"
          >
          </el-table-column>
          <el-table-column
            prop="created_at"
            label="Create at"
            width="180"
            sortable
            align="center"
          >
          </el-table-column>
        </el-table>
        <div class="mt-4 ml-1">
          You have total {{ bonusLeaveDate }} bonus days in this year.
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script>
import RemainLeaveService from "@/services/leave_management/remain_leave/remain_leave.services";
import { required } from "vuelidate/lib/validators";
import moment from "moment";
import BonusLeaveService from "@/services/leave_management/bonus_leave/bonus_leave.services";

const NO_DATA = "Empty";

export default {
  name: "RemainLeave",
  data() {
    return {
      dataInfo: null,
      userId: Number,
      remainLeaves: [],
      remainLeaveLastYear: {
        remain_last_year: 0,
        used_day_off: 0,
        allowed_day_off: 0,
        is_expired: false,
      },
      bonusLeaveDetail: {
        total_bonus: 0,
        used_day_off: 0,
        allowed_day_off: 0,
      },
      leaveCurrentYear: {
        annual_leave: 0,
        seniority_year: 0,
        used_day_off: 0,
        allowed_day_off: 0,
      },
      bonusLeaveData: [],
      visibleBonusLeaveCard: false,
      bonusLeaveDate: 0,
      profileTemp: "",
      yearNow: moment().year(),
      NO_DATA,
    };
  },
  async created() {
    this.userId = this.$route.params.id;
    await this.fetchDataForRemainLeave();
    await this.fetchDataForBonusLeave();
  },
  methods: {
    checkAvailableDays({ row, column }) {
      if (
        column.property === "allowBonus" ||
        column.property === "allowAnnual"
      ) {
        return "availableClass";
      }
      if (column.property === "allowLastYear") {
        return this.remainLeaveLastYear.is_expired
          ? "expiredClass"
          : "availableClass";
      }
    },
    async fetchDataForRemainLeave() {
      const response = await RemainLeaveService.getRemainLeaveUser(this.userId);
      if (response && response.status === 200) {
        this.remainLeaves = [response.data];
        this.bonusLeaveDetail = response.data.bonus_leave_details;
        this.remainLeaveLastYear = response.data.remain_last_year;
        this.leaveCurrentYear = response.data.leave_current_year;
        this.profileTemp = response.data.profile;
      }
    },
    async fetchDataForBonusLeave(id) {
      const response = await BonusLeaveService.getBonusLeaveUserInYear(
        this.userId
      );
      if (response && response.status === 200) {
        this.bonusLeaveData = response.data;
        if (this.bonusLeaveData.length !== 0) {
          this.visibleBonusLeaveCard = true;
          this.bonusLeaveData.forEach((bonus) => {
            this.bonusLeaveDate += bonus.bonus_days;
          });
        }
        this.remainLeaves[0].bonusLeaveDate = this.bonusLeaveDate;
      }
    },
  },
};
</script>

<style lang="scss">
.el-table--enable-row-hover .el-table__body tr:hover > td {
  background-color: initial;
}
.availableClass {
  background-color: #a8da98 !important;
}
.expiredClass {
  background-color: #df8888 !important;
}
</style>
