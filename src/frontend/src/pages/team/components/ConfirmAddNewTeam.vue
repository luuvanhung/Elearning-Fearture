<template>
  <div class="block" style="min-width: 880px">
    <el-button @click="onSave()" class="save-btn">Save</el-button>
    <el-table
      v-if="tableData.length > 0"
      class="table-responsive"
      ref="teamTable"
      highlight-current-row
      :data="tableData"
      @selection-change="onTeamsSelectedChange"
      border
    >
      <el-table-column type="selection" align="center" />
      <el-table-column align="center" :min-width="200" label="Team" fixed>
        <template v-slot="scope">
          {{ scope.row.team }}
        </template>
      </el-table-column>
      <el-table-column type="expand" align="center" :min-width="200" fixed>
        <template v-slot="props">
          <el-table
            :data="convertData(props.row.members)"
            style="width: 100%"
            border
          >
            <el-table-column prop="name" label="Name">
              <template slot-scope="scope">
                <el-popover
                  placement="left"
                  trigger="hover"
                  style="min-width: 0"
                >
                  <el-popconfirm
                    confirm-button-text="Delete"
                    cancel-button-text="No"
                    title="Remove this user?"
                    @confirm="onRemove(scope.row.name)"
                  >
                    <template slot="reference">
                      <el-button type="danger">Remove</el-button>
                    </template>
                  </el-popconfirm>
                  <p slot="reference">{{ scope.row.name }}</p>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column prop="role" label="Role"></el-table-column>
            <el-table-column label="Team">
              <template slot-scope="scope">
                <el-select
                  v-model="teamDistribution[scope.row.name]"
                  placeholder="Select"
                >
                  <el-option
                    v-for="team in teams"
                    :key="team.value"
                    :label="team.label"
                    :value="team.value"
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
      <p>No new teams</p>
    </div>
  </div>
</template>
<script>
export default {
  name: "ConfirmAddNewTeam",
  props: ["newUsers", "contactCols"],
  computed: {
    tableData() {
      return this.newTeams.map((team) => {
        return {
          team: team,
          members: this.newUsers
            .map(({ _index, values }) => {
              if (values[this.contactCols.team] === team) {
                return values;
              }
            })
            .filter((item) => item),
        };
      });
    },
    teams() {
      return this.newTeams.map((team) => {
        return {
          value: team,
          label: team,
        };
      });
    },
  },
  data() {
    return {
      value: "",
      selectedTeams: [],
      newTeams: this.newUsers
        .map(({ _index, values }) => {
          let team = values[this.contactCols.team];
          if (
            !team.toLowerCase().includes("squad") &&
            !team.toLowerCase().includes("department")
          ) {
            return values[this.contactCols.team];
          }
        })
        .filter(this.onlyUnique),
      teamDistribution: {},
    };
  },
  mounted() {
    if (this.$refs.teamTable) {
      this.$refs.teamTable.toggleAllSelection();
    }
    this.newUsers.forEach(({ _index, values }) => {
      this.$set(
        this.teamDistribution,
        `${values[this.contactCols.name]}`,
        `${values[this.contactCols.team]}`
      );
    });
  },
  methods: {
    reRenderTable() {
      this.newTeams.push("test");
      this.newTeams.pop();
      this.$refs.teamTable.toggleAllSelection();
    },
    onlyUnique(value, index, self) {
      return self.indexOf(value) === index && value;
    },
    onTeamsSelectedChange(val) {
      this.selectedTeams = val;
    },
    convertData(data) {
      const convertedData = [];
      data.forEach((member) => {
        convertedData.push({
          name: member[this.contactCols.name],
          role: member[this.contactCols.role],
          team: member[this.contactCols.team],
        });
      });
      return convertedData;
    },
    onSave() {
      this.newUsers.forEach(({ _index, values }) => {
        values[this.contactCols.team] =
          this.teamDistribution[values[this.contactCols.name]];
      });
      this.reRenderTable();
    },
    onRemove(employeeName) {
      this.newUsers.forEach((newUser, index) => {
        if (newUser.values[this.contactCols.name] === employeeName) {
          this.newUsers.splice(index, 1);
        }
      });
      this.reRenderTable();
    },
  },
  watch: {
    selectedTeams: function () {
      this.$emit("input", this.selectedTeams);
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
