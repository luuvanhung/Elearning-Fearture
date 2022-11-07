<template>
  <div class="block" style="min-width: 880px">
    <el-button @click="onSave()" class="save-btn">Save</el-button>
    <el-table
      class="table-responsive"
      ref="squadTable"
      highlight-current-row
      :data="tableData"
      @selection-change="onTeamsSelectedChange"
      border
      v-if="tableData.length > 0"
    >
      <el-table-column type="selection" align="center" />
      <el-table-column align="center" :min-width="200" label="Squad" fixed>
        <template v-slot="scope">
          {{ scope.row.squad }}
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
            <el-table-column label="Squad">
              <template slot-scope="scope">
                <el-select
                  v-model="squadDistribution[scope.row.team]"
                  placeholder="Select"
                >
                  <el-option
                    v-for="squad in squads"
                    :key="squad.value"
                    :label="squad.label"
                    :value="squad.value"
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
      <p>No new squads</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ConfirmAddNewSquad",
  props: ["newUsers", "contactCols", "newTeams"],
  computed: {
    tableData() {
      return this.newSquad.map((squad) => {
        return {
          squad: squad,
          teams: this.teamData
            .map((item) => {
              if (item.squad === squad) {
                return { team: item.team, squad: item.squad };
              }
            })
            .filter((item) => item),
        };
      });
    },
    squads() {
      return this.newSquad.map((squad) => {
        return {
          value: squad,
          label: squad,
        };
      });
    },
  },
  data() {
    return {
      selectedSquad: [],
      teamData: this.newTeams.map((item) => {
        return {
          team: item.team,
          squad: item.members[0][this.contactCols.squad],
        };
      }),
      newSquad: this.newUsers
        .map(({ _index, values }) => {
          let team = values[this.contactCols.team];
          if (team.toLowerCase().includes("squad")) {
            return values[this.contactCols.team].split(": ")[1];
          }
        })
        .filter(this.onlyUnique),
      squadDistribution: {},
    };
  },
  mounted() {
    if (this.$refs.squadTable) {
      this.$refs.squadTable.toggleAllSelection();
    }
    this.teamData.forEach((team) => {
      this.$set(this.squadDistribution, `${team.team}`, `${team.squad}`);
    });
  },
  methods: {
    reRenderTable() {
      this.newTeams.push("test");
      this.newTeams.pop();
      this.$refs.squadTable.toggleAllSelection();
    },
    onlyUnique(value, index, self) {
      return self.indexOf(value) === index && value;
    },
    onTeamsSelectedChange(val) {
      this.selectedSquad = val;
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
        team.squad = this.squadDistribution[team.team];
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
    selectedSquad: function () {
      this.$emit("input", this.selectedSquad);
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
