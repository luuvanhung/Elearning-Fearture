<template>
  <div class="container-bonus-leave">
    <filter-bonus-leave
      filterable
      :page_size="this.page_size"
      ref="filter"
      :search_name="this.search_name"
      :search_team="this.search_team"
      @ud_search_name="(value) => (this.search_name = value)"
      @ud_search_team="(value) => (this.search_team = value)"
    />
    <el-table
      :data="filterEmployee"
      stripe
      header-cell-class-name="bg-header-table"
      height="25vh"
      style="width: 100%"
      :default-sort="{ prop: 'profile.name', order: 'descending' }"
      @selection-change="handleSelectionChange"
      ref="employeeTable"
    >
      <el-table-column type="selection" width="45"> </el-table-column>
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
              />
              <img v-else class="img-fluid" src="@/static/images/icon.png" />
            </div>
          </router-link>
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
            :to="`/profile/${table.row.id}`"
            title="Click to move to Profile page"
            tag="a"
            prop="profile.name"
          >
            <strong>{{ table.row.profile.name }}</strong>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column prop="email" label="Email" sortable align="center">
      </el-table-column>
      <el-table-column prop="title" label="Position" sortable align="center">
        <template v-slot:default="table">
          <div>
            {{
              !table.row.title
                ? ""
                : table.row.title.map((e) => e.title).join(", ")
            }}
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="profile.teams"
        label="Team"
        sortable
        align="center"
      >
        <template v-slot:default="table">
          <div>
            {{ table.row.profile.teams }}
          </div>
        </template>
      </el-table-column>
    </el-table>

    <el-row type="flex" justify="center" class="m-4">
      <el-col :span="4" align="center">
        <el-button type="primary" @click="add()">Add</el-button>
      </el-col>
    </el-row>

    <el-row type="flex" :gutter="20">
      <el-col :span="4">
        <el-input-number
          controls-position="right"
          v-model="givenLeave"
          :step-strictly="true"
          :step="0.5"
          :min="0.5"
          :max="365"
          size="medium"
          placeholder="Amount of leaves"
        />
      </el-col>
      <el-col :offset="2" :span="7">
        <el-select
          v-model="bonusTypeId"
          :options="optionsBonusType"
          placeholder="Types"
          default-first-option
        >
          <el-option
            v-for="(item, index) in optionsBonusType"
            :key="index"
            :label="item.name"
            :value="item.id"
          >
          </el-option>
        </el-select>
      </el-col>
      <el-col>
        <el-input
          class="mb-2"
          label="Reason"
          single-line
          v-model="reason"
          clearable
          placeholder="Enter Reason"
        >
        </el-input>
      </el-col>
    </el-row>

    <el-table
      :data="employeesBonusLeaveData"
      stripe
      header-cell-class-name="bg-header-table"
      height="25vh"
      style="width: 100%"
    >
      <el-table-column
        prop="profile.image"
        label="Avatar"
        align="center"
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
              />
              <img v-else class="img-fluid" src="@/static/images/icon.png" />
            </div>
          </router-link>
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
            :to="`/profile/${table.row.id}`"
            title="Click to move to Profile page"
            tag="a"
            prop="profile.name"
          >
            <strong>{{ table.row.profile.name }}</strong>
          </router-link>
        </template>
      </el-table-column>

      <el-table-column prop="email" label="Email" sortable align="center">
      </el-table-column>
      <el-table-column prop="title" label="Position" sortable align="center">
        <template v-slot:default="table">
          <div>
            {{
              !table.row.title
                ? ""
                : table.row.title.map((e) => e.title).join(", ")
            }}
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="profile.teams"
        label="Team"
        sortable
        align="center"
      >
        <template v-slot:default="table">
          <div>
            {{ table.row.profile.teams }}
          </div>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="100" align="center">
        <template v-slot:default="table">
          <img
            :src="require('@/static/images/IconDelete.svg')"
            class="ml-1"
            @click="remove(table.$index)"
            title="Delete Probation Template"
          />
        </template>
      </el-table-column>
    </el-table>
    <div class="footer-dialog d-flex justify-content-end mt-2">
      <el-button type="info" @click="clear()">Clear</el-button>
      <el-button type="primary" @click="bonus()">Bonus</el-button>
    </div>
  </div>
</template>
<script>
import UserService from "@/services/user/user";
import BonusLeaveService from "@/services/leave_management/bonus_leave/bonus_leave.services";
import FilterBonusLeave from "@/pages/leaveBonus/filterBonusLeave";

export default {
  name: "bonusLeaveModel",
  middleware: "authentication",

  props: ["optionsBonusType"],
  data() {
    return {
      search_name: "",
      search_team: "",

      employeesData: [],
      employeesBonusLeaveData: [],
      selectedEmployees: [],
      bonusTypeId: null,
      givenLeave: 0.5,
      reason: "",
      users_pk: [],

      page_size: 8,
    };
  },
  components: {
    FilterBonusLeave,
  },

  async created() {
    await this.getData();
  },
  methods: {
    handleSelectionChange(value) {
      this.selectedEmployees = value;
    },

    add() {
      this.employeesBonusLeaveData.unshift(...this.selectedEmployees);
      this.employeesData = this.employeesData.filter(
        (data) => !this.selectedEmployees.includes(data)
      );
    },

    remove(index) {
      let employeeData = this.employeesBonusLeaveData[index];
      this.employeesBonusLeaveData.splice(index, 1);
      this.employeesData.unshift(employeeData);
      this.selectedEmployees.splice(index, 1);
    },

    async bonus() {
      this.users_pk = this.employeesBonusLeaveData.map((data) => data.id);
      if (
        this.bonusTypeId !== null &&
        this.users_pk.length !== 0 &&
        this.reason !== ""
      ) {
        const data = {
          bonus_type_id: this.bonusTypeId,
          reason: this.reason,
          bonus_days: this.givenLeave,
          users_pk: this.users_pk,
        };

        if (this.givenLeave % 0.5 === 0) {
          const res = await BonusLeaveService.create(data);
          if (res.status === 201) {
            this.$toast.success("Created Successfully");
            this.clear();
            this.$emit("getData");
          } else {
            this.$toast.error("Create Failed");
          }
        } else {
          this.$toast.error("Create Failed");
        }
      } else {
        this.$toast.error("Input is not valid");
      }
    },

    clear() {
      this.users_pk = null;
      this.bonusTypeId = null;
      this.employeesData.unshift(...this.employeesBonusLeaveData);
      this.employeesBonusLeaveData = [];
      this.reason = "";
      this.givenLeave = 0.5;
    },

    async getData() {
      let responseData = await UserService.getAllEmployees();
      if (responseData && responseData.data) {
        this.loadData(responseData, false);
      }
    },

    processing_data(responseData) {
      // convert teams array to string
      let temp = responseData.data.map((data) => {
        if (data.profile.teams.length != 0) {
          data.profile.teams = data.profile.teams
            .map((team) => team.name)
            .join(", ");
        } else {
          data.profile.teams = "";
        }
        return data;
      });
      responseData.data = temp;
      return responseData;
    },

    loadData(responseData, isSearching) {
      responseData = this.processing_data(responseData);
      this.employeesData = responseData.data;
    },
  },

  computed: {
    tableData() {
      let listResult = [];
      if (this.listInvite.length > 0) {
        return this.listInvite;
      } else {
        return listResult.concat(this.validUser, this.invalidUser);
      }
    },

    filterEmployee() {
      let searchText = this.search_name.toLowerCase();
      let team = this.search_team;
      let employeeData = this.employeesData.filter(
        (data) =>
          data.email.toLowerCase().includes(searchText) ||
          data.profile.name.toLowerCase().includes(searchText)
      );
      return team.trim() === ""
        ? employeeData
        : employeeData.filter((data) => data.profile.teams === team);
    },
  },
};
</script>

<style scoped>
@import "bonusLeave.scss";
@import "bonusTypes.scss";
</style>
