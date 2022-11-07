<template>
  <div class="mt-3">
    <div class="d-flex">
      <div class="mr-auto p-2">
        <FilterBox
          @searchRequest="searchRequest"
          :searchData="this.searchData"
          :page_size="pageSize"
        />
      </div>
      <Button
        :leaveRequestsUpdate="leaveRequestsUpdate"
        :lastPageCount="lastPageCount"
        :page="page"
        :searchData="searchData"
        @searchRequest="searchRequest"
      />
    </div>
    <LeaveRequestTable
      :requestOffsData="requestOffsData.rows"
      :isOfficer="false"
      @handleUpdateStatusLeaveRequest="handleUpdateStatusLeaveRequest"
    />
    <div class="d-flex justify-content-center mt-5">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="pageSize"
        :page-count="requestOffsData.totalPage"
        :current-page="requestOffsData.currentPage"
        @current-change="setPage"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import ManagementLeaveService from "@/services/leave_management/managementLeave.service";
import FilterBox from "@/pages/leaveManage/components/filter.vue";
import Button from "@/pages/leaveManage/components/button.vue";
import LeaveRequestTable from "@/pages/leaveManage/components/leaveRequestTable";
import { formatDate } from "@/utils/time";

export default {
  name: "Approval",
  middleware: "authentication",
  async created() {
    await this.asyncDataActive();
  },

  components: {
    FilterBox,
    LeaveRequestTable,
    Button,
  },

  data() {
    return {
      page: 1,
      lastPageCount: 0,
      pageSize: 10,
      isApprove: false,
      editedIndexRequest: -1,
      leaveRequestsUpdate: [],
      requestOffsData: {
        isSearching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
        count: 0,
      },
      searchData: {
        nameOrEmail: "",
        date: [],
        typeLeave: "",
        status: "",
      },
    };
  },

  methods: {
    formatDate,
    async setPage(page) {
      this.page = page;
      await this.getDataFilterOption();
    },

    getDataFilterOption() {
      if (this.requestOffsData.searching) {
        this.searchRequest(this.page, this.searchData);
      } else this.asyncDataActive(this.page);
    },

    async asyncDataActive() {
      const responseData = await ManagementLeaveService.getManagementRequestOff(
        this.page,
        this.pageSize
      );
      if (responseData) {
        this.loadData(responseData, false);
      }
    },

    loadData: function (responseData, isSearching) {
      this.requestOffsData.isSearching = isSearching;
      this.requestOffsData.rows = responseData.data.results.map(
        (request) => request.request_off
      );
      this.requestOffsData.totalPage = responseData.data.page_number;
      this.requestOffsData.currentPage = responseData.data.current;
      let totalData = responseData.data.count;
      this.lastPageCount =
        totalData - Math.floor(totalData / this.pageSize) * this.pageSize;
      this.lastPageCount =
        this.lastPageCount > 0 ? this.lastPageCount : this.pageSize;
    },

    handleUpdateStatusLeaveRequest(selection) {
      this.leaveRequestsUpdate = selection;
    },

    async searchRequest(page = this.page, searchData = this.searchData) {
      this.page = page;
      this.searchData = searchData;
      const nameOrEmail = this.searchData.nameOrEmail.trim();
      let fromDate = null;
      let toDate = null;
      const typeLeave = this.searchData.typeLeave;
      const status = this.searchData.status;
      if (this.searchData.date) {
        fromDate = this.formatDate(this.searchData.date[0]);
        toDate = this.formatDate(this.searchData.date[1]);
      }
      const responseData = await ManagementLeaveService.searchManageRequestOff({
        name_or_email: nameOrEmail,
        from_date: fromDate,
        to_date: toDate,
        type_leave: typeLeave,
        status: status,
        page: this.page,
        page_size: this.pageSize,
      });
      if (responseData && responseData.data) {
        this.loadData(responseData, true);
      }
    },
  },
};
</script>

<style lang="scss">
@import "./style.scss";
</style>
