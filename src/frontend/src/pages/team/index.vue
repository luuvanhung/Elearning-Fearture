<template>
  <div>
    <div>
      <el-row
        class="mt-3 mb-3 d-flex justify-content-between align-items-center"
      >
        <el-input
          class="ml-3"
          placeholder="Search here"
          v-model="searchValue"
          style="width: 25%; order: -1"
          @keyup.enter.native="searchRequest(1)"
        ></el-input>
        <div
          class="col-12 col-lg-6 mt-3 col-xl-6 ml-auto justify-xl-end d-flex justify-content-end"
        >
          <restricted-view :scopes="[scopeData['TeamEditAllTeam']]">
            <template v-slot:default>
              <el-button
                type="danger"
                class="ml=2"
                @click="handleDeleteMultiple"
              >
                Delete
              </el-button>
            </template>
          </restricted-view>
          <restricted-view :scopes="[scopeData['TeamCreate']]">
            <el-button type="primary" @click="handleImport" class="ml-2">
              <font-awesome-icon :icon="['fas', 'file-import']" />
              Import File
            </el-button>
          </restricted-view>
          <restricted-view :scopes="[scopeData['TeamCreate']]" style="order: 1">
            <template v-slot:default>
              <el-row>
                <router-link
                  to="/create-team/"
                  style="color: #ffffff; text-decoration: none"
                >
                  <el-button type="primary" class="ml-2">
                    <font-awesome-icon :icon="['fas', 'user-friends']" />
                    Create New Team
                  </el-button>
                </router-link>
              </el-row>
            </template>
          </restricted-view>
        </div>
      </el-row>
      <el-table
        @selection-change="handleSelectionChange"
        highlight-current-row
        :data="teamsData.rows"
        header-cell-class-name="bg-header-table"
        border
      >
        <restricted-view :scopes="[scopeData['TeamEditAllTeam']]">
          <template v-slot:default>
            <el-table-column type="selection" align="center"></el-table-column>
          </template>
        </restricted-view>
        <el-table-column prop="team_name" sortable label="Team Name">
          <template v-slot="scope">
            <div class="text-center">
              <router-link
                :to="'/teams/' + scope.row.id"
                style="text-decoration: none"
                title="Click to go to the team's detail page"
              >
                <strong> {{ scope.row.team_name }}</strong>
              </router-link>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="team_email" sortable label="Team Email">
          <template v-slot="scope">
            <div class="text-center">
              <a
                :href="'mailto:' + scope.row.team_email"
                style="text-decoration: none"
                title="Click to send mail"
              >
                {{ scope.row.team_email }}
              </a>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="leader_name" sortable label="Team Leader">
          <template v-slot="scope">
            <div class="text-center">
              <div
                class="text-center"
                :class="{
                  'text-danger': scope.row.leader_name === 'No leader',
                }"
              >
                {{ scope.row.leader_name }}
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="department_name" sortable label="Department">
          <template v-slot="scope">
            <div class="text-center">
              {{ scope.row.department_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="office_name" sortable label="Office">
          <template v-slot="scope">
            <div class="text-center">
              {{ scope.row.office_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="group_name" sortable label="Group">
          <template v-slot="scope">
            <div class="text-center">
              {{ scope.row.group_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          sortable
          prop="employee_number"
          label="Members"
          width="120"
        >
          <template v-slot="scope">
            <div class="text-center">
              {{ scope.row.employee_number }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="Action" width="80" align="center">
          <template v-slot="scope">
            <restricted-view
              :scopes="[
                scopeData['TeamEditAllTeam'],
                scopeData['TeamEditMyTeam'],
              ]"
            >
              <template v-slot:default>
                <div v-if="checkScope(scope.row)">
                  <el-button
                    circle
                    style="cursor: pointer"
                    type="danger"
                    icon="el-icon-delete"
                    @click="showModal(scope.row.id, scope.row.team_name)"
                  ></el-button>
                </div>
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
          :page-count="teamsData.totalPage"
          :current-page="teamsData.currentPage"
          @current-change="setPage"
        >
        </el-pagination>
      </div>
      <el-dialog :visible.sync="dialog" hide-footer hide-header="">
        <div class="d-block text-center text-danger">
          <h3>Remove team</h3>
          <hr />
        </div>
        <div class="d-block text-center mb-4">
          Do you want to remove team
          <p class="text-danger d-inline">{{ currentTeamName }}</p>
        </div>
        <div class="d-flex justify-content-center">
          <el-button type="primary" @click="del">Remove</el-button>
          <el-button type="danger" @click="hideModal">Cancel</el-button>
        </div>
      </el-dialog>
      <el-dialog
        title="Delete"
        :visible.sync="dialogDelMulti"
        width="30%"
        class="dialog"
      >
        <span>Do you want to delete this teams ?</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogDelMulti = false">Cancel</el-button>
          <el-button type="primary" @click="deleteTeams()">Confirm</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import TeamServices from "@/services/team/team.services";
import RestrictedView from "@/components/RestrictedView";
import { mapGetters, mapActions } from "vuex";
import { SCOPES } from "@/const/scopes";
export default {
  name: "team_table",
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  data() {
    return {
      rows: [],
      teamsSelected: [],
      teamsData: {
        searching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
        countLastPage: 0,
      },
      admin: localStorage.getItem("is_admin"),
      profile_id: localStorage.getItem("profile_id"),
      currentId: "",
      currentTeamName: "",
      color: {
        color: "#25c9d0",
        fontSize: "40px",
        marginLeft: "16px",
      },
      text: {
        fontSize: "20px",
      },
      errors: "",
      subject: "",
      dialog: false,
      dialogDelMulti: false,
      searchValue: "",
      scopeData: SCOPES,
      page: 1,
      pageSize: 10,
    };
  },

  created() {
    this.asyncData();
    this.getListTeam();
    this.getListSquad();
    this.getListDepartment();
  },
  computed: {
    ...mapGetters({
      tokenInfo: "scope/tokenInfo",
    }),
  },
  watch: {
    searchValue: function () {
      this.searchRequest(1);
    },
  },
  methods: {
    ...mapActions("team", ["getListTeam"]),
    ...mapActions("squad", ["getListSquad", "getListDepartment"]),
    async asyncData() {
      const responseData = await TeamServices.getTeams(
        this.page,
        this.pageSize
      );
      if (responseData) {
        this.loadData(responseData.data, false);
      }
    },
    loadData: function (responseData, isSearching) {
      this.teamsData.searching = isSearching;
      this.teamsData.rows = responseData.results;
      this.teamsData.totalPage = responseData.page_number;
      this.teamsData.currentPage = responseData.current;
      const totalData = responseData.count;
      this.teamsData.countLastPage =
        totalData - Math.floor(totalData / this.pageSize) * this.pageSize;
      this.teamsData.countLastPage =
        this.teamsData.countLastPage > 0
          ? this.teamsData.countLastPage
          : this.pageSize;
    },
    async setPage(page) {
      this.page = page;
      await this.getDataFilterOption();
    },
    getDataFilterOption() {
      if (this.teamsData.searching) {
        this.searchRequest(this.page, this.searchData);
      } else this.asyncData(this.page);
    },
    async searchRequest(page = 1, keyWord = this.searchValue) {
      this.page = page;
      const responseData = await TeamServices.searchRequest(
        keyWord,
        this.page,
        this.pageSize
      );
      if (responseData && responseData.data) {
        this.loadData(responseData.data, true);
      }
    },
    handleSelectionChange(selection) {
      this.teamsSelected = selection;
    },
    handleDeleteMultiple() {
      if (this.checkSelected(this.teamsSelected)) {
        this.dialogDelMulti = true;
      }
    },
    checkSelected(teamsSelected) {
      if (teamsSelected.length > 0) return true;
      else {
        this.$toast.warning("You have to select at least one row");
        return false;
      }
    },
    deleteTeams() {
      let deleteIds = [];
      this.teamsSelected.forEach((team) => deleteIds.push(team.id));
      if (this.teamsData.countLastPage === deleteIds.length) {
        this.page -= 1;
      }
      this.page = this.page === 0 ? 1 : this.page;
      TeamServices.deleteTeams(deleteIds)
        .then((res) => {
          if (res.status === 204) {
            this.$toast.success("Deleted Successfully");
            this.dialogDelMulti = false;
            this.searchRequest(this.page, this.searchData);
          }
        })
        .catch(() => {
          this.$toast.error("An error occurred");
          this.dialogDelMulti = false;
        });
    },
    showModal(id, name) {
      this.currentId = id;
      this.currentTeamName = name;
      this.dialog = true;
    },

    hideModal() {
      this.dialog = false;
    },

    del: async function () {
      try {
        if (this.teamsData.countLastPage === 1) {
          this.page -= 1;
        }
        await TeamServices.removeTeam(this.currentId);
        this.getDataFilterOption();
        this.$toast.success("Removed Successfully");
      } catch (e) {
        console.log(e);
        this.$toast.error("Remove Failed");
      }
      this.dialog = false;
    },

    checkTeamLead(team) {
      return team.team_leader === localStorage.getItem("user_id");
    },

    hasScope(scope) {
      return this.tokenInfo["scope"].indexOf(scope) !== -1;
    },

    checkScope(scope) {
      return (
        (this.hasScope(this.scopeData["TeamEditMyTeam"]) &&
          this.checkTeamLead(scope)) ||
        this.hasScope(this.scopeData["TeamEditAllTeam"])
      );
    },

    handleImport() {
      this.$router.push("/import-from-excel");
    },
  },
};
</script>

<style lang="scss">
@import "./style.scss";
</style>
