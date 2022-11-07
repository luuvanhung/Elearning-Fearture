<template>
  <div>
    <FilterBox @loadData="loadData" :page_size="page_size" ref="filter" />
    <div class="mt-3">
      <el-table
        highlight-current-row
        :data="requestsData.rows"
        header-cell-class-name="bg-header-table"
        border
      >
        <el-table-column sortable prop="user.name" label="Employee">
          <template slot-scope="scope">
            <div class="text-center">
              {{ scope.row.user.name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="Email" align="center">
          <template slot-scope="scope">
            {{ scope.row.user.email }}
          </template>
        </el-table-column>
        <el-table-column label="Date Off" width="200" align="center">
          <template slot-scope="scope">
            <div v-for="date in scope.row.wfh_date" :key="date.id">
              {{ date.date }}
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
          label="Total Days"
          align="center"
        ></el-table-column>
      </el-table>
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
  </div>
</template>

<script>
import RequestWfhService from "@/services/wfh_management/request_wfh/request_wfh.services";
import FilterBox from "@/pages/wfhManage/wfhofficeRequest/filter.vue";
export default {
  name: "WFHOfficeRequest",
  components: {
    FilterBox,
  },
  data() {
    return {
      page_size: 10,
      desserts: [],
      requestsData: {
        searching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
      },
    };
  },
  async created() {
    await this.asyncDataActive(1);
  },
  methods: {
    getDataFilterOption(page = 1) {
      if (this.requestsData.searching) {
        this.$refs.filter.search(page);
      } else this.asyncDataActive(page);
    },
    changePage(page) {
      this.getDataFilterOption(page);
    },
    async asyncDataActive(page) {
      const response = await RequestWfhService.getAllRequest(
        page,
        this.page_size
      );
      if (response) this.loadData(response, false);
    },
    loadData: function (responseData, isSearching) {
      this.requestsData.searching = isSearching;
      this.requestsData.rows = responseData.results;
      this.requestsData.currentPage = responseData.current;
      this.requestsData.totalPage = responseData.page_number;
    },
  },
};
</script>
<style scoped></style>
