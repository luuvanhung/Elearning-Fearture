<template>
  <div class="block" style="min-width: 880px">
    <el-button @click="onSave()" class="save-btn">Save</el-button>
    <el-table
      class="table-responsive"
      ref="departmentTable"
      highlight-current-row
      :data="tableData"
      @selection-change="onTeamsSelectedChange"
      border
      v-if="tableData.length > 0"
    >
      <el-table-column type="selection" align="center" />
      <el-table-column align="center" :min-width="200" label="Department" fixed>
        <template v-slot="scope">
          {{ scope.row.department }}
        </template>
      </el-table-column>
      <el-table-column type="expand" align="center" :min-width="200" fixed>
        <template v-slot="props">
          <el-table
            :data="convertData(props.row.teams)"
            style="width: 100%"
            border
          >
            <el-table-column prop="team" label="Team">
              <template slot-scope="scope">
                <el-popover placement="left" trigger="hover">
                  <el-popconfirm
                    confirm-button-text="Delete"
                    cancel-button-text="No"
                    title="Remove this team?"
                    @confirm="onRemove(scope.row.team)"
                  >
                    <template slot="reference">
                      <el-button type="danger">Remove</el-button>
                    </template>
                  </el-popconfirm>
                  <p slot="reference">{{ scope.row.team }}</p>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column label="Department">
              <template slot-scope="scope">
                <el-select
                  v-model="departmentDistribution[scope.row.team]"
                  placeholder="Select"
                >
                  <el-option
                    v-for="department in departments"
                    :key="department.value"
                    :label="department.label"
                    :value="department.value"
                  >
                  </el-option>
                </el-select>
              </template>
            </el-table-column>
          </el-table>
        </template>
      </el-table-column>
    </el-table>
    <div v-else class="no-data">
      <p>No new departments</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfirmAddNewDepartment",
  props: ["newUsers", "contactCols", "newTeams"],
  computed: {
    tableData() {
      return this.newDepartments.map((department) => {
        return {
          department: department,
          teams: this.teamData
            .map((item) => {
              if (item.department === department) {
                return { team: item.team, department: item.department };
              }
            })
            .filter((item) => item),
        };
      });
    },
    departments() {
      return this.newDepartments.map((department) => {
        return {
          value: department,
          label: department,
        };
      });
    },
  },
  data() {
    return {
      selectedDepartment: [],
      teamData: this.newTeams.map((item) => {
        return {
          team: item.team,
          department: item.members[0][this.contactCols.department],
        };
      }),
      newDepartments: this.newUsers
        .map(({ _index, values }) => {
          let team = values[this.contactCols.team];
          if (team.toLowerCase().includes("department")) {
            return values[this.contactCols.team].split(": ")[1];
          }
        })
        .filter(this.onlyUnique),
      departmentDistribution: {},
    };
  },
  mounted() {
    if (this.$refs.departmentTable) {
      this.$refs.departmentTable.toggleAllSelection();
    }
    this.teamData.forEach((team) => {
      this.$set(
        this.departmentDistribution,
        `${team.team}`,
        `${team.department}`
      );
    });
  },
  methods: {
    reRenderTable() {
      this.newTeams.push("test");
      this.newTeams.pop();
      this.$refs.departmentTable.toggleAllSelection();
    },
    onlyUnique(value, index, self) {
      return self.indexOf(value) === index && value;
    },
    onTeamsSelectedChange(val) {
      this.selectedDepartment = val;
    },
    convertData(data) {
      const convertedData = [];
      data.forEach((team) => {
        convertedData.push({
          team: team.team,
        });
      });
      return convertedData;
    },
    onSave() {
      this.teamData.forEach((team) => {
        team.department = this.departmentDistribution[team.team];
      });
      this.reRenderTable();
    },
    onRemove(teamName) {
      this.teamData.forEach((team, index) => {
        if (team.team === teamName) {
          this.teamData.splice(index, 1);
        }
      });
      this.reRenderTable();
    },
  },
  watch: {
    selectedDepartment: function () {
      this.$emit("input", this.selectedDepartment);
    },
  },
};
</script>
<style scoped>
.save-btn {
  position: absolute;
  top: -42px;
  right: 30px;
  font-size: 14px;
  padding: 6px 20px;
}
</style>
