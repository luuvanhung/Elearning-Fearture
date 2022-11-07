<template>
  <div>
    <div>
      <el-card>
        <div>
          <el-button
            type="primary"
            icon="el-icon-circle-plus"
            @click="addNewRequest"
          >
            New WFH Request
          </el-button>
        </div>
      </el-card>
      <el-table
        highlight-current-row
        :data="requestsData.rows"
        header-cell-class-name="bg-header-table"
        border
      >
        <el-table-column label="Dates" width="240" align="center">
          <template slot-scope="scope">
            <div v-for="WFHdate in scope.row.wfh_date" :key="WFHdate.id">
              {{ WFHdate.date }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="reason"
          label="Reason"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="total"
          label="Total"
          align="center"
        ></el-table-column>
      </el-table>
    </div>
    <div class="d-flex justify-content-center mt-5">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="page_size"
        :page-count="requestsData.totalPage"
        :current-page="requestsData.currentPage"
        @current-change="changePage"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import RequestWfhService from "@/services/wfh_management/request_wfh/request_wfh.services";

export default {
  name: "WFHRequest",
  data() {
    return {
      dialog: false,
      year: moment().year(),
      month: moment().month(),
      wfhRequests: [],
      Reason: 0,
      page_size: 10,
      requestsData: {
        totalPage: 0,
        currentPage: 1,
        rows: [],
      },
    };
  },
  created() {
    this.getWfhRequest(1);
  },
  methods: {
    addNewRequest() {
      this.$router.push("workfromhome/new-request");
    },
    changePage(page) {
      this.getWfhRequest(page);
    },
    async getWfhRequest(page) {
      const res = await RequestWfhService.getMyWfhRequest(page, this.page_size);
      if (res) this.loadData(res);
    },
    loadData(responseData) {
      this.requestsData.totalPage = responseData.page_number;
      this.requestsData.currentPage = responseData.current;
      this.requestsData.rows = responseData.results;
    },
  },
};
</script>

<style scoped></style>
