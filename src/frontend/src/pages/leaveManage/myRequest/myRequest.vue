<template>
  <div>
    <el-card class="mb-3">
      <div>
        <el-button
          type="primary"
          icon="el-icon-circle-plus"
          @click="addNewRequest"
        >
          New Request
        </el-button>
      </div>
    </el-card>
    <el-table
      highlight-current-row
      :data="requestsData.rows"
      header-cell-class-name="bg-header-table"
      border
    >
      <el-table-column label="List Date Off" width="240" align="center">
        <template slot-scope="scope">
          <div v-for="dateOff in scope.row.date_off" :key="dateOff.id">
            {{ dateOff.date }} ({{ dateOff.type }})
          </div>
        </template>
      </el-table-column>
      <el-table-column
        sortable
        prop="leave_type.name"
        label="Leave Type"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="reason"
        label="Reason"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="request_detail[0]"
        label="Assigned"
        align="center"
      ></el-table-column>
      <el-table-column sortable prop="total" label="Total Leaves" width="130">
        <template slot-scope="scope">
          <div class="text-center">
            {{ scope.row.total }}
          </div>
        </template>
      </el-table-column>
      <el-table-column sortable prop="status" label="Status" width="200">
        <template slot-scope="scope">
          <div class="text-center">
            <div v-if="scope.row.status === 'Approved'">
              <el-tag type="success"> Approved </el-tag>
            </div>
            <div v-else-if="scope.row.status === 'Rejected'">
              <el-tag type="danger"> Rejected </el-tag>
            </div>
            <div v-else-if="scope.row.status === 'Canceling'">
              <el-tag type="warning"> Canceling </el-tag>
            </div>
            <div v-else-if="scope.row.status === 'Canceled'">
              <el-tag type="info"> Canceled </el-tag>
            </div>
            <div v-else>
              <el-tag type="warning"> Pending </el-tag>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column sortable prop="action" label="Action" width="150">
        <template slot-scope="scope">
          <div class="text-center">
            <div v-if="scope.row.status === 'Pending'">
              <el-row>
                <el-button round type="danger" @click="cancelDialog(scope.row)">
                  Cancel
                </el-button>
              </el-row>
            </div>
          </div>
        </template>
      </el-table-column>
    </el-table>
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
    <el-dialog title="Cancel Request" :visible.sync="dialog">
      <div class="text-center text-danger">
        <h2>Do you want to cancel this request ?</h2>
      </div>
      <div class="mt-3 text-center">
        <el-button type="primary" @click="cancelRequest()">Confirm</el-button>
        <el-button type="danger" @click="closeDialog()">Cancel</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import moment from "moment";
import RequestOffService from "@/services/leave_management/request_off/request_off.services";
import ManagementLeaveService from "@/services/leave_management/managementLeave.service";
import { mapActions } from "vuex";
import GetUserService from "@/services/user/getUser";
export default {
  name: "MyRequest",
  data() {
    return {
      dialog: false,
      year: moment().year(),
      month: moment().month(),
      requestsData: {
        searching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
      },
      editedIndexRequest: -1,
      actionItem: {
        action: "",
        request_off: {
          id: "",
          profile: {
            name: "",
          },
        },
        Date: 0,
        Reason: 0,
        Status: 0,
        comment: "",
      },
      page: 1,
      pageSize: 10,
    };
  },

  async created() {
    await this.getRequestOffs();
    await GetUserService.getAllTitles().then((res) => {
      this.getListTitle(res.data);
    });
  },

  methods: {
    ...mapActions({
      getListTitle: "title/updateListTitle",
    }),

    async setPage(page) {
      this.page = page;
      await this.getRequestOffs();
    },

    addNewRequest() {
      this.$router.push("/leaves/new-request");
    },

    async getRequestOffs() {
      const responseData = await RequestOffService.getMyRequest(
        this.page,
        this.pageSize
      );
      if (responseData) {
        this.loadData(responseData, false);
      }
    },

    loadData: function (responseData, isSearching) {
      this.requestsData.searching = isSearching;
      this.requestsData.rows = responseData.results;
      this.requestsData.totalPage = responseData.page_number;
      this.requestsData.currentPage = responseData.current;
    },

    cancelDialog(requestItem) {
      this.editedIndex = this.requestsData.rows.indexOf(requestItem);
      this.$set(this.actionItem, "action", "Canceling");
      this.actionItem = Object.assign({}, requestItem);
      this.$set(this.actionItem, "action", "Canceling");
      this.dialog = true;
    },

    closeDialog() {
      this.dialog = false;
      this.$nextTick(() => {
        this.actionItem = {};
      });
    },

    async cancelRequest() {
      let data = {
        comment: "Cancel Request",
        request_off_ids: [this.actionItem.id],
        action: this.actionItem.action,
      };
      await ManagementLeaveService.actionRequest(data);
      this.closeDialog();
      await this.getRequestOffs();
    },
  },
};
</script>

<style scoped></style>
