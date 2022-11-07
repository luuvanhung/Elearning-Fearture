<template>
  <div class="mt-3">
    <sync-buttons @refreshDesserts="asyncDataActive"></sync-buttons>
    <div class="d-flex">
      <div class="mr-auto p-2">
        <FilterBox
          :page_size="pageSize"
          @searchRequest="searchRequest"
          :searchData="this.searchData"
        />
      </div>
      <Button
        :leaveRequestsUpdate="leaveRequestsUpdate"
        :page="page"
        :lastPageCount="lastPageCount"
        :searchData="searchData"
        @searchRequest="searchRequest"
      />
    </div>
    <LeaveRequestTable
      :requestOffsData="requestsData.rows"
      :isOfficer="true"
      @handleUpdateStatusLeaveRequest="handleUpdateStatusLeaveRequest"
    />
    <div class="d-flex justify-content-center mt-5">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="pageSize"
        :page-count="requestsData.totalPage"
        :current-page="requestsData.currentPage"
        @current-change="setPage"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import RequestOffService from "@/services/leave_management/request_off/request_off.services";
import syncButtons from "@/pages/leaveManage/officeRequest/sync-buttons.vue";
import FilterBox from "@/pages/leaveManage/components/filter.vue";
import Button from "@/pages/leaveManage/components/button.vue";
import LeaveRequestTable from "@/pages/leaveManage/components/leaveRequestTable";
import { formatDate } from "@/utils/time";

export default {
  name: "OfficeRequest",
  middleware: "authentication",
  components: {
    syncButtons,
    FilterBox,
    LeaveRequestTable,
    Button,
  },

  data() {
    return {
      page: 1,
      pageSize: 10,
      lastPageCount: 0,
      requestsData: {
        searching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
      },
      leaveRequestsUpdate: [],
      searchData: {
        nameOrEmail: "",
        date: [],
        typeLeave: "",
        status: "",
      },
    };
  },

  async created() {
    await this.asyncDataActive();
  },

  methods: {
    formatDate,
    async setPage(page) {
      this.page = page;
      await this.getDataFilterOption();
    },

    getDataFilterOption() {
      if (this.requestsData.searching) {
        this.searchRequest(this.page, this.searchData);
      } else this.asyncDataActive(this.page);
    },

    async asyncDataActive() {
      let responseData = await RequestOffService.getAllRequest(
        this.page,
        this.pageSize
      );
      if (responseData) {
        this.loadData(responseData, false);
      }
    },

    handleUpdateStatusLeaveRequest(selection) {
      this.leaveRequestsUpdate = selection;
    },

    loadData: function (responseData, isSearching) {
      this.requestsData.searching = isSearching;
      this.requestsData.rows = responseData.results;
      this.requestsData.totalPage = responseData.page_number;
      this.requestsData.currentPage = responseData.current;
      let totalData = responseData.count;
      this.lastPageCount =
        totalData - Math.floor(totalData / this.pageSize) * this.pageSize;
      this.lastPageCount =
        this.lastPageCount > 0 ? this.lastPageCount : this.pageSize;
    },

    async searchRequest(page = this.page, searchData = this.searchData) {
      this.page = page;
      this.searchData = searchData;
      let nameOrEmail = this.searchData.nameOrEmail.trim();
      let fromDate = null;
      let toDate = null;
      let typeLeave = this.searchData.typeLeave;
      let status = this.searchData.status;
      if (this.searchData.date) {
        fromDate = this.formatDate(this.searchData.date[0]);
        toDate = this.formatDate(this.searchData.date[1]);
      }
      const responseData = await RequestOffService.searchRequest({
        name_or_email: nameOrEmail,
        from_date: fromDate,
        to_date: toDate,
        type_leave: typeLeave,
        status: status,
        page: this.page,
        page_size: this.pageSize,
      });
      if (responseData && responseData.data) {
        this.loadData(responseData.data, true);
      }
    },
  },
};
</script>

<style scoped></style>
