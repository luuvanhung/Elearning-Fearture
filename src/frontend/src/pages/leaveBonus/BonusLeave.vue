<template>
  <div>
    <div class="mt-3">
      <div class="d-flex">
        <div class="mr-auto p-2">
          <FilterIndex
            @searchRequest="searchRequest"
            :searchData="searchData"
            :page_size="pageSize"
            :optionsBonusType="optionsBonusType"
            ref="filter"
          />
        </div>
        <div class="p-2">
          <restricted-view :scopes="[SCOPES['BonusLeaveEdit']]">
            <div class="d-flex justify-content-end mb-3">
              <el-button round type="danger" @click="handleDeleteMultiple">
                Delete
              </el-button>
              <el-button type="primary" round @click="dialogBonusLeave = true">
                <font-awesome-icon :icon="['fas', 'user-plus']" />
                <span class="ml-2">Add Bonus</span>
              </el-button>
            </div>
          </restricted-view>
        </div>
      </div>
      <el-table
        :data="bonusLeaveData.rows"
        stripe
        @selection-change="handleSelectionChange"
        header-cell-class-name="bg-header-table"
        style="width: 100%"
      >
        <el-table-column type="selection" align="center"></el-table-column>
        <el-table-column
          prop="bonus_type"
          label="Bonus types"
          sortable
          align="center"
        >
          <template v-slot:default="table">
            {{ table.row.bonus_type.name }}
          </template>
        </el-table-column>
        <el-table-column
          prop="profile.name"
          label="Name"
          width="180"
          sortable
          align="center"
        >
          <template v-slot:default="table">
            <router-link
              :to="`/profile/${table.row.profile.user_id}`"
              title="Click to move to Profile page"
              tag="a"
              prop="profile.name"
            >
              <strong>{{ table.row.profile.name }}</strong>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
          prop="profile.personal_email"
          label="Email"
          align="center"
        />
        <el-table-column
          prop="bonus_days"
          label="Bonus Leave Days"
          sortable
          align="center"
        >
        </el-table-column>
        <el-table-column prop="reason" label="Reason" sortable align="center">
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="Created at"
          width="180"
          sortable
          align="center"
        >
        </el-table-column>
        <el-table-column label="Actions" width="150" align="center">
          <template v-slot="scope">
            <restricted-view :scopes="[SCOPES['BonusLeaveEdit']]">
              <template v-slot:default>
                <el-button
                  circle
                  style="cursor: pointer"
                  @click="editRequest(scope.row)"
                  title="Edit BonusLeave"
                  type="primary"
                  icon="el-icon-edit"
                ></el-button>
                <el-button
                  circle
                  style="cursor: pointer"
                  type="danger"
                  icon="el-icon-delete"
                  @click="deleteRequest(scope.row.id)"
                  title="Delete Probation Template"
                />
              </template>
            </restricted-view>
          </template>
        </el-table-column>
      </el-table>
      <div class="d-flex justify-content-center mt-5">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="pageSize"
          :page-count="bonusLeaveData.totalPage"
          :current-page="bonusLeaveData.currentPage"
          :total="bonusLeaveData.count"
          @current-change="setPage"
        >
        </el-pagination>
      </div>
    </div>
    <el-dialog
      title="Delete"
      :visible.sync="dialogVisible"
      width="30%"
      class="dialog"
    >
      <span>Do you want to delete this template ?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="deleteBonusLeaves()"
          >Confirm</el-button
        >
      </span>
    </el-dialog>
    <el-dialog
      title="Bonus Leaves"
      width="80%"
      :visible.sync="dialogBonusLeave"
    >
      <BonusLeave
        :optionsBonusType="optionsBonusType"
        @getData="searchRequest"
      />
    </el-dialog>
    <el-dialog
      title="Edit Bonus Leaves"
      width="80%"
      :visible.sync="dialogEditBonusLeave"
    >
      <EditBonusLeave
        :optionsBonusType="optionsBonusType"
        :visible="dialogEditBonusLeave"
        :oldBonusLeave="oldBonusLeave"
        @handleEditData="handleData"
      />
    </el-dialog>
  </div>
</template>

<script>
import FilterIndex from "@/pages/leaveBonus/filterIndex";
import BonusLeave from "@/pages/leaveBonus/bonusLeaveModel";
import EditBonusLeave from "@/pages/leaveBonus/editBonusLeave";
import { SCOPES } from "@/const/scopes";

import BonusLeaveService from "@/services/leave_management/bonus_leave/bonus_leave.services.js";
import BonusTypeService from "@/services/leave_management/bonus_leave/bonus_type.services.js";
import "vue2-datepicker/index.css";
import { formatDate } from "@/utils/time";
import RestrictedView from "@/components/RestrictedView";

export default {
  components: {
    FilterIndex,
    BonusLeave,
    EditBonusLeave,
    RestrictedView,
  },
  name: "leaveBonus",
  middleware: "authentication",
  data() {
    return {
      pageInfo: {
        pageNumber: "",
        previous: "",
        next: "",
      },
      errors: "",
      pageSize: 8,
      page: 1,
      bonusLeaveData: {
        searching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
        countLastPage: 0,
      },
      optionsBonusType: [],
      oldBonusLeave: null,
      dialogBonusLeave: false,
      dialogEditBonusLeave: false,
      dialogVisible: false,
      searchData: {
        reason: "",
        searchName: "",
        date: [],
        bonusTypeId: "",
      },
      bonusLeaveSelected: [],
      deleteMulButton: false,
      deleteIds: [],
    };
  },
  watch: {
    bonusLeaveSelected: function () {
      this.handleVisibleDeleteButton();
    },
  },
  async created() {
    await this.setOptionsBonusType();
    await this.getData();
  },
  computed: {
    SCOPES: function () {
      return SCOPES;
    },
  },
  methods: {
    formatDate,
    async setOptionsBonusType() {
      let res = await BonusTypeService.get();
      if (res && res.data) {
        this.optionsBonusType = res.data;
      }
    },
    async setPage(page) {
      this.page = page;
      await this.getDataFilterOption();
    },
    getDataFilterOption() {
      if (this.bonusLeaveData.searching) {
        this.searchRequest(this.page, this.searchData);
      } else {
        this.getData();
      }
    },
    async getData() {
      let responseData = await BonusLeaveService.get(this.pageSize, this.page);
      if (responseData && responseData.data) {
        this.loadData(responseData, false);
      }
    },
    handleData(visible) {
      this.dialogEditBonusLeave = visible;
      this.searchRequest();
    },
    handleSelectionChange(selection) {
      this.bonusLeaveSelected = selection;
    },
    handleVisibleDeleteButton() {
      this.deleteMulButton = this.bonusLeaveSelected.length > 0;
      this.deleteIds = [];
      this.bonusLeaveSelected.forEach((element) => {
        this.deleteIds.push(element.id);
      });
    },
    handleDeleteMultiple() {
      if (this.checkSelected(this.bonusLeaveSelected)) {
        this.dialogVisible = true;
      }
    },
    checkSelected(bonusLeaveSelected) {
      if (bonusLeaveSelected.length > 0) return true;
      else {
        this.$toast.warning("You have to select at least one row");
        return false;
      }
    },
    loadData(responseData, isSearching) {
      this.bonusLeaveData.rows = [];
      this.bonusLeaveData.searching = isSearching;
      this.bonusLeaveData.totalPage = responseData.data.page_number;
      this.bonusLeaveData.currentPage = responseData.data.current;
      this.bonusLeaveData.rows = responseData.data.results;
      let totalData = responseData.data.count;
      this.bonusLeaveData.countLastPage =
        totalData - Math.floor(totalData / this.pageSize) * this.pageSize;
      this.bonusLeaveData.countLastPage =
        this.bonusLeaveData.countLastPage > 0
          ? this.bonusLeaveData.countLastPage
          : this.pageSize;
    },
    editRequest(obj) {
      this.oldBonusLeave = obj;
      this.oldBonusLeave.bonus_type = obj.bonus_type.id;
      this.oldBonusLeave.profileTemp = obj.profile;
      this.oldBonusLeave.profile = obj.profile.issue_date;
      this.dialogEditBonusLeave = true;
    },
    deleteRequest(id) {
      this.deleteIds = [];
      this.deleteIds.push(id);
      this.dialogVisible = true;
    },
    deleteBonusLeaves() {
      if (this.bonusLeaveData.countLastPage === this.deleteIds.length) {
        this.page -= 1;
      }
      this.page = this.page === 0 ? 1 : this.page;
      BonusLeaveService.deleteBonusLeaves(this.deleteIds)
        .then((res) => {
          if (res.status === 204) {
            this.$toast.success("Deleted Successfully");
            this.dialogVisible = false;
            this.searchRequest(this.page, this.searchData);
          }
        })
        .catch(() => {
          this.$toast.error("An error occurred");
          this.dialogVisible = false;
        });
    },
    async searchRequest(page = this.page, searchData = this.searchData) {
      this.page = page;
      this.searchData = searchData;
      let reason = searchData.reason;
      let name = searchData.searchName.toLowerCase();
      let bonusTypeId = searchData.bonusTypeId;
      let fromDate = null;
      let toDate = null;
      if (searchData.date) {
        fromDate = this.formatDate(searchData.date[0]);
        toDate = this.formatDate(searchData.date[1]);
      }
      const responseData = await BonusLeaveService.searchRequest(
        reason,
        name,
        bonusTypeId,
        fromDate,
        toDate,
        this.page,
        this.pageSize
      );
      if (responseData && responseData.data) {
        this.loadData(responseData, true);
      }
    },
  },
};
</script>
<style lang="scss" scoped>
@import "index";

.modal-active {
  display: block;
}

.img-fluid {
  width: 60px;
}
</style>
