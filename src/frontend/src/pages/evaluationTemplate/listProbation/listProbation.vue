<template>
  <div v-if="loading" class="lmask" ref="loading-mask" />
  <div v-else :style="{ visibility: !loading ? 'visible' : 'hidden' }">
    <el-card>
      <div class="btn-new">
        <restricted-view :scopes="['probation:create']">
          <el-button
            class="btn-new-probation"
            type="primary"
            icon="el-icon-circle-plus"
            @click="addNewProbation"
          >
            New Evaluation
          </el-button>
        </restricted-view>
      </div>
      <div class="office-export">
        <div class="d-flex">
          <div class="d-flex align-items-center">
            <span>Office: </span>
            <el-select
              v-model="search.office"
              placeholder="Office"
              clearable
              @change="handleSearch"
            >
              <el-option
                v-for="office in offices"
                :key="office.id"
                :label="office.name"
                :value="office.id"
              >
              </el-option>
            </el-select>
            <span>Evaluation Types: </span>
            <el-select
              v-model="search.type"
              placeholder="Type Evaluation"
              clearable
              @change="handleSearch"
            >
              <el-option
                v-for="type in templateTypes"
                :key="type.id"
                :label="type.type_name"
                :value="type.id"
              >
              </el-option>
            </el-select>
          </div>
          <div class="d-flex align-items-center search-by-name">
            <span>Full Name: </span>
            <el-input
              v-model="search.name"
              placeholder="Search by Name"
              clearable
              @change="handleSearch"
            />
          </div>
          <el-button
            size="medium"
            @click="handleSearch"
            type="primary"
            icon="el-icon-search"
            >Search</el-button
          >
        </div>
        <div>
          <el-button type="primary" @click="exportToExcelListProbation">
            <font-awesome-icon :icon="['fas', 'file-export']" />
            Export
          </el-button>
        </div>
      </div>
      <el-table
        class="table"
        ref="multipleTable"
        :data="probations"
        header-cell-class-name="bg-header-table"
        border
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" align="center"> </el-table-column>
        <el-table-column
          property="fullName"
          label="Full Name"
          prop="employee.profile.name"
          sortable
          align="center"
        >
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                v-model="scope.row.employee.profile.name"
                :placeholder="
                  scope.row.employee.profile.name === ''
                    ? 'Full Name*'
                    : scope.row.employee.profile.name
                "
              >
              </el-input>
            </div>
            <div v-else>
              {{ scope.row.employee.profile.name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          label="Start Date"
          prop="employee.profile.join_date"
          sortable
          align="center"
        >
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                v-model="scope.row.employee.profile.join_date"
                placeholder="Start Date*"
              ></el-input>
            </div>
            <div v-else>
              {{ scope.row.employee.profile.join_date }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          label="End Date"
          show-overflow-tooltip
          prop="probation_end_date"
          sortable
          align="center"
        >
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                v-model="scope.row.probation_end_date"
                placeholder="End Date*"
              ></el-input>
            </div>
            <div v-else>
              {{ scope.row.probation_end_date }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          property="remind"
          label="Remind"
          prop="remind"
          sortable
          align="center"
        >
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                v-model="scope.row.remind"
                placeholder="Remind*"
              ></el-input>
            </div>
            <div v-else-if="scope.row.remind === reminder">
              {{ scope.row.remind }}
            </div>
            <div v-else v-for="remind in scope.row.remind" :key="remind">
              {{ remind }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          label="Type Of Evaluation"
          show-overflow-tooltip
          prop="type_name"
          sortable
          align="center"
        >
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                v-model="scope.row.type_name"
                placeholder="Type Evaluation*"
              ></el-input>
            </div>
            <div v-else>
              {{ scope.row.type_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column property="actions" label="Actions" align="center">
          <template v-slot="scope">
            <el-button
              circle
              style="cursor: pointer"
              @click="showViewDetailProbation(scope.row)"
              type="primary"
              icon="el-icon-edit"
              title="Edit Probation List"
            ></el-button>
            <restricted-view :scopes="['probation:destroy']">
              <el-button
                circle
                style="cursor: pointer"
                type="danger"
                icon="el-icon-delete"
                @click="deleteProbation(scope.row.id)"
                title="Delete Probation List"
              />
            </restricted-view>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        class="pagination"
        background
        hide-on-single-page
        layout="prev, pager, next"
        :current-page="+query.page"
        :page-size="+query.page_size"
        @current-change="changePages"
        :total="total"
      >
      </el-pagination>
    </el-card>
  </div>
</template>
<script>
import { mapState, mapActions } from "vuex";
import ProbationService from "../../../services/probation/probation";
import RestrictedView from "@/components/RestrictedView";
import { generateProbationList } from "@/utils/excelListProbation";

export default {
  name: "listProbation",
  components: {
    RestrictedView,
  },

  created() {
    setTimeout(this.disableMask, 1000);
    this.fetchOffices();
    this.fetchTypes();
    this.query = {
      ...this.query,
      ...this.$route.query,
      ...this.search,
    };
  },

  computed: {
    ...mapState("probation", ["offices", "templateTypes"]),
  },

  data() {
    return {
      multipleSelection: [],
      probations: [],
      total: 0,
      search: {
        name: "",
        office: "",
        type: "",
      },
      query: {
        page: 1,
        page_size: 10,
      },
      loading: true,
      reminder: "No reminder",
    };
  },

  methods: {
    ...mapActions("probation", ["fetchOffices", "fetchTypes"]),

    disableMask() {
      this.loading = false;
    },

    handleSelectionChange(val) {
      this.multipleSelection = val;
    },

    addNewProbation() {
      this.$router.push("evaluations/new");
    },

    showViewDetailProbation(row) {
      this.$router.push({ path: `/evaluations/${row.id}` });
    },

    deleteProbation(id) {
      this.$confirm("Are you sure you want to delete it?", "Confirm", {
        distinguishCancelAndClose: true,
        confirmButtonText: "Yes",
        cancelButtonText: "No",
      })
        .then(async () => {
          const res = await ProbationService.deleteProbation(id);
          if (res.status === 204) {
            this.$toast.success("Deleted Successfully");
            await this.getListProbations();
          } else {
            this.$toast.error("Delete Failed");
          }
        })
        .catch(() => {
          /* TODO document why this arrow function is empty */
        });
    },

    async getListProbations() {
      const result = await ProbationService.getPage(this.query);
      if (result) {
        this.probations = result.results;
        this.total = result.count;
      }
    },

    async changePages(newPage) {
      this.query.page = newPage;
    },

    handleSearch() {
      this.query = {
        ...this.query,
        ...this.search,
        page: 1,
      };
    },

    exportToExcelListProbation() {
      generateProbationList(this);
    },
  },

  watch: {
    query: {
      deep: true,
      handler: function () {
        this.getListProbations();
        this.$router
          .push({ path: "/evaluations", query: this.query })
          .catch((err) => err);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./listProbation.scss";
</style>
