<template>
  <div>
    <restricted-view :scopes="['admin:invite_user']">
      <template v-slot:default>
        <div class="row">
          <div
            class="col-12 col-lg-6 mt-3 col-xl-6 ml-auto justify-xl-end d-flex justify-content-end"
          >
            <el-button type="primary">
              <download-excel
                class="btn btn-info"
                :fetch="fetchDataForExportExcel"
                :fields="json_fields"
                worksheet="My Worksheet"
                title="Click to export excel"
                name="user.xlsx"
              >
                <font-awesome-icon :icon="['fas', 'file-export']" />
                Export file
              </download-excel>
            </el-button>
            <el-button type="primary" @click="dialogInvite = true">
              <font-awesome-icon :icon="['fas', 'user-plus']" />
              <span class="ml-2">Invite</span>
            </el-button>
            <el-button type="primary" @click="dialogImportFile = true">
              <font-awesome-icon :icon="['fas', 'file-import']" />
              <span class="ml-2">Import file</span>
            </el-button>
          </div>
        </div>
      </template>
    </restricted-view>
    <div class="">
      <FilterBox
        @getData="getData"
        @loadData="loadData"
        :page_size="this.page_size"
        ref="filter"
      />
      <el-table
        :data="employeesData.rows"
        stripe
        header-cell-class-name="bg-header-table"
        style="width: 100%"
      >
        <el-table-column
          prop="profile.image"
          label="Avatar"
          cell-click="`/profile/`"
        >
          <template v-slot:default="table">
            <router-link
              :to="`/profile/${table.row.id}`"
              tag="span"
              prop="profile.image"
            >
              <div class="d-flex" style="justify-content: center">
                <img
                  class="img-fluid"
                  :src="table.row.profile.image"
                  v-if="table.row.profile.image !== null"
                  alt="avatar"
                />
                <img
                  v-else
                  class="img-fluid"
                  src="@/static/images/icon.png"
                  alt="avatar-default"
                />
              </div>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
          prop="profile.name"
          label="Name"
          align="center"
          width="180"
        >
          <template v-slot:default="table">
            <router-link
              :to="`/profile/${table.row.id}`"
              title="Click to move to Profile page"
              tag="a"
              prop="profile.name"
            >
              <strong>{{ table.row.profile.name }}</strong>
            </router-link>
          </template>
        </el-table-column>
        <restricted-view :scopes="['user:view_private_user_information_list']">
          <template v-slot:default>
            <el-table-column prop="email" label="Email">
              <template v-slot:default="table">
                <a
                  class="btn text-muted"
                  :href="'mailto:' + table.row.profile.email"
                  title="Click to send mail"
                >
                  {{ table.row.email }}</a
                >
              </template>
            </el-table-column>
          </template>
        </restricted-view>

        <el-table-column prop="title" label="Position">
          <template v-slot:default="table">
            <div style="text-align: center">
              {{
                !table.row.title
                  ? ""
                  : table.row.title.map((e) => e.title).join(", ")
              }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="profile.gender" label="Gender" align="center">
          <template v-slot:default="table">
            <strong v-if="GENDERS[table.row.profile.gender] !== undefined">
              {{ GENDERS[table.row.profile.gender].text }}
            </strong>
          </template>
        </el-table-column>
        <restricted-view :scopes="['user:view_private_user_information_list']">
          <template v-slot:default>
            <el-table-column
              prop="profile.birth_day"
              label="Birthday"
              align="center"
            >
            </el-table-column>
            <el-table-column prop="profile.phone" label="Phone" align="center">
            </el-table-column>
          </template>
        </restricted-view>

        <el-table-column prop="profile.teams" label="Team">
          <template v-slot:default="table">
            <router-link
              v-for="team in table.row.profile.teams"
              :to="'/teams/' + team.id"
              class="font-weight-bold text-center d-block w-100 py-2 badge my-2 badge-pill"
              style="font-size: 0.9em"
              :key="team.index"
            >
              {{ team.name ? team.name : "No team" }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
          prop="profile.join_date"
          label="On board at Paradox/Olivia"
          align="center"
        >
        </el-table-column>
      </el-table>
      <div class="d-flex justify-content-center mt-5">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="employeesData.page_size"
          :page-count="employeesData.totalPage"
          :current-page="employeesData.currentPage"
          :total="employeesData.count"
          @current-change="setPage"
        >
        </el-pagination>
      </div>
    </div>

    <el-dialog title="Invite user" :visible.sync="dialogInvite">
      <InviteModal />
    </el-dialog>
    <el-dialog
      title="Import File"
      v-if="dialogImportFile"
      :visible.sync="dialogImportFile"
    >
      <ImportFileModal @updateDialogImportFile="updateDialogImportFile" />
    </el-dialog>
  </div>
</template>

<script>
import FilterBox from "@/pages/employeelist/filter";
import ImportFileModal from "@/pages/employeelist/ImportFileModal.vue";
import InviteModal from "@/pages/employeelist/inviteModal.vue";
import { GENDERS } from "@/const/genders";

import GetUserService from "@/services/user/getUser";
import ExportExcelService from "@/services/user/exportExcel";
import "vue2-datepicker/index.css";
import Vue from "vue";
import moment from "moment";
import RestrictedView from "@/components/RestrictedView";

export default {
  components: {
    FilterBox,
    ImportFileModal,
    InviteModal,
    RestrictedView,
  },
  name: "id_list_table",
  middleware: "authentication",
  data() {
    return {
      json_fields: {
        Name: {
          field: "profile",
          callback: (value) => {
            return `${value.name}`;
          },
        },
        Email: "email",
        "Birth day": {
          field: "profile",
          callback: (value) => {
            return `${value.birth_day}`;
          },
        },
        Phone: {
          field: "profile",
          callback: (value) => {
            return `${value.phone}`;
          },
        },
        "Join date": {
          field: "profile",
          callback: (value) => {
            return `${value.join_date}`;
          },
        },
        Team: {
          field: "profile",
          callback: (value) => {
            return this.getCallBack(value.teams);
          },
        },
      },
      bus: new Vue(),
      admin: localStorage.getItem("is_admin"),
      items: [
        {
          text: "Homepage",
          to: { name: "Index" },
        },
        {
          text: "Employee List",
          active: true,
        },
      ],
      borderradius: {
        borderRadius: "1.25rem",
        textAlign: "center",
      },
      tablewidth: {
        width: "250px",
      },
      tableteamwidth: {
        width: "220px",
      },
      color: {
        color: "#25c9d0",
        fontSize: "40px",
        marginLeft: "16px",
      },
      text: {
        fontSize: "20px",
      },
      pageInfo: {
        pageNumber: "",
        previous: "",
        next: "",
      },
      errors: "",
      subject: "",
      content: "",
      page_size: 8,
      employeesData: {
        searching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
      },
      dialogInvite: false,
      dialogImportFile: false,
    };
  },
  async created() {
    await this.getData(1, this.page_size);
  },
  computed: {
    GENDERS: function () {
      return GENDERS;
    },
  },
  methods: {
    updateDialogImportFile(value) {
      this.dialogImportFile = value;
    },
    getCallBack(value) {
      const data = value.map((e) => e.name);
      return data;
    },
    async fetchDataForExportExcel() {
      let data = null;
      if (this.employeesData.searching) {
        const searchData = this.$refs.filter.getSearchData();
        const joindate = this.format_date(searchData.joinDate);
        data = await ExportExcelService.search(
          searchData.name,
          searchData.email,
          searchData.birthdayMonth,
          joindate,
          searchData.gender,
          searchData.title,
          searchData.team,
          searchData.active
        );
      } else {
        data = await ExportExcelService.get();
      }
      return data.data;
    },
    async setPage(page) {
      await this.getDataFilterOption(page, this.page_size);
    },
    getDataFilterOption(page = 1, page_size = this.page_size) {
      if (this.employeesData.searching) {
        this.$refs.filter.search(page);
      } else {
        this.getData(page, page_size);
      }
    },
    async getData(page = 1, page_size = this.page_size) {
      let responseData = await GetUserService.get(page_size, page);
      if (responseData && responseData.data) {
        this.loadData(responseData, false);
      }
    },
    loadData(responseData, isSearching) {
      this.employeesData.searching = isSearching;
      this.employeesData.rows = responseData.data.results;
      this.employeesData.totalPage = responseData.data.page_number;
      this.employeesData.currentPage = responseData.data.current;
    },
    format_date(value) {
      if (value) {
        return moment(String(value)).format("YYYY-MM");
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
img {
  width: 60px;
  height: 60px;
}
</style>
